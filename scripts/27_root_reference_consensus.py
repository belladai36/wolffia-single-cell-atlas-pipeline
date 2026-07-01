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
import seaborn as sns
from scipy import sparse
from scipy.optimize import minimize_scalar
from sklearn.base import clone
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    log_loss,
)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from pipeline_utils import PROJECT_ROOT


DEFAULT_ROOT_REFERENCE = (
    PROJECT_ROOT
    / "results"
    / "public_reference_gse123818_wt_train_to_gse121619"
    / "train_reference_scored.h5ad"
)
DEFAULT_SECOND_ROOT = (
    PROJECT_ROOT
    / "results"
    / "public_reference_gse123818_wt_train_to_gse121619"
    / "test_reference_scored.h5ad"
)
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results" / "root_reference_consensus"
DEFAULT_FIGURE_DIR = PROJECT_ROOT / "figures" / "root_reference_consensus"

SHORT_PROGRAM_LABELS = {
    "abiotic_stress_response": "Stress",
    "proliferative_or_meristematic": "Proliferative",
    "transport_interface_or_water_balance": "Transport / water",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark root-derived broad-program classifiers and build a conservative consensus set."
    )
    parser.add_argument("--root-reference", type=Path, default=DEFAULT_ROOT_REFERENCE)
    parser.add_argument("--second-root", type=Path, default=DEFAULT_SECOND_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--figure-dir", type=Path, default=DEFAULT_FIGURE_DIR)
    parser.add_argument(
        "--feature-list",
        type=Path,
        default=None,
        help="Optional CSV containing a fixed cross-species-compatible feature list.",
    )
    parser.add_argument("--feature-column", default="arabidopsis_gene_id")
    parser.add_argument("--n-top-hvgs", type=int, default=2000)
    parser.add_argument("--n-pcs", type=int, default=30)
    parser.add_argument("--n-splits", type=int, default=2)
    parser.add_argument("--min-model-confidence", type=float, default=0.60)
    parser.add_argument("--min-marker-margin", type=float, default=0.05)
    parser.add_argument("--pseudo-label-weight", type=float, default=0.50)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def dense_float32(matrix) -> np.ndarray:
    if sparse.issparse(matrix):
        return matrix.toarray().astype(np.float32, copy=False)
    return np.asarray(matrix, dtype=np.float32)


def select_shared_hvgs(root: ad.AnnData, second: ad.AnnData, n_top_hvgs: int) -> list[str]:
    shared_genes = root.var_names.intersection(second.var_names)
    if len(shared_genes) < 100:
        raise ValueError(f"Only {len(shared_genes)} shared genes were found between the two root datasets.")

    root_shared = root[:, shared_genes].copy()
    import scanpy as sc

    sc.pp.highly_variable_genes(
        root_shared,
        n_top_genes=min(n_top_hvgs, root_shared.n_vars),
        flavor="seurat",
    )
    genes = root_shared.var_names[root_shared.var["highly_variable"]].astype(str).tolist()
    if len(genes) < 100:
        raise ValueError(f"Only {len(genes)} shared highly variable genes were selected.")
    return genes


def load_fixed_features(
    path: Path,
    column: str,
    root: ad.AnnData,
    second: ad.AnnData,
) -> list[str]:
    feature_table = pd.read_csv(path)
    if column not in feature_table.columns:
        raise KeyError(f"Feature column {column!r} was not found in {path}")
    requested = feature_table[column].dropna().astype(str).drop_duplicates().tolist()
    shared = set(root.var_names.astype(str)).intersection(second.var_names.astype(str))
    features = [feature for feature in requested if feature in shared]
    if len(features) < 20:
        raise ValueError(f"Only {len(features)} fixed features were shared by both datasets.")
    return features


def build_models(n_pcs: int, random_state: int) -> dict[str, Pipeline]:
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("scale", StandardScaler()),
                ("pca", PCA(n_components=n_pcs, random_state=random_state)),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=3000,
                        class_weight="balanced",
                        random_state=random_state,
                    ),
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


