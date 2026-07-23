#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("NUMBA_CACHE_DIR", "/private/tmp/numba-cache")
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/mplconfig")

import anndata as ad
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import seaborn as sns
from scipy import sparse
from sklearn.base import clone
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from pipeline_utils import PROJECT_ROOT


DEFAULT_LEAF_REFERENCE = PROJECT_ROOT / "data" / "public_references" / "processed" / "GSE161332_leaf.h5ad"
DEFAULT_MARKERS = PROJECT_ROOT / "data" / "metadata" / "public_reference_program_markers.csv"
DEFAULT_TRANSFER_FEATURES = PROJECT_ROOT / "data" / "metadata" / "wolffia_transfer_feature_set.csv"
DEFAULT_PUBLISHED_METADATA = (
    PROJECT_ROOT / "data" / "public_references" / "raw" / "GSE161332" / "pscb_leaf" / "leaf_metadata_from_pscb.csv"
)
DEFAULT_CLUSTER_MAP = PROJECT_ROOT / "data" / "metadata" / "gse161332_pscb_cluster_annotation_map.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results" / "leaf_primary_ortholog_model"
DEFAULT_FIGURE_DIR = PROJECT_ROOT / "figures" / "leaf_primary_ortholog_model"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Train and benchmark a leaf-primary Arabidopsis model restricted to "
            "Arabidopsis-to-Wolffia ortholog transfer features."
        )
    )
    parser.add_argument("--leaf-reference", type=Path, default=DEFAULT_LEAF_REFERENCE)
    parser.add_argument("--markers", type=Path, default=DEFAULT_MARKERS)
    parser.add_argument("--transfer-features", type=Path, default=DEFAULT_TRANSFER_FEATURES)
    parser.add_argument(
        "--published-metadata",
        type=Path,
        default=DEFAULT_PUBLISHED_METADATA,
        help="Optional PSCB/Kim et al. metadata CSV extracted from leaf.RDS.",
    )
    parser.add_argument(
        "--cluster-map",
        type=Path,
        default=DEFAULT_CLUSTER_MAP,
        help="Cluster-to-broad-program mapping for the PSCB/Kim et al. leaf atlas.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--figure-dir", type=Path, default=DEFAULT_FIGURE_DIR)
    parser.add_argument("--feature-column", default="arabidopsis_gene_id")
    parser.add_argument("--n-pcs", type=int, default=30)
    parser.add_argument("--n-clusters", type=int, default=18)
    parser.add_argument("--n-splits", type=int, default=5)
    parser.add_argument("--min-cluster-margin", type=float, default=0.05)
    parser.add_argument("--min-cells-per-program", type=int, default=20)
    parser.add_argument("--min-model-confidence", type=float, default=0.60)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument(
        "--write-scored-h5ad",
        action="store_true",
        help="Write a full scored/pseudolabeled h5ad. Off by default because this file is large.",
    )
    return parser.parse_args()


def attach_published_cluster_labels(
    adata: ad.AnnData,
    metadata_path: Path,
    cluster_map_path: Path,
) -> tuple[ad.AnnData, pd.DataFrame] | tuple[None, None]:
    if not metadata_path.exists() or not cluster_map_path.exists():
        return None, None
    adata = adata.copy()
    metadata = pd.read_csv(metadata_path, index_col=0)
    cluster_map = pd.read_csv(cluster_map_path)
    cluster_map["cluster_id"] = cluster_map["cluster_id"].astype(str)
    metadata["seurat_clusters"] = metadata["seurat_clusters"].astype(str)
    annotated = metadata.merge(
        cluster_map,
        left_on="seurat_clusters",
        right_on="cluster_id",
        how="left",
    )
    annotated.index = metadata.index.astype(str)
    shared = adata.obs_names.astype(str).intersection(annotated.index.astype(str))
    if len(shared) == 0:
        raise ValueError(f"No overlapping barcodes were found between {metadata_path} and the leaf AnnData object.")
    adata.obs["published_leaf_cluster"] = pd.Series(index=adata.obs_names, dtype="object")
    adata.obs["published_leaf_label"] = pd.Series(index=adata.obs_names, dtype="object")
    adata.obs["published_broad_program"] = pd.Series(index=adata.obs_names, dtype="object")
    adata.obs.loc[shared, "published_leaf_cluster"] = annotated.loc[shared, "seurat_clusters"].astype(str)
    adata.obs.loc[shared, "published_leaf_label"] = annotated.loc[shared, "published_cluster_label"].astype(str)
    adata.obs.loc[shared, "published_broad_program"] = annotated.loc[shared, "broad_program"].astype(str)
    adata.obs["published_broad_program"] = adata.obs["published_broad_program"].fillna("unlabeled")
    summary = (
        adata.obs.loc[shared, ["published_leaf_cluster", "published_leaf_label", "published_broad_program"]]
        .value_counts(dropna=False)
        .rename("n_cells")
        .reset_index()
        .sort_values(["published_leaf_cluster"])
    )
    return adata, summary


