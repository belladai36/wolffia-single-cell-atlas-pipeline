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

from pipeline_utils import PROJECT_ROOT


DEFAULT_LEAF_LOGISTIC = PROJECT_ROOT / "results" / "leaf_primary_ortholog_model" / "logistic_regression_leaf_primary.joblib"
DEFAULT_LEAF_FOREST = PROJECT_ROOT / "results" / "leaf_primary_ortholog_model" / "random_forest_leaf_primary.joblib"
DEFAULT_ROOT_LOGISTIC = (
    PROJECT_ROOT / "results" / "root_reference_consensus_ortholog_restricted" / "logistic_regression_root_consensus.joblib"
)
DEFAULT_ROOT_FOREST = (
    PROJECT_ROOT / "results" / "root_reference_consensus_ortholog_restricted" / "random_forest_root_consensus.joblib"
)
DEFAULT_TRANSFER_FEATURES = PROJECT_ROOT / "data" / "metadata" / "wolffia_transfer_feature_set.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results" / "combined_wolffia_application"
DEFAULT_FIGURE_DIR = PROJECT_ROOT / "figures" / "combined_wolffia_application"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply the leaf-primary model and root-benchmark model to a Wolffia expression matrix."
    )
    parser.add_argument("input_h5ad", nargs="?", type=Path, help="Normalized/log1p Wolffia h5ad file.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--figure-dir", type=Path, default=DEFAULT_FIGURE_DIR)
    parser.add_argument("--transfer-features", type=Path, default=DEFAULT_TRANSFER_FEATURES)
    parser.add_argument("--leaf-logistic", type=Path, default=DEFAULT_LEAF_LOGISTIC)
    parser.add_argument("--leaf-forest", type=Path, default=DEFAULT_LEAF_FOREST)
    parser.add_argument("--root-logistic", type=Path, default=DEFAULT_ROOT_LOGISTIC)
    parser.add_argument("--root-forest", type=Path, default=DEFAULT_ROOT_FOREST)
    parser.add_argument("--gene-id-column", default=None, help="Optional adata.var column containing Wolffia gene IDs.")
    parser.add_argument(
        "--input-gene-space",
        choices=["wolffia", "arabidopsis"],
        default="wolffia",
        help="Use 'arabidopsis' only for testing with Arabidopsis matrices already named by Arabidopsis gene IDs.",
    )
    parser.add_argument("--min-model-confidence", type=float, default=0.60)
    parser.add_argument("--min-feature-coverage", type=float, default=0.80)
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Run on synthetic Wolffia-like data generated from the ortholog feature table.",
    )
    parser.add_argument("--smoke-test-cells", type=int, default=64)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def dense_float32(matrix) -> np.ndarray:
    if sparse.issparse(matrix):
        return matrix.toarray().astype(np.float32, copy=False)
    return np.asarray(matrix, dtype=np.float32)


def apply_temperature(probabilities: np.ndarray, temperature: float | None) -> np.ndarray:
    if temperature is None:
        return probabilities
    clipped = np.clip(np.asarray(probabilities, dtype=float), 1e-8, 1.0)
    scaled = np.exp(np.log(clipped) / float(temperature))
    return scaled / scaled.sum(axis=1, keepdims=True)


def load_model_pair(logistic_path: Path, forest_path: Path) -> dict[str, dict[str, object]]:
    return {
        "logistic_regression": joblib.load(logistic_path),
        "random_forest": joblib.load(forest_path),
    }


def feature_aliases(adata: ad.AnnData, gene_id_column: str | None) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for name in adata.var_names.astype(str):
        aliases.setdefault(name, name)
    if gene_id_column is not None:
        if gene_id_column not in adata.var.columns:
            raise KeyError(f"Gene ID column {gene_id_column!r} was not found in adata.var.")
        for var_name, gene_id in zip(adata.var_names.astype(str), adata.var[gene_id_column].astype(str), strict=False):
            if gene_id and gene_id.lower() != "nan":
                aliases.setdefault(gene_id, var_name)
    return aliases


