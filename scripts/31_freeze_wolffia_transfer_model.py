#!/usr/bin/env python
"""Freeze and stress-test the provisional Arabidopsis-to-Wolffia transfer model."""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/mplconfig")

import anndata as ad
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, f1_score

from pipeline_utils import PROJECT_ROOT


MODEL_DIR = PROJECT_ROOT / "results" / "root_reference_consensus_ortholog_restricted"
MAPPING_PATH = PROJECT_ROOT / "data" / "metadata" / "wolffia_transfer_feature_set.csv"
MARKER_PATH = PROJECT_ROOT / "data" / "metadata" / "wolffia_program_marker_orthologs.csv"
ROOT_PATH = (
    PROJECT_ROOT
    / "results"
    / "public_reference_gse123818_wt_train_to_gse121619"
    / "train_reference_scored.h5ad"
)
OUTPUT_DIR = PROJECT_ROOT / "results" / "final_wolffia_transfer_model"
FIGURE_DIR = PROJECT_ROOT / "figures" / "final_wolffia_transfer_model"

MODEL_FILES = {
    "logistic_regression": MODEL_DIR / "logistic_regression_root_consensus.joblib",
    "random_forest": MODEL_DIR / "random_forest_root_consensus.joblib",
}
CONFIDENCE_THRESHOLD = 0.60
MIN_GLOBAL_FEATURE_COVERAGE = 0.80
RANDOM_STATE = 42


def calibrate(probabilities: np.ndarray, temperature: float) -> np.ndarray:
    clipped = np.clip(np.asarray(probabilities, dtype=float), 1e-8, 1.0)
    scaled = np.exp(np.log(clipped) / temperature)
    return scaled / scaled.sum(axis=1, keepdims=True)


def load_oof_ensemble() -> pd.DataFrame:
    predictions = pd.read_csv(MODEL_DIR / "cluster_heldout_predictions.csv")
    keys = ["fold", "cell_index", "cluster", "true_pseudo_label"]
    frames = []
    for model_name in MODEL_FILES:
        subset = predictions.loc[predictions["model"] == model_name].copy()
        frames.append(
            subset[keys + ["predicted_label", "calibrated_confidence"]].rename(
                columns={
                    "predicted_label": f"{model_name}_prediction",
                    "calibrated_confidence": f"{model_name}_confidence",
                }
            )
        )
    return frames[0].merge(frames[1], on=keys, validate="one_to_one")


def threshold_audit(ensemble: pd.DataFrame) -> pd.DataFrame:
    rows = []
    lr_label = ensemble["logistic_regression_prediction"]
    rf_label = ensemble["random_forest_prediction"]
    for threshold in np.round(np.arange(0.45, 0.76, 0.05), 2):
        accepted = (
            lr_label.eq(rf_label)
            & ensemble["logistic_regression_confidence"].ge(threshold)
            & ensemble["random_forest_confidence"].ge(threshold)
        )
        truth = ensemble.loc[accepted, "true_pseudo_label"]
        predicted = lr_label.loc[accepted]
        rows.append(
            {
                "confidence_threshold": threshold,
                "n_cells": len(ensemble),
                "n_accepted": int(accepted.sum()),
                "acceptance_rate": float(accepted.mean()),
                "selective_accuracy": float(truth.eq(predicted).mean()),
                "selective_balanced_accuracy": float(balanced_accuracy_score(truth, predicted)),
                "selective_macro_f1": float(f1_score(truth, predicted, average="macro", zero_division=0)),
            }
        )
    return pd.DataFrame(rows)


def predict_pair(x: np.ndarray, artifacts: dict[str, dict]) -> pd.DataFrame:
    result = pd.DataFrame(index=np.arange(x.shape[0]))
    for model_name, artifact in artifacts.items():
        raw = artifact["model"].predict_proba(x)
        probabilities = calibrate(raw, artifact["temperature"])
        classes = np.asarray(artifact["classes"], dtype=object)
        result[f"{model_name}_prediction"] = classes[probabilities.argmax(axis=1)]
        result[f"{model_name}_confidence"] = probabilities.max(axis=1)
    result["model_agreement"] = result["logistic_regression_prediction"].eq(
        result["random_forest_prediction"]
    )
    result["minimum_model_confidence"] = result[
        ["logistic_regression_confidence", "random_forest_confidence"]
    ].min(axis=1)
    result["accepted"] = result["model_agreement"] & result["minimum_model_confidence"].ge(
        CONFIDENCE_THRESHOLD
    )
    result["consensus_label"] = np.where(
        result["accepted"], result["logistic_regression_prediction"], "ambiguous"
    )
    return result


