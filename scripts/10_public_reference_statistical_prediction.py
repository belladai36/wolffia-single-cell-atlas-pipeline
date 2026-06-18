#!/usr/bin/env python
from __future__ import annotations

import argparse
import os
from pathlib import Path

os.environ.setdefault("NUMBA_DISABLE_JIT", "1")
os.environ.setdefault("NUMBA_CACHE_DIR", "/private/tmp/numba-cache")
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/mplconfig")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import seaborn as sns
from scipy import sparse
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from pipeline_utils import load_config, project_path, write_json


def read_program_markers(path: Path) -> dict[str, list[dict[str, str]]]:
    marker_df = pd.read_csv(path)
    required = {"program", "gene"}
    missing = required.difference(marker_df.columns)
    if missing:
        raise ValueError(f"Program marker file is missing columns: {sorted(missing)}")

    markers: dict[str, list[dict[str, str]]] = {}
    for program, subdf in marker_df.groupby("program"):
        rows: list[dict[str, str]] = []
        for _, row in subdf.iterrows():
            gene_symbol = str(row["gene"]).strip() if pd.notna(row["gene"]) else ""
            gene_id = str(row.get("gene_id", "")).strip() if pd.notna(row.get("gene_id", "")) else ""
            if gene_symbol or gene_id:
                rows.append({"gene": gene_symbol, "gene_id": gene_id})
        if rows:
            markers[str(program)] = rows
    return markers


def read_label_rules(path: Path) -> pd.DataFrame:
    rule_df = pd.read_csv(path)
    required = {"dataset_name", "label_pattern", "broad_program"}
    missing = required.difference(rule_df.columns)
    if missing:
        raise ValueError(f"Label rule file is missing columns: {sorted(missing)}")

    if "priority" not in rule_df.columns:
        rule_df["priority"] = np.arange(len(rule_df))
    return rule_df.sort_values(["dataset_name", "priority"]).reset_index(drop=True)


def apply_label_rules(
    adata: sc.AnnData,
    label_column: str,
    rule_df: pd.DataFrame,
    dataset_name: str,
) -> sc.AnnData:
    if label_column not in adata.obs.columns:
        raise KeyError(f"Label column '{label_column}' was not found in adata.obs")

    labels = adata.obs[label_column].astype(str)
    broad_program = pd.Series(["unmapped"] * adata.n_obs, index=adata.obs_names, dtype="object")

    dataset_rules = rule_df[rule_df["dataset_name"].isin([dataset_name, "*"])].copy()
    for _, row in dataset_rules.iterrows():
        matched = labels.str.contains(str(row["label_pattern"]), case=False, regex=True, na=False)
        broad_program.loc[(broad_program == "unmapped") & matched] = str(row["broad_program"])

    adata.obs["original_label"] = labels.values
    adata.obs["broad_program"] = pd.Categorical(broad_program)
    return adata


def apply_direct_labels(adata: sc.AnnData, label_column: str) -> sc.AnnData:
    if label_column not in adata.obs.columns:
        raise KeyError(f"Label column '{label_column}' was not found in adata.obs")

    labels = adata.obs[label_column].astype(str)
    adata = adata.copy()
    adata.obs["original_label"] = labels.values
    adata.obs["broad_program"] = pd.Categorical(labels)
    return adata


def initialize_unlabeled_dataset(adata: sc.AnnData) -> sc.AnnData:
    adata = adata.copy()
    adata.obs["original_label"] = pd.Series(["unlabeled"] * adata.n_obs, index=adata.obs_names, dtype="object")
    adata.obs["broad_program"] = pd.Categorical(["unlabeled"] * adata.n_obs)
    return adata


def normalize_for_reference_analysis(adata: sc.AnnData) -> sc.AnnData:
    adata = adata.copy()
    if "counts" in adata.layers:
        adata.X = adata.layers["counts"].copy()
    if sparse.issparse(adata.X):
        adata.X = adata.X.tocsr().astype(np.float32)
        counts_per_cell = np.asarray(adata.X.sum(axis=1)).ravel()
        counts_per_cell[counts_per_cell == 0] = 1.0
        scale = np.divide(10000.0, counts_per_cell, dtype=np.float32)
        adata.X = sparse.diags(scale) @ adata.X
    else:
        adata.X = np.asarray(adata.X, dtype=np.float32)
        counts_per_cell = adata.X.sum(axis=1, keepdims=True)
        counts_per_cell[counts_per_cell == 0] = 1.0
        adata.X = (adata.X / counts_per_cell) * 10000.0
    adata.X = adata.X.log1p() if sparse.issparse(adata.X) else np.log1p(adata.X)
    return adata