def build_feature_matrix(
    adata: ad.AnnData,
    selected_arabidopsis_genes: list[str],
    transfer_table: pd.DataFrame,
    gene_id_column: str | None,
    input_gene_space: str,
) -> tuple[np.ndarray, pd.DataFrame, float]:
    aliases = feature_aliases(adata, gene_id_column)
    transfer_by_arabidopsis = transfer_table.drop_duplicates("arabidopsis_gene_id").set_index("arabidopsis_gene_id")
    columns: list[np.ndarray] = []
    rows: list[dict[str, object]] = []

    for arabidopsis_gene in selected_arabidopsis_genes:
        matched_var_name = None
        matched_by = "missing"
        if input_gene_space == "arabidopsis" and arabidopsis_gene in aliases:
            matched_var_name = aliases[arabidopsis_gene]
            matched_by = "arabidopsis_gene_id"
        elif arabidopsis_gene in transfer_by_arabidopsis.index:
            row = transfer_by_arabidopsis.loc[arabidopsis_gene]
            candidates = [
                str(row.get("wolffia_ncbi_gene_id", "")),
                str(row.get("wolffia_locus_tag", "")),
                str(row.get("wolffia_gene_symbol", "")),
                str(row.get("wolffia_gene_key", "")),
            ]
            for candidate_name, candidate in zip(
                ["wolffia_ncbi_gene_id", "wolffia_locus_tag", "wolffia_gene_symbol", "wolffia_gene_key"],
                candidates,
                strict=True,
            ):
                if candidate and candidate.lower() != "nan" and candidate in aliases:
                    matched_var_name = aliases[candidate]
                    matched_by = candidate_name
                    break
        if matched_var_name is None:
            columns.append(np.zeros(adata.n_obs, dtype=np.float32))
        else:
            values = dense_float32(adata[:, [matched_var_name]].X).ravel()
            columns.append(values)
        rows.append(
            {
                "arabidopsis_gene_id": arabidopsis_gene,
                "matched_input_feature": matched_var_name or "",
                "matched_by": matched_by,
                "present": matched_var_name is not None,
            }
        )

    feature_audit = pd.DataFrame(rows)
    coverage = float(feature_audit["present"].mean()) if len(feature_audit) else 0.0
    return np.column_stack(columns).astype(np.float32, copy=False), feature_audit, coverage


def predict_layer(
    layer_name: str,
    model_pair: dict[str, dict[str, object]],
    x: np.ndarray,
    min_model_confidence: float,
    feature_coverage: float,
    min_feature_coverage: float,
) -> pd.DataFrame:
    predictions = pd.DataFrame(index=np.arange(x.shape[0]))
    for model_name, artifact in model_pair.items():
        model = artifact["model"]
        probabilities = model.predict_proba(x)
        probabilities = apply_temperature(probabilities, artifact.get("temperature"))
        class_order = model.named_steps["classifier"].classes_
        predicted = class_order[probabilities.argmax(axis=1)]
        confidence = probabilities.max(axis=1)
        predictions[f"{layer_name}_{model_name}_prediction"] = predicted
        predictions[f"{layer_name}_{model_name}_confidence"] = confidence

    label_a = predictions[f"{layer_name}_logistic_regression_prediction"]
    label_b = predictions[f"{layer_name}_random_forest_prediction"]
    conf_a = predictions[f"{layer_name}_logistic_regression_confidence"]
    conf_b = predictions[f"{layer_name}_random_forest_confidence"]
    accepted = (
        label_a.eq(label_b)
        & (conf_a >= min_model_confidence)
        & (conf_b >= min_model_confidence)
        & (feature_coverage >= min_feature_coverage)
    )
    predictions[f"{layer_name}_model_agreement"] = label_a.eq(label_b)
    predictions[f"{layer_name}_minimum_confidence"] = np.minimum(conf_a, conf_b)
    predictions[f"{layer_name}_feature_coverage"] = feature_coverage
    predictions[f"{layer_name}_accepted"] = accepted
    predictions[f"{layer_name}_label"] = np.where(accepted, label_a, "ambiguous")
    return predictions


def final_interpretation(row: pd.Series) -> tuple[str, str]:
    leaf_label = str(row["leaf_label"])
    root_label = str(row["root_label"])
    leaf_ok = bool(row["leaf_accepted"])
    root_ok = bool(row["root_accepted"])
    if leaf_ok and root_ok and leaf_label == root_label:
        return leaf_label, "strong_leaf_root_agreement"
    if leaf_ok and not root_ok:
        return leaf_label, "primary_leaf_supported_root_ambiguous"
    if leaf_ok and root_ok and leaf_label != root_label:
        return "review_required", "leaf_root_disagreement"
    if not leaf_ok and root_ok:
        return "ambiguous", "secondary_root_like_signal_only"
    return "ambiguous", "both_models_ambiguous"