def synthetic_stress_test(artifacts: dict[str, dict]) -> pd.DataFrame:
    root = ad.read_h5ad(ROOT_PATH)
    genes = artifacts["logistic_regression"]["selected_genes"]
    if genes != artifacts["random_forest"]["selected_genes"]:
        raise ValueError("The two final models do not use the same ordered feature set.")

    rng = np.random.default_rng(RANDOM_STATE)
    sampled = []
    for _, positions in root.obs.groupby("broad_program", observed=True).indices.items():
        positions = np.asarray(positions)
        sampled.extend(rng.choice(positions, size=min(200, len(positions)), replace=False).tolist())
    sampled = np.asarray(sorted(sampled))
    matrix = root[sampled, genes].X
    x = matrix.toarray().astype(np.float32) if hasattr(matrix, "toarray") else np.asarray(matrix, dtype=np.float32)
    truth = root.obs.iloc[sampled]["broad_program"].astype(str).to_numpy()

    scenarios = [("baseline", 0.0, 0.0)]
    scenarios.extend((f"feature_dropout_{int(dropout * 100)}pct", dropout, 0.0) for dropout in (0.10, 0.25, 0.40))
    scenarios.extend((f"gaussian_noise_{noise:.2f}sd", 0.0, noise) for noise in (0.10, 0.25, 0.50))
    rows = []
    feature_sd = np.std(x, axis=0, ddof=0)
    for scenario, dropout, noise in scenarios:
        replicates = 1 if scenario == "baseline" else 10
        for replicate in range(replicates):
            perturbed = x.copy()
            if dropout:
                missing = rng.choice(x.shape[1], size=round(dropout * x.shape[1]), replace=False)
                perturbed[:, missing] = 0.0
            if noise:
                perturbation = rng.normal(0.0, noise, size=perturbed.shape) * feature_sd
                perturbed = np.clip(perturbed + perturbation, a_min=0.0, a_max=None).astype(np.float32)
            predicted = predict_pair(perturbed, artifacts)
            accepted = predicted["accepted"].to_numpy()
            accepted_truth = truth[accepted]
            accepted_labels = predicted.loc[accepted, "consensus_label"].to_numpy()
            rows.append(
                {
                    "scenario": scenario,
                    "replicate": replicate + 1,
                    "feature_dropout_fraction": dropout,
                    "noise_sd_fraction": noise,
                    "n_cells": len(truth),
                    "n_accepted": int(accepted.sum()),
                    "acceptance_rate": float(accepted.mean()),
                    "selective_accuracy": float(np.mean(accepted_truth == accepted_labels)) if accepted.any() else np.nan,
                    "ambiguous_rate": float(1.0 - accepted.mean()),
                }
            )
    return pd.DataFrame(rows)


def marker_evidence_table(selected_genes: list[str]) -> pd.DataFrame:
    markers = pd.read_csv(MARKER_PATH)
    category = markers["mapping_confidence"].map(
        {"high": "strict_transfer_ready", "medium": "strict_transfer_ready", "low": "family_review_only"}
    )
    markers["frozen_use"] = category.fillna("unresolved_excluded")
    markers["classifier_feature"] = markers["gene_id"].astype(str).isin(set(selected_genes))
    markers["permitted_use"] = markers["frozen_use"].map(
        {
            "strict_transfer_ready": "independent marker-module support",
            "family_review_only": "manual family-aware interpretation only",
            "unresolved_excluded": "excluded until new evidence exists",
        }
    )
    return markers