def ensure_pca(adata: sc.AnnData, n_pcs: int, random_state: int) -> None:
    if "X_pca" in adata.obsm:
        return
    n_comps = min(n_pcs, adata.n_vars, max(2, adata.n_obs - 1))
    sc.pp.pca(adata, n_comps=n_comps, svd_solver="arpack", random_state=random_state)


def build_feature_alias_map(adata: sc.AnnData) -> dict[str, str]:
    alias_map: dict[str, str] = {}
    for var_name in adata.var_names.astype(str):
        alias_map.setdefault(var_name.lower(), var_name)

    if "gene_ids" in adata.var.columns:
        for var_name, gene_id in zip(adata.var_names.astype(str), adata.var["gene_ids"].astype(str), strict=False):
            if gene_id and gene_id.lower() != "nan":
                alias_map.setdefault(gene_id.lower(), var_name)
    return alias_map


def resolve_program_markers(
    adata: sc.AnnData,
    markers: dict[str, list[dict[str, str]]],
) -> tuple[dict[str, list[str]], pd.DataFrame]:
    alias_map = build_feature_alias_map(adata)
    resolved: dict[str, list[str]] = {}
    summary_rows: list[dict[str, object]] = []

    for program, marker_rows in markers.items():
        present: list[str] = []
        requested: list[str] = []
        resolved_pairs: list[str] = []

        for marker_row in marker_rows:
            candidates = [marker_row.get("gene", ""), marker_row.get("gene_id", "")]
            requested_label = marker_row.get("gene") or marker_row.get("gene_id") or "unknown_marker"
            requested.append(requested_label)

            matched = None
            for candidate in candidates:
                key = str(candidate).strip().lower()
                if key and key in alias_map:
                    matched = alias_map[key]
                    break

            if matched is not None:
                present.append(matched)
                resolved_pairs.append(f"{requested_label}:{matched}")

        unique_present = list(dict.fromkeys(present))
        resolved[program] = unique_present
        summary_rows.append(
            {
                "program": program,
                "n_input_markers": len(marker_rows),
                "n_markers_found": len(unique_present),
                "markers_requested": ",".join(requested),
                "markers_found": ",".join(unique_present),
                "marker_resolution": ",".join(resolved_pairs),
            }
        )

    return resolved, pd.DataFrame(summary_rows)


def compute_program_scores(
    adata: sc.AnnData,
    markers: dict[str, list[dict[str, str]]],
) -> tuple[sc.AnnData, pd.DataFrame]:
    adata = adata.copy()
    resolved_markers, score_df = resolve_program_markers(adata, markers)

    for program, present in resolved_markers.items():
        if present:
            sc.tl.score_genes(adata, gene_list=present, score_name=f"{program}_score", use_raw=False)
        else:
            adata.obs[f"{program}_score"] = 0.0

    return adata, score_df


def infer_labels_from_cluster_scores(
    adata: sc.AnnData,
    cluster_column: str,
    program_names: list[str],
    min_top_score: float,
    min_margin: float,
) -> tuple[sc.AnnData, pd.DataFrame, pd.DataFrame]:
    if cluster_column not in adata.obs.columns:
        raise KeyError(f"Cluster column '{cluster_column}' was not found in adata.obs")

    adata = adata.copy()
    score_cols = [f"{program}_score" for program in program_names if f"{program}_score" in adata.obs.columns]
    cluster_labels = adata.obs[cluster_column].astype(str)
    summary_df = adata.obs.assign(cluster_label=cluster_labels).groupby("cluster_label", observed=True)[score_cols].mean()

    assignment_rows: list[dict[str, object]] = []
    cluster_to_program: dict[str, str] = {}

    for cluster_label, row in summary_df.iterrows():
        ordered = row.sort_values(ascending=False)
        top_col = ordered.index[0]
        top_score = float(ordered.iloc[0])
        second_score = float(ordered.iloc[1]) if len(ordered) > 1 else float("-inf")
        margin = top_score - second_score if np.isfinite(second_score) else np.inf
        program = top_col.removesuffix("_score")

        if top_score < min_top_score or margin < min_margin:
            assigned = "unmapped"
        else:
            assigned = program

        cluster_to_program[str(cluster_label)] = assigned
        assignment_rows.append(
            {
                "cluster_label": str(cluster_label),
                "assigned_program": assigned,
                "top_program": program,
                "top_score": top_score,
                "second_score": second_score,
                "score_margin": margin,
            }
        )

    adata.obs["original_label"] = cluster_labels.values
    adata.obs["broad_program"] = pd.Categorical(cluster_labels.map(cluster_to_program).fillna("unmapped"))
    assignment_df = pd.DataFrame(assignment_rows).sort_values("cluster_label").reset_index(drop=True)
    summary_df = summary_df.reset_index()
    return adata, assignment_df, summary_df