def make_smoke_test_adata(transfer_table: pd.DataFrame, n_cells: int, random_state: int) -> ad.AnnData:
    rng = np.random.default_rng(random_state)
    features = (
        transfer_table["wolffia_ncbi_gene_id"]
        .fillna(transfer_table["wolffia_locus_tag"])
        .astype(str)
        .replace("nan", np.nan)
        .dropna()
        .drop_duplicates()
        .tolist()
    )
    if len(features) < 20:
        raise ValueError("Not enough Wolffia feature identifiers are available for smoke-test data.")
    x = rng.lognormal(mean=0.3, sigma=0.8, size=(n_cells, len(features))).astype(np.float32)
    return ad.AnnData(x, var=pd.DataFrame(index=features), obs=pd.DataFrame(index=[f"smoke_cell_{i}" for i in range(n_cells)]))


def save_summary_figure(predictions: pd.DataFrame, output_path: Path) -> None:
    counts = (
        predictions["final_label"]
        .value_counts()
        .rename_axis("final_label")
        .reset_index(name="n_cells")
        .sort_values("n_cells", ascending=False)
    )
    plt.figure(figsize=(9, 5))
    sns.barplot(data=counts, x="final_label", y="n_cells", color="#4C78A8")
    plt.xticks(rotation=30, ha="right")
    plt.xlabel("Final interpretation label")
    plt.ylabel("Cells")
    plt.title("Combined leaf-primary and root-benchmark predictions")
    plt.tight_layout()
    plt.savefig(output_path, dpi=220)
    plt.close()


def main() -> None:
    args = parse_args()
    if args.input_h5ad is None and not args.smoke_test:
        raise SystemExit("Provide input_h5ad or use --smoke-test.")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")

    transfer_table = pd.read_csv(args.transfer_features)
    leaf_pair = load_model_pair(args.leaf_logistic, args.leaf_forest)
    root_pair = load_model_pair(args.root_logistic, args.root_forest)
    leaf_features = list(leaf_pair["logistic_regression"]["selected_genes"])
    root_features = list(root_pair["logistic_regression"]["selected_genes"])
    if leaf_features != root_features:
        raise ValueError("Leaf and root model feature orders differ; combined application is unsafe.")

    if args.smoke_test:
        adata = make_smoke_test_adata(transfer_table, args.smoke_test_cells, args.random_state)
        input_label = "synthetic_smoke_test"
    else:
        adata = ad.read_h5ad(args.input_h5ad)
        input_label = str(args.input_h5ad)

    x, feature_audit, feature_coverage = build_feature_matrix(
        adata,
        leaf_features,
        transfer_table,
        args.gene_id_column,
        args.input_gene_space,
    )
    leaf_predictions = predict_layer(
        "leaf",
        leaf_pair,
        x,
        args.min_model_confidence,
        feature_coverage,
        args.min_feature_coverage,
    )
    root_predictions = predict_layer(
        "root",
        root_pair,
        x,
        args.min_model_confidence,
        feature_coverage,
        args.min_feature_coverage,
    )
    predictions = pd.concat([leaf_predictions, root_predictions], axis=1)
    final_pairs = predictions.apply(final_interpretation, axis=1, result_type="expand")
    predictions["final_label"] = final_pairs[0].to_numpy()
    predictions["final_interpretation_status"] = final_pairs[1].to_numpy()
    predictions.insert(0, "cell_id", adata.obs_names.astype(str))

    feature_audit.to_csv(args.output_dir / "combined_feature_coverage_audit.csv", index=False)
    predictions.to_csv(args.output_dir / "combined_leaf_root_predictions.csv", index=False)
    save_summary_figure(predictions, args.figure_dir / "combined_final_label_counts.png")

    summary = {
        "input": input_label,
        "n_cells": int(adata.n_obs),
        "n_transfer_features": int(len(leaf_features)),
        "feature_coverage": feature_coverage,
        "min_model_confidence": args.min_model_confidence,
        "min_feature_coverage": args.min_feature_coverage,
        "leaf_acceptance_rate": float(predictions["leaf_accepted"].mean()),
        "root_acceptance_rate": float(predictions["root_accepted"].mean()),
        "final_label_counts": {str(k): int(v) for k, v in predictions["final_label"].value_counts().to_dict().items()},
        "final_status_counts": {
            str(k): int(v) for k, v in predictions["final_interpretation_status"].value_counts().to_dict().items()
        },
        "interpretation_warning": (
            "Final labels are provisional transfer predictions. Biological annotation still requires "
            "marker-module, cluster-level, QC, and dataset-reproducibility support."
        ),
    }
    with open(args.output_dir / "combined_application_summary.json", "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(json.dumps(summary, indent=2))
    print(f"Wrote predictions to {args.output_dir / 'combined_leaf_root_predictions.csv'}")
    print(f"Wrote figure to {args.figure_dir / 'combined_final_label_counts.png'}")


if __name__ == "__main__":
    main()