def make_figure(thresholds: pd.DataFrame, robustness: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    axes[0].plot(thresholds["acceptance_rate"], thresholds["selective_accuracy"], marker="o")
    chosen = thresholds.loc[thresholds["confidence_threshold"].eq(CONFIDENCE_THRESHOLD)].iloc[0]
    axes[0].scatter(chosen["acceptance_rate"], chosen["selective_accuracy"], s=120, color="#D55E00")
    axes[0].annotate("Frozen: 0.60", (chosen["acceptance_rate"], chosen["selective_accuracy"]), xytext=(8, -18), textcoords="offset points")
    axes[0].set(xlabel="Accepted fraction", ylabel="Accuracy among accepted cells", title="Held-out threshold tradeoff", xlim=(0, 0.7), ylim=(0.75, 1.01))

    summary = robustness.groupby("scenario", sort=False).agg(
        acceptance=("acceptance_rate", "mean"), accuracy=("selective_accuracy", "mean")
    )
    axes[1].scatter(summary["acceptance"], summary["accuracy"], s=70)
    for label, row in summary.iterrows():
        axes[1].annotate(label.replace("_", " "), (row["acceptance"], row["accuracy"]), xytext=(5, 3), textcoords="offset points", fontsize=8)
    axes[1].set(xlabel="Accepted fraction", ylabel="Accuracy among accepted cells", title="Synthetic perturbation stress test", xlim=(0, 0.7), ylim=(0.70, 1.01))
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "frozen_model_validation.png", dpi=250, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = {name: joblib.load(path) for name, path in MODEL_FILES.items()}
    mapping = pd.read_csv(MAPPING_PATH)
    selected_genes = artifacts["logistic_regression"]["selected_genes"]
    if mapping["arabidopsis_gene_id"].astype(str).tolist() != selected_genes:
        raise ValueError("Frozen mapping order does not match the trained model feature order.")

    thresholds = threshold_audit(load_oof_ensemble())
    thresholds.to_csv(OUTPUT_DIR / "confidence_threshold_audit.csv", index=False)
    robustness = synthetic_stress_test(artifacts)
    robustness.to_csv(OUTPUT_DIR / "synthetic_robustness.csv", index=False)
    marker_evidence_table(selected_genes).to_csv(OUTPUT_DIR / "frozen_marker_evidence.csv", index=False)
    make_figure(thresholds, robustness)

    chosen = thresholds.loc[thresholds["confidence_threshold"].eq(CONFIDENCE_THRESHOLD)].iloc[0]
    manifest = {
        "model_name": "Wolffia coarse-program transfer model v1",
        "status": "provisional frozen model pending validation on real Wolffia expression data",
        "feature_policy": "340 high- or medium-confidence one-to-one reciprocal protein mappings",
        "n_features": len(mapping),
        "feature_mapping": str(MAPPING_PATH.relative_to(PROJECT_ROOT)),
        "models": {name: str(path.relative_to(PROJECT_ROOT)) for name, path in MODEL_FILES.items()},
        "programs": artifacts["logistic_regression"]["classes"],
        "decision_rule": {
            "require_logistic_random_forest_agreement": True,
            "minimum_calibrated_confidence_each_model": CONFIDENCE_THRESHOLD,
            "minimum_global_feature_coverage": MIN_GLOBAL_FEATURE_COVERAGE,
            "otherwise": "ambiguous",
            "high_confidence_biological_annotation_also_requires": "independent coherent marker-module support",
        },
        "held_out_pseudo_label_performance_at_frozen_threshold": {
            "acceptance_rate": float(chosen["acceptance_rate"]),
            "selective_accuracy": float(chosen["selective_accuracy"]),
            "selective_balanced_accuracy": float(chosen["selective_balanced_accuracy"]),
            "selective_macro_f1": float(chosen["selective_macro_f1"]),
        },
        "limitations": [
            "Targets are marker-derived Arabidopsis cluster pseudo-labels, not curated Wolffia cell types.",
            "The classifier currently distinguishes only three root-derived coarse programs.",
            "Synthetic perturbations test software behavior and rejection safety, not biological transfer accuracy.",
            "Family-level directional matches are review evidence and are not classifier features.",
            "The model must be re-evaluated after PRJNA1124135 is processed.",
        ],
    }
    with open(OUTPUT_DIR / "final_model_manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
    print(json.dumps(manifest["held_out_pseudo_label_performance_at_frozen_threshold"], indent=2))
    print(f"Wrote frozen model audit to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
