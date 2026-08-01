#!/usr/bin/env python3
"""Score a future Wolffia dataset with the trusted native marker panel.

This script is intended for future control-vs-treatment datasets, including
salt-stress experiments. It expects a normalized/log1p AnnData file with
Waus8730 gene IDs in ``adata.var_names`` or in a specified ``adata.var`` column.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_PANEL = Path("data/metadata/wolffia_trusted_native_marker_panel.csv")


def import_anndata():
    try:
        import anndata as ad
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: anndata. Run this script in the project single-cell "
            "Python environment, such as the py311/scanpy environment."
        ) from exc
    return ad


def expression_vector(adata, genes: list[str]) -> np.ndarray:
    """Return mean expression across present genes for each cell."""
    present = [gene for gene in genes if gene in adata.var_names]
    if not present:
        return np.full(adata.n_obs, np.nan)
    X = adata[:, present].X
    if hasattr(X, "toarray"):
        return np.asarray(X.mean(axis=1)).ravel()
    return np.asarray(X).mean(axis=1)


def attach_metadata(adata, metadata_path: Path | None, cell_id_column: str | None):
    """Join optional sample/cell metadata into adata.obs."""
    if metadata_path is None:
        return adata

    metadata = pd.read_csv(metadata_path)
    if cell_id_column:
        if cell_id_column not in metadata.columns:
            raise ValueError(f"Metadata file does not contain cell-id column: {cell_id_column}")
        metadata = metadata.set_index(cell_id_column)
    else:
        metadata = metadata.set_index(metadata.columns[0])

    adata.obs = adata.obs.join(metadata, how="left", rsuffix="_metadata")
    return adata


def score_programs(adata, panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Score every trusted native program and return cell/program tables."""
    cell_scores = adata.obs.copy()
    coverage_rows = []

    for program_id, sub in panel.groupby("native_program_id"):
        program_name = sub["native_program_name"].iloc[0]
        genes = sorted(sub["waus8730_gene_id"].dropna().unique())
        present = [gene for gene in genes if gene in adata.var_names]
        score = expression_vector(adata, genes)
        score_col = f"trusted_score_{program_id}"
        cell_scores[score_col] = score

        coverage_rows.append(
            {
                "native_program_id": program_id,
                "native_program_name": program_name,
                "panel_genes": len(genes),
                "genes_present_in_matrix": len(present),
                "coverage_fraction": len(present) / len(genes) if genes else np.nan,
                "missing_genes": ";".join(sorted(set(genes) - set(present))),
            }
        )

    return cell_scores, pd.DataFrame(coverage_rows)


def summarize_scores(
    cell_scores: pd.DataFrame,
    panel: pd.DataFrame,
    group_columns: list[str],
) -> pd.DataFrame:
    """Summarize program scores by selected metadata columns."""
    score_cols = [col for col in cell_scores.columns if col.startswith("trusted_score_")]
    program_names = (
        panel.drop_duplicates("native_program_id")
        .set_index("native_program_id")["native_program_name"]
        .to_dict()
    )

    rows = []
    valid_group_columns = [col for col in group_columns if col in cell_scores.columns]
    if not valid_group_columns:
        valid_group_columns = ["all_cells"]
        cell_scores = cell_scores.copy()
        cell_scores["all_cells"] = "all_cells"

    for group_column in valid_group_columns:
        grouped = cell_scores.groupby(group_column, observed=True, dropna=False)
        for group_value, group_df in grouped:
            for score_col in score_cols:
                program_id = score_col.replace("trusted_score_", "")
                rows.append(
                    {
                        "grouping": group_column,
                        "group": group_value,
                        "native_program_id": program_id,
                        "native_program_name": program_names.get(program_id, program_id),
                        "n_cells": len(group_df),
                        "mean_score": group_df[score_col].mean(),
                        "median_score": group_df[score_col].median(),
                    }
                )
    return pd.DataFrame(rows)


def normalize_gene_ids(adata, gene_id_column: str | None):
    """Optionally replace var_names with a specified gene ID column."""
    if gene_id_column is None:
        return adata
    if gene_id_column not in adata.var.columns:
        raise ValueError(f"adata.var does not contain gene-id column: {gene_id_column}")
    adata.var_names = adata.var[gene_id_column].astype(str)
    return adata


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score a future Wolffia dataset with the trusted native marker panel."
    )
    parser.add_argument("input_h5ad", type=Path, help="Normalized/log1p Wolffia h5ad file.")
    parser.add_argument("--panel", type=Path, default=DEFAULT_PANEL)
    parser.add_argument("--metadata", type=Path, default=None, help="Optional cell metadata CSV.")
    parser.add_argument(
        "--metadata-cell-id-column",
        default=None,
        help="Cell ID column in metadata CSV. Defaults to first column.",
    )
    parser.add_argument(
        "--gene-id-column",
        default=None,
        help="Optional adata.var column to use as Waus8730 gene IDs.",
    )
    parser.add_argument(
        "--group-columns",
        default="condition,sample_id,replicate,cluster,leiden",
        help="Comma-separated obs columns to summarize when present.",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    ad = import_anndata()
    panel = pd.read_csv(args.panel)
    adata = ad.read_h5ad(args.input_h5ad)
    adata = normalize_gene_ids(adata, args.gene_id_column)
    adata = attach_metadata(adata, args.metadata, args.metadata_cell_id_column)

    cell_scores, coverage = score_programs(adata, panel)
    group_columns = [col.strip() for col in args.group_columns.split(",") if col.strip()]
    summary = summarize_scores(cell_scores, panel, group_columns)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    cell_path = args.output_dir / "trusted_native_program_cell_scores.csv"
    coverage_path = args.output_dir / "trusted_native_program_gene_coverage.csv"
    summary_path = args.output_dir / "trusted_native_program_score_summary.csv"

    cell_scores.to_csv(cell_path, index=True, index_label="cell_id")
    coverage.to_csv(coverage_path, index=False)
    summary.to_csv(summary_path, index=False)

    print(f"Wrote: {cell_path}")
    print(f"Wrote: {coverage_path}")
    print(f"Wrote: {summary_path}")
    print(f"Cells scored: {adata.n_obs}")
    print(f"Programs scored: {panel['native_program_id'].nunique()}")
    print("Minimum program coverage:", coverage["coverage_fraction"].min())


if __name__ == "__main__":
    main()