def normalize_counts(adata: ad.AnnData) -> ad.AnnData:
    adata = adata.copy()
    if "counts" in adata.layers:
        adata.X = adata.layers["counts"].copy()
    if sparse.issparse(adata.X):
        adata.X = adata.X.tocsr().astype(np.float32)
        counts_per_cell = np.asarray(adata.X.sum(axis=1)).ravel()
        counts_per_cell[counts_per_cell == 0] = 1.0
        adata.X = sparse.diags(10000.0 / counts_per_cell) @ adata.X
        adata.X = adata.X.log1p()
    else:
        x = np.asarray(adata.X, dtype=np.float32)
        counts_per_cell = x.sum(axis=1, keepdims=True)
        counts_per_cell[counts_per_cell == 0] = 1.0
        adata.X = np.log1p((x / counts_per_cell) * 10000.0)
    return adata


def read_markers(path: Path) -> dict[str, list[str]]:
    marker_table = pd.read_csv(path)
    markers: dict[str, list[str]] = {}
    for program, subframe in marker_table.groupby("program", sort=True):
        genes = subframe["gene_id"].dropna().astype(str).drop_duplicates().tolist()
        markers[str(program)] = genes
    return markers


def score_programs(adata: ad.AnnData, markers: dict[str, list[str]]) -> tuple[ad.AnnData, pd.DataFrame]:
    adata = adata.copy()
    rows: list[dict[str, object]] = []
    gene_set = set(adata.var_names.astype(str))
    for program, requested in markers.items():
        present = [gene for gene in requested if gene in gene_set]
        if present:
            sc.tl.score_genes(adata, gene_list=present, score_name=f"{program}_score", use_raw=False)
        else:
            adata.obs[f"{program}_score"] = 0.0
        rows.append(
            {
                "program": program,
                "n_requested_markers": len(requested),
                "n_present_markers": len(present),
                "present_markers": ",".join(present),
            }
        )
    return adata, pd.DataFrame(rows)


def add_leaf_clusters(adata: ad.AnnData, n_pcs: int, n_clusters: int, random_state: int) -> ad.AnnData:
    adata = adata.copy()
    sc.pp.highly_variable_genes(adata, n_top_genes=min(2000, adata.n_vars), flavor="seurat")
    n_comps = min(n_pcs, adata.n_obs - 1, int(adata.var["highly_variable"].sum()))
    sc.pp.pca(
        adata,
        n_comps=max(2, n_comps),
        mask_var="highly_variable",
        random_state=random_state,
        svd_solver="arpack",
    )
    from sklearn.cluster import KMeans

    clusters = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=20).fit_predict(adata.obsm["X_pca"])
    adata.obs["leaf_pseudocluster"] = pd.Categorical(clusters.astype(str))
    return adata