def plot_program_heatmap(adata: sc.AnnData, program_names: list[str], output_path: Path) -> None:
    score_cols = [f"{program}_score" for program in program_names if f"{program}_score" in adata.obs.columns]
    plot_df = adata.obs.loc[adata.obs["broad_program"] != "unmapped", ["broad_program", *score_cols]].copy()
    if plot_df.empty or not score_cols:
        return

    summary_df = plot_df.groupby("broad_program", observed=True)[score_cols].mean()
    plt.figure(figsize=(10, max(4, 0.6 * len(summary_df.index))))
    sns.heatmap(summary_df, cmap="viridis", center=0)
    plt.title("Mean Program Scores by Broad Program")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_program_boxplots(adata: sc.AnnData, program_names: list[str], output_path: Path) -> None:
    score_cols = [f"{program}_score" for program in program_names if f"{program}_score" in adata.obs.columns]
    plot_df = adata.obs.loc[adata.obs["broad_program"] != "unmapped", ["broad_program", *score_cols]].copy()
    if plot_df.empty or not score_cols:
        return

    long_df = plot_df.melt(id_vars="broad_program", value_vars=score_cols, var_name="program_score", value_name="score")
    long_df["program_score"] = long_df["program_score"].str.replace("_score", "", regex=False)

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=long_df, x="program_score", y="score", hue="broad_program", showfliers=False)
    plt.xticks(rotation=45, ha="right")
    plt.title("Program Scores Across Broad Programs")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def save_predicted_label_counts(labels: np.ndarray, output_path: Path) -> None:
    pd.Series(labels, name="predicted_broad_program").value_counts().rename_axis("predicted_broad_program").reset_index(
        name="n_cells"
    ).to_csv(output_path, index=False)


def save_pca_plot(adata: sc.AnnData, color: str, output_path: Path, title: str, n_pcs: int, random_state: int) -> None:
    ensure_pca(adata, n_pcs=n_pcs, random_state=random_state)
    coords = adata.obsm["X_pca"][:, :2]
    plot_df = pd.DataFrame(
        {
            "PC1": coords[:, 0],
            "PC2": coords[:, 1],
            color: adata.obs[color].astype(str).to_numpy(),
        }
    )

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=plot_df, x="PC1", y="PC2", hue=color, s=10, linewidth=0)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def dense_matrix(x) -> np.ndarray:
    if sparse.issparse(x):
        return x.toarray()
    return np.asarray(x)


