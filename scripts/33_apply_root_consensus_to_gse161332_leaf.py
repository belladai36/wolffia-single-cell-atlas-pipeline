#!/usr/bin/env python
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import scipy.io

from pipeline_utils import project_path


def read_barcodes(path: Path) -> list[str]:
    with gzip.open(path, "rt") as handle:
        return [line.strip() for line in handle if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply the frozen root-consensus 340-feature model directly to GSE161332 leaf matrix files."
    )
    parser.add_argument("--raw-dir", default="data/public_references/raw/GSE161332")
    parser.add_argument("--model-dir", default="results/root_reference_consensus_ortholog_restricted")
    parser.add_argument("--output-dir", default="results/gse161332_leaf_transfer_test")
    parser.add_argument("--min-confidence", type=float, default=0.60)
    parser.add_argument("--min-feature-coverage", type=float, default=0.80)
    args = parser.parse_args()

    raw_dir = project_path(args.raw_dir)
    model_dir = project_path(args.model_dir)
    output_dir = project_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    features = pd.read_csv(raw_dir / "GSE161332_features.tsv.gz", sep="\t", header=None, compression="gzip")
    features = features.iloc[:, :2].copy()
    features.columns = ["gene_id", "gene_name"]
    features["gene_id"] = features["gene_id"].astype(str)
    features["gene_name"] = features["gene_name"].astype(str)

    barcodes = read_barcodes(raw_dir / "GSE161332_barcodes.tsv.gz")

    logistic_artifact = joblib.load(model_dir / "logistic_regression_root_consensus.joblib")
    random_forest_artifact = joblib.load(model_dir / "random_forest_root_consensus.joblib")
    selected_genes = [str(gene) for gene in logistic_artifact["selected_genes"]]

    if selected_genes != [str(gene) for gene in random_forest_artifact["selected_genes"]]:
        raise ValueError("Logistic-regression and random-forest artifacts do not use the same feature order.")

    feature_index = {gene_id: idx for idx, gene_id in enumerate(features["gene_id"])}
    present_genes = [gene for gene in selected_genes if gene in feature_index]
    feature_coverage = len(present_genes) / len(selected_genes)

    matrix = scipy.io.mmread(raw_dir / "GSE161332_matrix.mtx.gz").tocsr().astype(np.float32)
    if matrix.shape != (features.shape[0], len(barcodes)):
        raise ValueError(
            f"Matrix shape {matrix.shape} does not match feature/cell counts {(features.shape[0], len(barcodes))}."
        )

    cell_sums = np.asarray(matrix.sum(axis=0)).ravel().astype(np.float32)
    cell_sums[cell_sums == 0] = 1.0
    scale = 10000.0 / cell_sums

    rows = [feature_index[gene] for gene in present_genes]
    leaf_features = matrix[rows, :].transpose().tocsr()
    leaf_features = leaf_features.multiply(scale[:, None])
    leaf_features.data = np.log1p(leaf_features.data)
    leaf_features = leaf_features.tocsr()

    present_column = {gene: idx for idx, gene in enumerate(present_genes)}
    x_model = np.zeros((len(barcodes), len(selected_genes)), dtype=np.float32)
    for col_idx, gene in enumerate(selected_genes):
        if gene in present_column:
            x_model[:, col_idx] = np.asarray(leaf_features[:, present_column[gene]].toarray()).ravel()

    logistic_model = logistic_artifact["model"]
    random_forest_model = random_forest_artifact["model"]

    logistic_prediction = logistic_model.predict(x_model)
    random_forest_prediction = random_forest_model.predict(x_model)
    logistic_confidence = logistic_model.predict_proba(x_model).max(axis=1)
    random_forest_confidence = random_forest_model.predict_proba(x_model).max(axis=1)

    models_agree = logistic_prediction == random_forest_prediction
    accepted = (
        models_agree
        & (logistic_confidence >= args.min_confidence)
        & (random_forest_confidence >= args.min_confidence)
        & (feature_coverage >= args.min_feature_coverage)
    )
    consensus_prediction = np.where(accepted, logistic_prediction, "ambiguous")

    prediction_df = pd.DataFrame(
        {
            "cell_id": barcodes,
            "logistic_prediction": logistic_prediction,
            "logistic_confidence": logistic_confidence,
            "random_forest_prediction": random_forest_prediction,
            "random_forest_confidence": random_forest_confidence,
            "models_agree": models_agree,
            "consensus_prediction": consensus_prediction,
        }
    )
    prediction_df.to_csv(output_dir / "gse161332_leaf_consensus_predictions.csv", index=False)

    consensus_counts = (
        prediction_df["consensus_prediction"].value_counts().rename_axis("consensus_prediction").reset_index(name="n_cells")
    )
    consensus_counts["fraction"] = consensus_counts["n_cells"] / len(prediction_df)
    consensus_counts.to_csv(output_dir / "gse161332_leaf_consensus_counts.csv", index=False)

    individual_counts = pd.DataFrame(
        {
            "logistic": pd.Series(logistic_prediction).value_counts(),
            "random_forest": pd.Series(random_forest_prediction).value_counts(),
        }
    ).fillna(0).astype(int)
    individual_counts.to_csv(output_dir / "gse161332_leaf_individual_model_counts.csv")

    feature_coverage_df = pd.DataFrame(
        {
            "selected_gene": selected_genes,
            "present_in_gse161332": [gene in feature_index for gene in selected_genes],
        }
    )
    feature_coverage_df.to_csv(output_dir / "gse161332_leaf_feature_coverage.csv", index=False)

    summary = {
        "dataset": "GSE161332",
        "n_cells": len(barcodes),
        "n_genes": int(features.shape[0]),
        "n_selected_features": len(selected_genes),
        "n_present_features": len(present_genes),
        "feature_coverage": feature_coverage,
        "coverage_requirement": args.min_feature_coverage,
        "coverage_passes": feature_coverage >= args.min_feature_coverage,
        "n_models_agree": int(models_agree.sum()),
        "model_agreement_rate": float(models_agree.mean()),
        "n_consensus_accepted": int(accepted.sum()),
        "consensus_acceptance_rate": float(accepted.mean()),
        "consensus_counts": {
            str(row["consensus_prediction"]): int(row["n_cells"]) for _, row in consensus_counts.iterrows()
        },
        "individual_model_counts": {
            column: {str(label): int(value) for label, value in individual_counts[column].items()}
            for column in individual_counts.columns
        },
        "median_logistic_confidence": float(np.median(logistic_confidence)),
        "median_random_forest_confidence": float(np.median(random_forest_confidence)),
    }

    (output_dir / "gse161332_leaf_transfer_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