def assign_cluster_pseudo_labels(
    adata: ad.AnnData,
    min_margin: float,
) -> tuple[ad.AnnData, pd.DataFrame, pd.DataFrame]:
    adata = adata.copy()
    score_columns = [column for column in adata.obs.columns if column.endswith("_score")]
    if len(score_columns) < 2:
        raise ValueError("At least two program score columns are required.")
    cluster_scores = (
        adata.obs.groupby("leaf_pseudocluster", observed=True)[score_columns]
        .mean()
        .sort_index()
    )
    assignment_rows: list[dict[str, object]] = []
    cluster_to_program: dict[str, str] = {}
    for cluster, row in cluster_scores.iterrows():
        ordered = row.sort_values(ascending=False)
        top_program = ordered.index[0].removesuffix("_score")
        second_program = ordered.index[1].removesuffix("_score")
        top_score = float(ordered.iloc[0])
        second_score = float(ordered.iloc[1])
        margin = top_score - second_score
        assigned = top_program if margin >= min_margin else "ambiguous"
        cluster_to_program[str(cluster)] = assigned
        assignment_rows.append(
            {
                "leaf_pseudocluster": str(cluster),
                "assigned_program": assigned,
                "top_program": top_program,
                "top_score": top_score,
                "second_program": second_program,
                "second_score": second_score,
                "score_margin": margin,
                "n_cells": int((adata.obs["leaf_pseudocluster"].astype(str) == str(cluster)).sum()),
            }
        )
    adata.obs["leaf_pseudo_label"] = pd.Categorical(
        adata.obs["leaf_pseudocluster"].astype(str).map(cluster_to_program).fillna("ambiguous")
    )
    return adata, pd.DataFrame(assignment_rows), cluster_scores.reset_index()


def load_transfer_features(path: Path, column: str, adata: ad.AnnData) -> tuple[list[str], pd.DataFrame]:
    feature_table = pd.read_csv(path)
    if column not in feature_table.columns:
        raise KeyError(f"Feature column {column!r} was not found in {path}.")
    requested = feature_table[column].dropna().astype(str).drop_duplicates().tolist()
    present = [gene for gene in requested if gene in set(adata.var_names.astype(str))]
    coverage = pd.DataFrame(
        {
            "requested_transfer_features": [len(requested)],
            "present_transfer_features": [len(present)],
            "feature_coverage": [len(present) / len(requested) if requested else 0.0],
        }
    )
    if len(present) < 20:
        raise ValueError(f"Only {len(present)} transfer features were present in the leaf matrix.")
    return present, coverage


def dense_float32(matrix) -> np.ndarray:
    if sparse.issparse(matrix):
        return matrix.toarray().astype(np.float32, copy=False)
    return np.asarray(matrix, dtype=np.float32)


def make_h5ad_string_columns_portable(adata: ad.AnnData) -> ad.AnnData:
    adata = adata.copy()
    adata.obs_names = adata.obs_names.astype(str)
    adata.var_names = adata.var_names.astype(str)
    adata.obs.index.name = None
    adata.var.index.name = None
    for column in adata.obs.columns:
        if pd.api.types.is_string_dtype(adata.obs[column]):
            adata.obs[column] = adata.obs[column].astype(object).astype(str)
    for column in adata.var.columns:
        if pd.api.types.is_string_dtype(adata.var[column]):
            adata.var[column] = adata.var[column].astype(object).astype(str)
    ad.settings.allow_write_nullable_strings = True
    return adata


def build_models(n_pcs: int, random_state: int) -> dict[str, Pipeline]:
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("scale", StandardScaler()),
                ("pca", PCA(n_components=n_pcs, random_state=random_state)),
                (
                    "classifier",
                    LogisticRegression(max_iter=3000, class_weight="balanced", random_state=random_state),
                ),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("scale", StandardScaler()),
                ("pca", PCA(n_components=n_pcs, random_state=random_state)),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=400,
                        class_weight="balanced_subsample",
                        min_samples_leaf=2,
                        n_jobs=-1,
                        random_state=random_state,
                    ),
                ),
            ]
        ),
    }