def evaluate_grouped_cv(
    x: np.ndarray,
    labels: np.ndarray,
    groups: np.ndarray,
    models: dict[str, Pipeline],
    n_splits: int,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    group_label_table = pd.DataFrame({"group": groups, "label": labels}).drop_duplicates()
    groups_per_label = group_label_table.groupby("label")["group"].nunique()
    if (groups_per_label < n_splits).any():
        limiting = groups_per_label[groups_per_label < n_splits].to_dict()
        raise ValueError(
            f"n_splits={n_splits} exceeds the number of independent clusters for one or more labels: {limiting}"
        )
    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    metric_rows: list[dict[str, object]] = []
    prediction_rows: list[dict[str, object]] = []

    for fold, (train_index, test_index) in enumerate(splitter.split(x, labels, groups), start=1):
        held_out_clusters = sorted(set(groups[test_index]))
        for model_name, model_template in models.items():
            model = clone(model_template)
            model.fit(x[train_index], labels[train_index])
            predictions = model.predict(x[test_index])
            probabilities = model.predict_proba(x[test_index])
            confidence = probabilities.max(axis=1)
            class_order = model.named_steps["classifier"].classes_

            metric_rows.append(
                {
                    "model": model_name,
                    "fold": fold,
                    "n_train_cells": len(train_index),
                    "n_test_cells": len(test_index),
                    "held_out_clusters": ",".join(map(str, held_out_clusters)),
                    "accuracy": accuracy_score(labels[test_index], predictions),
                    "balanced_accuracy": balanced_accuracy_score(labels[test_index], predictions),
                    "macro_f1": f1_score(labels[test_index], predictions, average="macro", zero_division=0),
                    "log_loss": log_loss(labels[test_index], probabilities, labels=class_order),
                    "mean_confidence": confidence.mean(),
                }
            )

            for position, cell_index in enumerate(test_index):
                prediction_row = {
                    "model": model_name,
                    "fold": fold,
                    "cell_index": int(cell_index),
                    "cluster": str(groups[cell_index]),
                    "true_pseudo_label": str(labels[cell_index]),
                    "predicted_label": str(predictions[position]),
                    "confidence": float(confidence[position]),
                }
                for class_position, class_label in enumerate(class_order):
                    prediction_row[f"probability__{class_label}"] = float(probabilities[position, class_position])
                prediction_rows.append(prediction_row)

    return pd.DataFrame(metric_rows), pd.DataFrame(prediction_rows)


def expected_calibration_error(predictions: pd.DataFrame, n_bins: int = 10) -> float:
    bins = np.linspace(0, 1, n_bins + 1)
    bin_ids = np.clip(np.digitize(predictions["confidence"], bins, right=True), 1, n_bins)
    correct = predictions["true_pseudo_label"].eq(predictions["predicted_label"]).to_numpy(dtype=float)
    total = len(predictions)
    error = 0.0
    for bin_id in range(1, n_bins + 1):
        mask = bin_ids == bin_id
        if mask.any():
            error += mask.sum() / total * abs(correct[mask].mean() - predictions.loc[mask, "confidence"].mean())
    return float(error)


def apply_temperature(probabilities: np.ndarray, temperature: float) -> np.ndarray:
    clipped = np.clip(np.asarray(probabilities, dtype=float), 1e-8, 1.0)
    scaled = np.exp(np.log(clipped) / temperature)
    return scaled / scaled.sum(axis=1, keepdims=True)


def fit_temperature(probabilities: np.ndarray, true_labels: np.ndarray, classes: list[str]) -> float:
    class_to_position = {label: position for position, label in enumerate(classes)}
    true_positions = np.array([class_to_position[label] for label in true_labels], dtype=int)

    def objective(log_temperature: float) -> float:
        temperature = float(np.exp(log_temperature))
        calibrated = apply_temperature(probabilities, temperature)
        return float(-np.log(calibrated[np.arange(len(true_positions)), true_positions]).mean())

    result = minimize_scalar(objective, bounds=(-3.0, 3.0), method="bounded")
    if not result.success:
        raise RuntimeError(f"Temperature calibration failed: {result.message}")
    return float(np.exp(result.x))


def marker_winners(adata: ad.AnnData) -> pd.DataFrame:
    score_columns = [column for column in adata.obs.columns if column.endswith("_score")]
    if len(score_columns) < 2:
        raise ValueError("At least two program-score columns are required for consensus filtering.")
    scores = adata.obs[score_columns].to_numpy(dtype=float)
    order = np.argsort(scores, axis=1)
    top_index = order[:, -1]
    second_index = order[:, -2]
    programs = np.array([column.removesuffix("_score") for column in score_columns], dtype=object)
    return pd.DataFrame(
        {
            "marker_top_program": programs[top_index],
            "marker_top_score": scores[np.arange(len(scores)), top_index],
            "marker_second_program": programs[second_index],
            "marker_margin": (
                scores[np.arange(len(scores)), top_index] - scores[np.arange(len(scores)), second_index]
            ),
        },
        index=adata.obs_names,
    )


def fit_and_predict(
    model_template: Pipeline,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_target: np.ndarray,
) -> tuple[Pipeline, np.ndarray, np.ndarray]:
    model = clone(model_template)
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_target)
    predictions = model.named_steps["classifier"].classes_[probabilities.argmax(axis=1)]
    return model, predictions, probabilities


