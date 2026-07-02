#!/usr/bin/env python
"""Compare full and transfer-ready models and audit marker-program coverage."""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/mplconfig")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from pipeline_utils import PROJECT_ROOT


FULL_DIR = PROJECT_ROOT / "results" / "root_reference_consensus"
TRANSFER_DIR = PROJECT_ROOT / "results" / "root_reference_consensus_ortholog_restricted"
ORTHOLOGY_DIR = PROJECT_ROOT / "results" / "orthology"
MARKER_PATH = PROJECT_ROOT / "data" / "metadata" / "wolffia_program_marker_orthologs.csv"
OUTPUT_DIR = PROJECT_ROOT / "results" / "transfer_model_audit"
FIGURE_DIR = PROJECT_ROOT / "figures" / "transfer_model_audit"


def load_benchmark(directory: Path, feature_set: str) -> tuple[pd.DataFrame, dict]:
    metrics = pd.read_csv(directory / "model_comparison_summary.csv")
    metrics.insert(0, "feature_set", feature_set)
    with open(directory / "benchmark_summary.json", encoding="utf-8") as handle:
        summary = json.load(handle)
    return metrics, summary


def classify_marker(row: pd.Series) -> str:
    confidence = str(row.get("mapping_confidence", "unmapped"))
    if confidence in {"high", "medium"}:
        return "transfer_ready"
    if confidence == "low":
        return "family_level_candidate"
    return "unresolved"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")

    full_metrics, full_summary = load_benchmark(FULL_DIR, "Full (2,000 genes)")
    transfer_metrics, transfer_summary = load_benchmark(TRANSFER_DIR, "Transfer-ready (340 genes)")
    metrics = pd.concat([full_metrics, transfer_metrics], ignore_index=True)
    metrics.to_csv(OUTPUT_DIR / "model_metric_comparison.csv", index=False)

    comparison_rows = []
    for model in sorted(metrics["model"].unique()):
        full = full_metrics.loc[full_metrics["model"] == model].iloc[0]
        restricted = transfer_metrics.loc[transfer_metrics["model"] == model].iloc[0]
        for metric in ["accuracy", "balanced_accuracy", "macro_f1", "calibrated_expected_calibration_error"]:
            comparison_rows.append(
                {
                    "model": model,
                    "metric": metric,
                    "full_value": full[metric],
                    "transfer_ready_value": restricted[metric],
                    "absolute_change": restricted[metric] - full[metric],
                }
            )
    comparison = pd.DataFrame(comparison_rows)
    comparison.to_csv(OUTPUT_DIR / "model_performance_changes.csv", index=False)

    consensus = pd.DataFrame(
        [
            {
                "feature_set": "Full (2,000 genes)",
                "accepted_cells": full_summary["n_consensus_accepted"],
                "ambiguous_cells": full_summary["n_second_root_cells"] - full_summary["n_consensus_accepted"],
                "acceptance_rate": full_summary["consensus_acceptance_rate"],
            },
            {
                "feature_set": "Transfer-ready (340 genes)",
                "accepted_cells": transfer_summary["n_consensus_accepted"],
                "ambiguous_cells": transfer_summary["n_second_root_cells"] - transfer_summary["n_consensus_accepted"],
                "acceptance_rate": transfer_summary["consensus_acceptance_rate"],
            },
        ]
    )
    consensus.to_csv(OUTPUT_DIR / "consensus_acceptance_comparison.csv", index=False)

    markers = pd.read_csv(MARKER_PATH)
    markers["transfer_category"] = markers.apply(classify_marker, axis=1)
    marker_columns = [
        "program", "gene", "gene_id", "priority", "notes", "wolffia_ncbi_gene_id",
        "wolffia_gene_symbol", "wolffia_protein_id", "wolffia_product",
        "percent_identity", "query_coverage", "subject_coverage",
        "reciprocal_best_hit", "orthology_status", "mapping_confidence", "transfer_category",
    ]
    markers[marker_columns].to_csv(OUTPUT_DIR / "marker_transfer_audit.csv", index=False)

    coverage = (
        markers.groupby(["program", "transfer_category"]).size().unstack(fill_value=0)
        .reindex(columns=["transfer_ready", "family_level_candidate", "unresolved"], fill_value=0)
    )
    coverage["total_markers"] = coverage.sum(axis=1)
    coverage["transfer_ready_fraction"] = coverage["transfer_ready"] / coverage["total_markers"]
    coverage["candidate_or_better_fraction"] = (
        coverage["transfer_ready"] + coverage["family_level_candidate"]
    ) / coverage["total_markers"]
    coverage.reset_index().to_csv(OUTPUT_DIR / "program_marker_audit.csv", index=False)

    plot_metrics = metrics.melt(
        id_vars=["feature_set", "model"],
        value_vars=["balanced_accuracy", "macro_f1"],
        var_name="metric", value_name="score",
    )
    plot_metrics["model"] = plot_metrics["model"].replace(
        {"logistic_regression": "Logistic regression", "random_forest": "Random forest"}
    )
    plot_metrics["metric"] = plot_metrics["metric"].replace(
        {"balanced_accuracy": "Balanced accuracy", "macro_f1": "Macro F1"}
    )
    fig, axes = plt.subplots(1, 3, figsize=(19, 6))
    for axis, model in zip(axes[:2], ["Logistic regression", "Random forest"]):
        subset = plot_metrics.loc[plot_metrics["model"] == model]
        sns.barplot(data=subset, x="metric", y="score", hue="feature_set", ax=axis)
        axis.set_ylim(0, 0.8)
        axis.set_title(model)
        axis.set_xlabel("")
        axis.set_ylabel("Score")
        axis.legend(title="", fontsize=10)
    consensus_plot = consensus.copy()
    consensus_plot["acceptance_percent"] = consensus_plot["acceptance_rate"] * 100
    sns.barplot(data=consensus_plot, x="feature_set", y="acceptance_percent", ax=axes[2], color="#4C78A8")
    axes[2].set_ylim(0, 50)
    axes[2].set_title("Independent-root consensus")
    axes[2].set_ylabel("Accepted cells (%)")
    axes[2].set_xlabel("")
    axes[2].tick_params(axis="x", rotation=12)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "full_vs_transfer_ready_benchmark.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    coverage_plot = coverage.drop(columns=["total_markers", "transfer_ready_fraction", "candidate_or_better_fraction"])
    coverage_plot = coverage_plot.sort_values("transfer_ready", ascending=True)
    coverage_plot.columns = ["Transfer-ready", "Family-level candidate", "Unresolved"]
    ax = coverage_plot.plot(
        kind="barh", stacked=True, figsize=(12, 8),
        color=["#2A9D8F", "#E9C46A", "#D9D9D9"],
    )
    ax.set_title("Wolffia transfer evidence for Arabidopsis program markers")
    ax.set_xlabel("Number of markers")
    ax.set_ylabel("")
    ax.legend(title="", loc="lower right")
    ax.figure.tight_layout()
    ax.figure.savefig(FIGURE_DIR / "program_marker_transfer_audit.png", dpi=300, bbox_inches="tight")
    plt.close(ax.figure)

    print(f"Wrote audit tables to {OUTPUT_DIR}")
    print(f"Wrote audit figures to {FIGURE_DIR}")


if __name__ == "__main__":
    main()
