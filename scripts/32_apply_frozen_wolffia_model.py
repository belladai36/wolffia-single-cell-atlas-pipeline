#!/usr/bin/env python
"""Apply the frozen v1 model to a normalized/log-transformed Wolffia AnnData object."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import anndata as ad
import joblib
import numpy as np
import pandas as pd
from scipy import sparse

from pipeline_utils import PROJECT_ROOT


MODEL_DIR = PROJECT_ROOT / "results" / "root_reference_consensus_ortholog_restricted"
MAPPING_PATH = PROJECT_ROOT / "data" / "metadata" / "wolffia_transfer_feature_set.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_h5ad", type=Path)
    parser.add_argument("output_h5ad", type=Path)
    parser.add_argument("--gene-id-column", default=None, help="adata.var column containing NCBI gene IDs; defaults to var_names")
    parser.add_argument("--min-feature-coverage", type=float, default=0.80)
    parser.add_argument("--min-confidence", type=float, default=0.60)
    return parser.parse_args()


def calibrate(probabilities: np.ndarray, temperature: float) -> np.ndarray:
    clipped = np.clip(np.asarray(probabilities, dtype=float), 1e-8, 1.0)
    scaled = np.exp(np.log(clipped) / temperature)
    return scaled / scaled.sum(axis=1, keepdims=True)


def main() -> None:
    args = parse_args()
    adata = ad.read_h5ad(args.input_h5ad)
    mapping = pd.read_csv(MAPPING_PATH)
    gene_ids = adata.var_names.astype(str) if args.gene_id_column is None else adata.var[args.gene_id_column].astype(str)
    if gene_ids.duplicated().any():
        raise ValueError("Wolffia gene identifiers must be unique before transfer.")
    input_position = pd.Series(np.arange(adata.n_vars), index=gene_ids)
    requested = mapping["wolffia_ncbi_gene_id"].astype(str)
    present = requested.isin(input_position.index)
    coverage = float(present.mean())
    if coverage < args.min_feature_coverage:
        raise ValueError(f"Only {coverage:.1%} of frozen features are present; require {args.min_feature_coverage:.1%}.")

    x = np.zeros((adata.n_obs, len(mapping)), dtype=np.float32)
    target_columns = np.flatnonzero(present.to_numpy())
    source_columns = input_position.loc[requested[present]].to_numpy(dtype=int)
    values = adata.X[:, source_columns]
    x[:, target_columns] = values.toarray() if sparse.issparse(values) else np.asarray(values)

    outputs = pd.DataFrame(index=adata.obs_names)
    for name in ("logistic_regression", "random_forest"):
        artifact = joblib.load(MODEL_DIR / f"{name}_root_consensus.joblib")
        if artifact["selected_genes"] != mapping["arabidopsis_gene_id"].astype(str).tolist():
            raise ValueError(f"{name} feature order does not match the frozen mapping table.")
        probabilities = calibrate(artifact["model"].predict_proba(x), artifact["temperature"])
        classes = np.asarray(artifact["classes"], dtype=object)
        outputs[f"{name}_prediction"] = classes[probabilities.argmax(axis=1)]
        outputs[f"{name}_confidence"] = probabilities.max(axis=1)
    outputs["model_agreement"] = outputs["logistic_regression_prediction"].eq(outputs["random_forest_prediction"])
    outputs["minimum_model_confidence"] = outputs[["logistic_regression_confidence", "random_forest_confidence"]].min(axis=1)
    outputs["transfer_accepted"] = outputs["model_agreement"] & outputs["minimum_model_confidence"].ge(args.min_confidence)
    outputs["transfer_program_v1"] = np.where(outputs["transfer_accepted"], outputs["logistic_regression_prediction"], "ambiguous")
    for column in outputs:
        adata.obs[column] = outputs[column]
    adata.uns["wolffia_transfer_model_v1"] = {
        "feature_coverage": coverage,
        "n_features_present": int(present.sum()),
        "n_features_required": len(mapping),
        "minimum_confidence": args.min_confidence,
        "marker_support_required_for_high_confidence_biological_annotation": True,
        "input_scale_requirement": "normalized and log1p-transformed expression compatible with training references",
    }
    args.output_h5ad.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(args.output_h5ad)
    summary_path = args.output_h5ad.with_suffix(".transfer_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump({
            "feature_coverage": coverage,
            "accepted_cells": int(outputs["transfer_accepted"].sum()),
            "total_cells": adata.n_obs,
            "label_counts": outputs["transfer_program_v1"].value_counts().to_dict(),
        }, handle, indent=2)
    print(f"Wrote {args.output_h5ad}")


if __name__ == "__main__":
    main()