def save_confusion_figure(
    predictions: pd.DataFrame,
    labels: list[str],
    output_path: Path,
) -> None:
    model_names = predictions["model"].drop_duplicates().tolist()
    display_labels = [SHORT_PROGRAM_LABELS.get(label, label) for label in labels]
    fig, axes = plt.subplots(1, len(model_names), figsize=(6.5 * len(model_names), 5.5), squeeze=False)
    for axis, model_name in zip(axes[0], model_names, strict=True):
        subset = predictions[predictions["model"] == model_name]
        matrix = confusion_matrix(
            subset["true_pseudo_label"],
            subset["predicted_label"],
            labels=labels,
            normalize="true",
        )
        sns.heatmap(
            matrix,
            annot=True,
            fmt=".2f",
            cmap="Blues",
            vmin=0,
            vmax=1,
            xticklabels=display_labels,
            yticklabels=display_labels,
            ax=axis,
        )
        axis.set_title(model_name.replace("_", " ").title())
        axis.set_xlabel("Predicted pseudo-label")
        axis.set_ylabel("Held-out pseudo-label")
        axis.tick_params(axis="x", rotation=25)
        axis.tick_params(axis="y", rotation=0)
    fig.suptitle("Cluster-held-out root reference benchmark", y=1.02)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def save_metric_figure(summary: pd.DataFrame, output_path: Path) -> None:
    metric_columns = ["accuracy", "balanced_accuracy", "macro_f1"]
    plot_data = summary.melt(
        id_vars="model",
        value_vars=metric_columns,
        var_name="metric",
        value_name="score",
    )
    plt.figure(figsize=(8, 5))
    sns.barplot(data=plot_data, x="metric", y="score", hue="model")
    plt.ylim(0, 1)
    plt.ylabel("Mean cluster-held-out score")
    plt.xlabel("")
    plt.title("Classifier comparison on held-out GSE123818 clusters")
    plt.tight_layout()
    plt.savefig(output_path, dpi=220)
    plt.close()