def run_stratified_cv(
    x: np.ndarray,
    y: np.ndarray,
    models: dict[str, Pipeline],
    n_splits: int,
    random_state: int,
    min_confidence: float,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    metric_rows: list[dict[str, object]] = []
    prediction_frames: list[pd.DataFrame] = []
    consensus_frames: list[pd.DataFrame] = []
    for fold, (train_index, test_index) in enumerate(splitter.split(x, y), start=1):
        fold_predictions = pd.DataFrame(
            {
                "fold": fold,
                "cell_index": test_index,
                "true_pseudo_label": y[test_index],
            }
        )
        for model_name, model_template in models.items():
            model = clone(model_template)
            model.fit(x[train_index], y[train_index])
            predicted = model.predict(x[test_index])
            probabilities = model.predict_proba(x[test_index])
            confidence = probabilities.max(axis=1)
            metric_rows.append(
                {
                    "model": model_name,
                    "fold": fold,
                    "n_train_cells": len(train_index),
                    "n_test_cells": len(test_index),
                    "accuracy": accuracy_score(y[test_index], predicted),
                    "balanced_accuracy": balanced_accuracy_score(y[test_index], predicted),
                    "macro_f1": f1_score(y[test_index], predicted, average="macro", zero_division=0),
                    "mean_confidence": float(confidence.mean()),
                }
            )
            fold_predictions[f"{model_name}_prediction"] = predicted
            fold_predictions[f"{model_name}_confidence"] = confidence
        prediction_frames.append(fold_predictions)
        consensus = fold_predictions.copy()
        consensus["model_agreement"] = (
            consensus["logistic_regression_prediction"] == consensus["random_forest_prediction"]
        )
        consensus["minimum_model_confidence"] = consensus[
            ["logistic_regression_confidence", "random_forest_confidence"]
        ].min(axis=1)
        consensus["consensus_accepted"] = consensus["model_agreement"] & (
            consensus["minimum_model_confidence"] >= min_confidence
        )
        consensus["consensus_label"] = np.where(
            consensus["consensus_accepted"],
            consensus["logistic_regression_prediction"],
            "ambiguous",
        )
        consensus_frames.append(consensus)
    return pd.DataFrame(metric_rows), pd.concat(prediction_frames, ignore_index=True), pd.concat(
        consensus_frames, ignore_index=True
    )


def save_confusion_figure(
    consensus: pd.DataFrame,
    labels: list[str],
    output_path: Path,
    label_source: str,
) -> None:
    accepted = consensus[consensus["consensus_accepted"]].copy()
    if accepted.empty:
        plt.figure(figsize=(7, 5))
        plt.text(0.5, 0.5, "No accepted consensus predictions", ha="center", va="center")
        plt.axis("off")
    else:
        matrix = confusion_matrix(
            accepted["true_pseudo_label"],
            accepted["consensus_label"],
            labels=labels,
            normalize="true",
        )
        plt.figure(figsize=(9, 7))
        sns.heatmap(matrix, annot=True, fmt=".2f", cmap="Greens", xticklabels=labels, yticklabels=labels)
        plt.xlabel("Accepted consensus prediction")
        ylabel = "Published broad program" if label_source == "published_cluster_labels" else "Marker-derived pseudo-label"
        plt.ylabel(ylabel)
        plt.title("Leaf-primary consensus on held-out cells")
        plt.xticks(rotation=35, ha="right")
        plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close()


def save_counts_figure(adata: ad.AnnData, output_path: Path, label_column: str) -> None:
    counts = adata.obs[label_column].astype(str).value_counts().rename_axis("program").reset_index(name="n_cells")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=counts, x="program", y="n_cells", color="#59A14F")
    plt.xticks(rotation=35, ha="right")
    plt.xlabel("Leaf broad program label")
    plt.ylabel("Cells")
    plt.title("Leaf reference label composition")
    plt.tight_layout()
    plt.savefig(output_path, dpi=220)
    plt.close()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")

    leaf = normalize_counts(ad.read_h5ad(args.leaf_reference))
    markers = read_markers(args.markers)
    leaf, marker_recovery = score_programs(leaf, markers)
    leaf, published_label_summary = attach_published_cluster_labels(
        leaf,
        args.published_metadata,
        args.cluster_map,
    )
    label_source = "published_cluster_labels" if leaf is not None else "marker_pseudoclusters"
    if leaf is None:
        leaf = normalize_counts(ad.read_h5ad(args.leaf_reference))
        leaf, marker_recovery = score_programs(leaf, markers)
    leaf = add_leaf_clusters(leaf, args.n_pcs, args.n_clusters, args.random_state)
    leaf, cluster_assignments, cluster_scores = assign_cluster_pseudo_labels(leaf, args.min_cluster_margin)
    transfer_features, feature_coverage = load_transfer_features(args.transfer_features, args.feature_column, leaf)

    training_label_column = "published_broad_program" if label_source == "published_cluster_labels" else "leaf_pseudo_label"
    excluded_labels = ["ambiguous", "unlabeled", "nan", "None"]
    labeled = leaf[~leaf.obs[training_label_column].astype(str).isin(excluded_labels)].copy()
    label_counts = labeled.obs[training_label_column].astype(str).value_counts()
    valid_labels = label_counts[label_counts >= args.min_cells_per_program].index.tolist()
    labeled = labeled[labeled.obs[training_label_column].astype(str).isin(valid_labels)].copy()
    if labeled.obs[training_label_column].nunique() < 2:
        raise ValueError("Fewer than two labels remained after filtering; cannot train a classifier.")

    x = dense_float32(labeled[:, transfer_features].X)
    y = labeled.obs[training_label_column].astype(str).to_numpy()
    n_pcs = min(args.n_pcs, x.shape[0] - 1, x.shape[1])
    models = build_models(n_pcs=n_pcs, random_state=args.random_state)
    min_class_count = int(pd.Series(y).value_counts().min())
    n_splits = min(args.n_splits, min_class_count)
    if n_splits < 2:
        raise ValueError("At least two cells per label are required for cross-validation.")
    cv_metrics, cv_predictions, cv_consensus = run_stratified_cv(
        x,
        y,
        models,
        n_splits=n_splits,
        random_state=args.random_state,
        min_confidence=args.min_model_confidence,
    )

    fitted_paths: dict[str, str] = {}
    for model_name, model_template in models.items():
        fitted = clone(model_template)
        fitted.fit(x, y)
        path = args.output_dir / f"{model_name}_leaf_primary.joblib"
        joblib.dump(
            {
                "model": fitted,
                "selected_genes": transfer_features,
                "classes": sorted(np.unique(y).tolist()),
                "leaf_reference": str(args.leaf_reference),
                "feature_source": str(args.transfer_features),
                "label_status": (
                    "Published PSCB/Kim et al. cluster labels collapsed to broad programs"
                    if label_source == "published_cluster_labels"
                    else "leaf cluster marker-derived pseudo-labels, not curated cell-type truth"
                ),
                "model_role": "v2_leaf_primary",
            },
            path,
            compress=3,
        )
        fitted_paths[model_name] = str(path)

    metric_summary = (
        cv_metrics.groupby("model", as_index=False)
        .agg(
            accuracy=("accuracy", "mean"),
            balanced_accuracy=("balanced_accuracy", "mean"),
            macro_f1=("macro_f1", "mean"),
            mean_confidence=("mean_confidence", "mean"),
        )
        .sort_values(["balanced_accuracy", "macro_f1"], ascending=False)
    )
    consensus_accepted = cv_consensus["consensus_accepted"]
    accepted_subset = cv_consensus[consensus_accepted]
    accepted_accuracy = (
        accuracy_score(accepted_subset["true_pseudo_label"], accepted_subset["consensus_label"])
        if not accepted_subset.empty
        else float("nan")
    )
    consensus_counts = cv_consensus["consensus_label"].value_counts().to_dict()

    marker_recovery.to_csv(args.output_dir / "leaf_marker_recovery.csv", index=False)
    if published_label_summary is not None:
        published_label_summary.to_csv(args.output_dir / "published_leaf_cluster_label_summary.csv", index=False)
    cluster_assignments.to_csv(args.output_dir / "leaf_cluster_program_assignments.csv", index=False)
    cluster_scores.to_csv(args.output_dir / "leaf_cluster_program_scores.csv", index=False)
    feature_coverage.to_csv(args.output_dir / "leaf_transfer_feature_coverage.csv", index=False)
    cv_metrics.to_csv(args.output_dir / "leaf_primary_cv_fold_metrics.csv", index=False)
    cv_predictions.to_csv(args.output_dir / "leaf_primary_cv_predictions.csv", index=False)
    cv_consensus.to_csv(args.output_dir / "leaf_primary_cv_consensus.csv", index=False)
    metric_summary.to_csv(args.output_dir / "leaf_primary_model_metric_summary.csv", index=False)
    pd.Series(transfer_features, name="selected_gene").to_csv(
        args.output_dir / "leaf_primary_selected_transfer_features.csv",
        index=False,
    )
    cell_label_columns = [
        "leaf_pseudocluster",
        "leaf_pseudo_label",
        *[column for column in leaf.obs.columns if column.endswith("_score")],
    ]
    leaf.obs[cell_label_columns].to_csv(args.output_dir / "gse161332_leaf_cell_pseudolabels.csv")
    if args.write_scored_h5ad:
        make_h5ad_string_columns_portable(leaf).write_h5ad(
            args.output_dir / "gse161332_leaf_scored_pseudolabeled.h5ad"
        )

    save_counts_figure(leaf, args.figure_dir / "leaf_pseudo_label_counts.png", training_label_column)
    save_confusion_figure(
        cv_consensus,
        sorted(np.unique(y).tolist()),
        args.figure_dir / "leaf_primary_consensus_confusion_matrix.png",
        label_source,
    )

    summary = {
        "model_role": "v2_leaf_primary",
        "leaf_reference": str(args.leaf_reference),
        "label_source": label_source,
        "training_label_column": training_label_column,
        "label_status": (
            "Published PSCB/Kim et al. cluster labels collapsed to broad programs"
            if label_source == "published_cluster_labels"
            else "marker-derived pseudo-labels from leaf pseudoclusters; not curated cell-type truth"
        ),
        "n_leaf_cells": int(leaf.n_obs),
        "n_training_cells_after_filtering": int(labeled.n_obs),
        "training_label_counts_after_filtering": {
            str(k): int(v) for k, v in pd.Series(y).value_counts().to_dict().items()
        },
        "n_requested_transfer_features": int(feature_coverage["requested_transfer_features"].iloc[0]),
        "n_present_transfer_features": int(feature_coverage["present_transfer_features"].iloc[0]),
        "feature_coverage": float(feature_coverage["feature_coverage"].iloc[0]),
        "n_cv_splits": int(n_splits),
        "min_model_confidence": args.min_model_confidence,
        "consensus_acceptance_rate": float(consensus_accepted.mean()),
        "consensus_selective_accuracy": float(accepted_accuracy),
        "consensus_label_counts": {str(k): int(v) for k, v in consensus_counts.items()},
        "model_paths": fitted_paths,
        "interpretation": (
            "This leaf-primary model is more biologically relevant to Wolffia than the root-derived benchmark. "
            "Current accuracy values measure recovery of broad Arabidopsis leaf labels, not true Wolffia accuracy."
        ),
    }
    with open(args.output_dir / "leaf_primary_model_summary.json", "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(metric_summary.to_string(index=False))
    print(
        f"Consensus accepted {consensus_accepted.sum():,}/{len(cv_consensus):,} held-out leaf cells "
        f"({consensus_accepted.mean():.1%}); selective label recovery = {accepted_accuracy:.1%}."
    )
    print(f"Wrote results to {args.output_dir}")
    print(f"Wrote figures to {args.figure_dir}")


if __name__ == "__main__":
    main()