def prepare_classifier_inputs(
    train_adata: sc.AnnData,
    test_adata: sc.AnnData,
    n_top_hvgs: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    shared_genes = train_adata.var_names.intersection(test_adata.var_names)
    if len(shared_genes) < 50:
        raise ValueError("Too few shared genes between train and test datasets for transfer analysis.")

    train_shared = train_adata[:, shared_genes].copy()
    test_shared = test_adata[:, shared_genes].copy()

    sc.pp.highly_variable_genes(train_shared, n_top_genes=min(n_top_hvgs, train_shared.n_vars), flavor="seurat")
    selected_genes = train_shared.var_names[train_shared.var["highly_variable"]].tolist()
    if len(selected_genes) < 20:
        raise ValueError("Too few highly variable genes were selected for classifier training.")

    train_selected = train_shared[:, selected_genes].copy()
    test_selected = test_shared[:, selected_genes].copy()

    x_train = dense_matrix(train_selected.X)
    x_test = dense_matrix(test_selected.X)
    y_train = train_selected.obs["broad_program"].astype(str).to_numpy()
    return x_train, x_test, y_train, selected_genes


def build_classifier(classifier_name: str, n_components: int, random_state: int):
    if classifier_name == "random_forest":
        return Pipeline(
            steps=[
                ("scale", StandardScaler()),
                ("pca", PCA(n_components=n_components, random_state=random_state)),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=300,
                        random_state=random_state,
                        class_weight="balanced",
                    ),
                ),
            ]
        )

    return Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=n_components, random_state=random_state)),
            (
                "classifier",
                LogisticRegression(
                    max_iter=3000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: list[str],
    output_path: Path,
) -> None:
    cm = confusion_matrix(y_true, y_pred, labels=labels, normalize="true")
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt=".2f", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Cross-Dataset Transfer Confusion Matrix")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run statistical prediction on public reference single-cell datasets.")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    analysis_cfg = config.get("public_reference_analysis", {})
    if not analysis_cfg:
        raise ValueError("Missing 'public_reference_analysis' section in config/config.yaml")

    output_dir = project_path(analysis_cfg["output_dir"])
    figure_dir = project_path(analysis_cfg["figure_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    random_state = analysis_cfg.get("random_state", config.get("analysis", {}).get("random_state", 42))
    n_top_hvgs = analysis_cfg.get("n_top_hvgs", 2000)
    n_pcs = analysis_cfg.get("n_pcs", config.get("analysis", {}).get("n_pcs", 30))
    min_cells = analysis_cfg.get("min_cells_per_program", 20)
    classifier_name = analysis_cfg.get("classifier", "logistic_regression")
    train_label_mode = analysis_cfg.get("train_label_mode", "rule_based")
    test_label_mode = analysis_cfg.get("test_label_mode", "rule_based")
    max_train_cells = analysis_cfg.get("max_train_cells")
    max_test_cells = analysis_cfg.get("max_test_cells")
    infer_min_score = float(analysis_cfg.get("infer_min_score", -1.0))
    infer_min_margin = float(analysis_cfg.get("infer_min_margin", 0.0))

    print("Loading reference datasets...")
    train_adata = sc.read_h5ad(project_path(analysis_cfg["train_h5ad"]))
    test_adata = sc.read_h5ad(project_path(analysis_cfg["test_h5ad"]))
    print(f"Train dataset: {train_adata.n_obs} cells x {train_adata.n_vars} genes")
    print(f"Test dataset: {test_adata.n_obs} cells x {test_adata.n_vars} genes")

    markers = read_program_markers(project_path(analysis_cfg["program_markers_csv"]))
    rule_df = None
    if "rule_based" in {train_label_mode, test_label_mode}:
        rule_df = read_label_rules(project_path(analysis_cfg["label_rules_csv"]))

    if test_label_mode == "direct":
        test_adata = apply_direct_labels(test_adata, label_column=analysis_cfg["test_label_column"])
        test_has_labels = True
    elif test_label_mode == "rule_based":
        test_adata = apply_label_rules(
            test_adata,
            label_column=analysis_cfg["test_label_column"],
            rule_df=rule_df,
            dataset_name=analysis_cfg["test_dataset_name"],
        )
        test_has_labels = True
    elif test_label_mode == "unlabeled":
        test_adata = initialize_unlabeled_dataset(test_adata)
        test_has_labels = False
    else:
        raise ValueError(f"Unsupported test_label_mode: {test_label_mode}")

    train_adata = normalize_for_reference_analysis(train_adata)
    test_adata = normalize_for_reference_analysis(test_adata)
    print("Finished normalization.")

    train_adata, train_marker_summary = compute_program_scores(train_adata, markers)
    test_adata, test_marker_summary = compute_program_scores(test_adata, markers)
    print("Computed program scores.")

    train_marker_summary.to_csv(output_dir / "train_marker_recovery.csv", index=False)
    test_marker_summary.to_csv(output_dir / "test_marker_recovery.csv", index=False)

    if train_label_mode == "direct":
        train_adata = apply_direct_labels(train_adata, label_column=analysis_cfg["train_label_column"])
    elif train_label_mode == "rule_based":
        train_adata = apply_label_rules(
            train_adata,
            label_column=analysis_cfg["train_label_column"],
            rule_df=rule_df,
            dataset_name=analysis_cfg["train_dataset_name"],
        )
    elif train_label_mode == "infer_from_cluster_scores":
        train_adata, cluster_assignment_df, cluster_score_df = infer_labels_from_cluster_scores(
            train_adata,
            cluster_column=analysis_cfg["train_label_column"],
            program_names=list(markers),
            min_top_score=infer_min_score,
            min_margin=infer_min_margin,
        )
        cluster_assignment_df.to_csv(output_dir / "train_cluster_program_assignments.csv", index=False)
        cluster_score_df.to_csv(output_dir / "train_cluster_program_scores.csv", index=False)
    else:
        raise ValueError(f"Unsupported train_label_mode: {train_label_mode}")

    save_pca_plot(
        train_adata,
        "broad_program",
        figure_dir / "train_broad_program_pca.png",
        "Train Broad Programs",
        n_pcs=n_pcs,
        random_state=random_state,
    )
    plot_program_heatmap(train_adata, list(markers), figure_dir / "train_program_score_heatmap.png")
    plot_program_boxplots(train_adata, list(markers), figure_dir / "train_program_score_boxplots.png")
    if test_has_labels:
        save_pca_plot(
            test_adata,
            "broad_program",
            figure_dir / "test_broad_program_pca.png",
            "Test Broad Programs",
            n_pcs=n_pcs,
            random_state=random_state,
        )
        plot_program_heatmap(test_adata, list(markers), figure_dir / "test_program_score_heatmap.png")

    train_labeled = train_adata[train_adata.obs["broad_program"] != "unmapped"].copy()
    valid_programs = train_labeled.obs["broad_program"].value_counts()
    valid_programs = valid_programs[valid_programs >= min_cells].index.tolist()
    train_labeled = train_labeled[train_labeled.obs["broad_program"].isin(valid_programs)].copy()

    if train_labeled.n_obs == 0:
        raise ValueError("No labeled training cells remained after applying labels and minimum cell thresholds.")

    if max_train_cells and train_labeled.n_obs > int(max_train_cells):
        sc.pp.subsample(train_labeled, n_obs=int(max_train_cells), random_state=random_state, copy=False)
    print(f"Training cells after filtering: {train_labeled.n_obs}")

    if test_has_labels:
        test_prediction_input = test_adata[test_adata.obs["broad_program"].isin(valid_programs)].copy()
        if test_prediction_input.n_obs == 0:
            raise ValueError("No labeled target cells remained after filtering target labels to training programs.")
    else:
        test_prediction_input = test_adata.copy()

    if max_test_cells and test_prediction_input.n_obs > int(max_test_cells):
        sc.pp.subsample(test_prediction_input, n_obs=int(max_test_cells), random_state=random_state, copy=False)
    print(f"Target cells for prediction: {test_prediction_input.n_obs}")

    x_train, x_test, y_train, selected_genes = prepare_classifier_inputs(train_labeled, test_prediction_input, n_top_hvgs)
    print(f"Prepared classifier inputs using {len(selected_genes)} genes.")
    n_components = min(30, x_train.shape[0] - 1, x_train.shape[1])
    if n_components < 2:
        raise ValueError("Too few dimensions are available for PCA-based classifier training.")

    model = build_classifier(classifier_name, n_components=n_components, random_state=random_state)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Finished classifier training and prediction.")

    labels = sorted(np.unique(y_train).tolist())
    metrics = {
        "classifier": classifier_name,
        "train_dataset_name": analysis_cfg["train_dataset_name"],
        "test_dataset_name": analysis_cfg["test_dataset_name"],
        "n_train_cells": int(x_train.shape[0]),
        "n_test_cells": int(x_test.shape[0]),
        "n_selected_genes": int(len(selected_genes)),
        "selected_genes_preview": selected_genes[:50],
        "labels_used": labels,
        "test_label_mode": test_label_mode,
    }

    if test_has_labels:
        y_test = test_prediction_input.obs["broad_program"].astype(str).to_numpy()
        report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()
        report_df.to_csv(output_dir / "cross_dataset_classification_report.csv")
        metrics["accuracy"] = float(accuracy_score(y_test, y_pred))
        plot_confusion_matrix(y_test, y_pred, labels, figure_dir / "cross_dataset_confusion_matrix.png")

    write_json(metrics, output_dir / "cross_dataset_metrics.json")
    save_predicted_label_counts(y_pred, output_dir / "predicted_label_counts.csv")

    test_prediction_input.obs["predicted_broad_program"] = y_pred
    save_pca_plot(
        test_prediction_input,
        "predicted_broad_program",
        figure_dir / "test_predicted_broad_program_pca.png",
        "Predicted Broad Programs on Test Dataset",
        n_pcs=n_pcs,
        random_state=random_state,
    )

    train_adata.write_h5ad(output_dir / "train_reference_scored.h5ad")
    test_adata.obs["predicted_broad_program"] = pd.Series(y_pred, index=test_prediction_input.obs_names)
    test_adata.write_h5ad(output_dir / "test_reference_scored.h5ad")
    print(f"Wrote outputs to {output_dir}")


if __name__ == "__main__":
    main()