def save_reliability_figure(predictions: pd.DataFrame, output_path: Path, n_bins: int = 10) -> None:
    bins = np.linspace(0, 1, n_bins + 1)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharex=True, sharey=True)
    for axis, confidence_column, panel_title in zip(
        axes,
        ["confidence", "calibrated_confidence"],
        ["Before temperature scaling", "After temperature scaling"],
        strict=True,
    ):
        for model_name, subset in predictions.groupby("model", sort=False):
            plot_data = subset.copy()
            plot_data["correct"] = plot_data["true_pseudo_label"].eq(plot_data["predicted_label"]).astype(float)
            plot_data["confidence_bin"] = pd.cut(
                plot_data[confidence_column],
                bins=bins,
                include_lowest=True,
                duplicates="drop",
            )
            reliability = (
                plot_data.groupby("confidence_bin", observed=True)
                .agg(
                    mean_confidence=(confidence_column, "mean"),
                    observed_accuracy=("correct", "mean"),
                    n_cells=("correct", "size"),
                )
                .reset_index()
            )
            axis.plot(
                reliability["mean_confidence"],
                reliability["observed_accuracy"],
                marker="o",
                linewidth=2,
                label=model_name.replace("_", " ").title(),
            )
        axis.plot([0, 1], [0, 1], linestyle="--", color="black", label="Perfect calibration")
        axis.set_xlim(0, 1)
        axis.set_ylim(0, 1)
        axis.set_xlabel("Mean predicted confidence")
        axis.set_title(panel_title)
    axes[0].set_ylabel("Observed pseudo-label accuracy")
    axes[1].legend(loc="lower right")
    fig.suptitle("Confidence reliability on held-out clusters", y=1.02)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def save_consensus_figure(predictions: pd.DataFrame, output_path: Path) -> None:
    accepted = predictions[predictions["consensus_accepted"]]
    counts = accepted["consensus_label"].value_counts().rename_axis("program").reset_index(name="n_cells")
    plt.figure(figsize=(9, 5))
    if counts.empty:
        plt.text(0.5, 0.5, "No cells passed consensus filters", ha="center", va="center")
        plt.axis("off")
    else:
        counts["display_program"] = counts["program"].map(SHORT_PROGRAM_LABELS).fillna(counts["program"])
        sns.barplot(data=counts, x="display_program", y="n_cells", color="#4C78A8")
        plt.xticks(rotation=15, ha="right")
        plt.xlabel("Consensus pseudo-label")
        plt.ylabel("GSE121619 cells retained")
    plt.title("Conservative GSE121619 consensus set")
    plt.tight_layout()
    plt.savefig(output_path, dpi=220)
    plt.close()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")

    root = ad.read_h5ad(args.root_reference)
    second = ad.read_h5ad(args.second_root)
    required_root_columns = {"broad_program", "leiden"}
    missing_root_columns = required_root_columns.difference(root.obs.columns)
    if missing_root_columns:
        raise KeyError(f"Root reference is missing required columns: {sorted(missing_root_columns)}")

    if args.feature_list is None:
        selected_genes = select_shared_hvgs(root, second, args.n_top_hvgs)
        feature_selection = "root-derived shared highly variable genes"
    else:
        selected_genes = load_fixed_features(
            args.feature_list,
            args.feature_column,
            root,
            second,
        )
        feature_selection = f"fixed feature list: {args.feature_list}"
    x_root = dense_float32(root[:, selected_genes].X)
    x_second = dense_float32(second[:, selected_genes].X)
    y_root = root.obs["broad_program"].astype(str).to_numpy()
    root_groups = root.obs["leiden"].astype(str).to_numpy()
    labels = sorted(np.unique(y_root).tolist())

    n_pcs = min(args.n_pcs, x_root.shape[0] - 1, x_root.shape[1])
    models = build_models(n_pcs=n_pcs, random_state=args.random_state)
    cv_metrics, cv_predictions = evaluate_grouped_cv(
        x_root,
        y_root,
        root_groups,
        models,
        n_splits=args.n_splits,
        random_state=args.random_state,
    )
    model_summary = (
        cv_metrics.groupby("model", as_index=False)
        .agg(
            accuracy=("accuracy", "mean"),
            balanced_accuracy=("balanced_accuracy", "mean"),
            macro_f1=("macro_f1", "mean"),
            log_loss=("log_loss", "mean"),
            mean_confidence=("mean_confidence", "mean"),
        )
        .sort_values(["balanced_accuracy", "macro_f1"], ascending=False)
    )
    calibration_rows = [
        {
            "model": model_name,
            "expected_calibration_error": expected_calibration_error(subset),
        }
        for model_name, subset in cv_predictions.groupby("model", sort=False)
    ]
    model_summary = model_summary.merge(pd.DataFrame(calibration_rows), on="model", how="left")

    temperature_by_model: dict[str, float] = {}
    calibrated_rows: list[dict[str, object]] = []
    for model_name, subset in cv_predictions.groupby("model", sort=False):
        probability_columns = [f"probability__{label}" for label in labels]
        probabilities = subset[probability_columns].to_numpy(dtype=float)
        temperature = fit_temperature(
            probabilities,
            subset["true_pseudo_label"].astype(str).to_numpy(),
            labels,
        )
        calibrated = apply_temperature(probabilities, temperature)
        calibrated_confidence = calibrated.max(axis=1)
        calibrated_predictions = np.asarray(labels, dtype=object)[calibrated.argmax(axis=1)]
        calibration_frame = pd.DataFrame(
            {
                "true_pseudo_label": subset["true_pseudo_label"].astype(str).to_numpy(),
                "predicted_label": calibrated_predictions,
                "confidence": calibrated_confidence,
            }
        )
        temperature_by_model[model_name] = temperature
        calibrated_rows.append(
            {
                "model": model_name,
                "temperature": temperature,
                "calibrated_log_loss": log_loss(
                    subset["true_pseudo_label"],
                    calibrated,
                    labels=labels,
                ),
                "calibrated_mean_confidence": calibrated_confidence.mean(),
                "calibrated_expected_calibration_error": expected_calibration_error(calibration_frame),
            }
        )
        cv_predictions.loc[subset.index, "calibrated_confidence"] = calibrated_confidence
    model_summary = model_summary.merge(pd.DataFrame(calibrated_rows), on="model", how="left")

    target_predictions = pd.DataFrame(index=second.obs_names)
    fitted_root_models: dict[str, Pipeline] = {}
    for model_name, model_template in models.items():
        fitted_model, predictions, probabilities = fit_and_predict(model_template, x_root, y_root, x_second)
        calibrated_probabilities = apply_temperature(probabilities, temperature_by_model[model_name])
        calibrated_confidence = calibrated_probabilities.max(axis=1)
        fitted_root_models[model_name] = fitted_model
        target_predictions[f"{model_name}_prediction"] = predictions
        target_predictions[f"{model_name}_raw_confidence"] = probabilities.max(axis=1)
        target_predictions[f"{model_name}_confidence"] = calibrated_confidence

    target_predictions = target_predictions.join(marker_winners(second))
    prediction_columns = [f"{model_name}_prediction" for model_name in models]
    confidence_columns = [f"{model_name}_confidence" for model_name in models]
    model_agreement = target_predictions[prediction_columns].nunique(axis=1) == 1
    agreed_prediction = target_predictions[prediction_columns[0]]
    target_predictions["model_agreement"] = model_agreement
    target_predictions["minimum_model_confidence"] = target_predictions[confidence_columns].min(axis=1)
    target_predictions["marker_agreement"] = agreed_prediction == target_predictions["marker_top_program"]
    target_predictions["consensus_accepted"] = (
        target_predictions["model_agreement"]
        & target_predictions["marker_agreement"]
        & (target_predictions["minimum_model_confidence"] >= args.min_model_confidence)
        & (target_predictions["marker_margin"] >= args.min_marker_margin)
    )
    target_predictions["consensus_label"] = np.where(
        target_predictions["consensus_accepted"],
        agreed_prediction,
        "ambiguous",
    )
    target_predictions.insert(0, "cell_barcode", target_predictions.index.astype(str))

    accepted = target_predictions["consensus_accepted"].to_numpy()
    x_augmented = np.vstack([x_root, x_second[accepted]])
    y_augmented = np.concatenate(
        [y_root, target_predictions.loc[accepted, "consensus_label"].astype(str).to_numpy()]
    )
    sample_weights = np.concatenate(
        [np.ones(len(y_root), dtype=float), np.full(accepted.sum(), args.pseudo_label_weight, dtype=float)]
    )
    final_model_paths: dict[str, str] = {}
    for model_name, model_template in models.items():
        final_model = clone(model_template)
        final_model.fit(x_augmented, y_augmented, classifier__sample_weight=sample_weights)
        model_path = args.output_dir / f"{model_name}_root_consensus.joblib"
        joblib.dump(
            {
                "model": final_model,
                "selected_genes": selected_genes,
                "classes": labels,
                "root_reference": str(args.root_reference),
                "second_root": str(args.second_root),
                "pseudo_label_weight": args.pseudo_label_weight,
                "temperature": temperature_by_model[model_name],
            },
            model_path,
            compress=3,
        )
        final_model_paths[model_name] = str(model_path)

    cv_metrics.to_csv(args.output_dir / "cluster_heldout_fold_metrics.csv", index=False)
    cv_predictions.to_csv(args.output_dir / "cluster_heldout_predictions.csv", index=False)
    model_summary.to_csv(args.output_dir / "model_comparison_summary.csv", index=False)
    target_predictions.to_csv(args.output_dir / "gse121619_consensus_predictions.csv", index=False)
    pd.Series(selected_genes, name="selected_gene").to_csv(args.output_dir / "selected_genes.csv", index=False)

    save_confusion_figure(
        cv_predictions,
        labels,
        args.figure_dir / "cluster_heldout_confusion_matrices.png",
    )
    save_metric_figure(model_summary, args.figure_dir / "classifier_metric_comparison.png")
    save_reliability_figure(cv_predictions, args.figure_dir / "classifier_confidence_reliability.png")
    save_consensus_figure(target_predictions, args.figure_dir / "gse121619_consensus_counts.png")

    consensus_counts = target_predictions["consensus_label"].value_counts().to_dict()
    summary = {
        "benchmark_scope": "GSE123818 cluster-held-out pseudo-label benchmark",
        "label_status": "cluster-level marker-derived pseudo-labels; not curated cell-type truth",
        "root_reference": str(args.root_reference),
        "second_root": str(args.second_root),
        "n_root_cells": int(root.n_obs),
        "n_second_root_cells": int(second.n_obs),
        "n_selected_genes": len(selected_genes),
        "feature_selection": feature_selection,
        "n_splits": args.n_splits,
        "root_programs": labels,
        "min_model_confidence": args.min_model_confidence,
        "min_marker_margin": args.min_marker_margin,
        "n_consensus_accepted": int(accepted.sum()),
        "consensus_acceptance_rate": float(accepted.mean()),
        "consensus_label_counts": {str(key): int(value) for key, value in consensus_counts.items()},
        "temperature_by_model": temperature_by_model,
        "model_paths": final_model_paths,
        "validation_warning": (
            "Cross-validation measures recovery of marker-derived cluster pseudo-labels. "
            "It is not an independent estimate of biological cell-type annotation accuracy."
        ),
    }
    with open(args.output_dir / "benchmark_summary.json", "w") as handle:
        json.dump(summary, handle, indent=2)

    print(model_summary.to_string(index=False))
    print(
        f"Accepted {accepted.sum():,}/{second.n_obs:,} GSE121619 cells "
        f"({accepted.mean():.1%}) into the conservative consensus set."
    )
    print(f"Wrote results to {args.output_dir}")
    print(f"Wrote figures to {args.figure_dir}")


if __name__ == "__main__":
    main()
