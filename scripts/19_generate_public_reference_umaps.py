#!/usr/bin/env python
from __future__ import annotations

import argparse
import os
from pathlib import Path

os.environ.setdefault("NUMBA_CACHE_DIR", "/private/tmp/numba-cache")
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/mplconfig")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import seaborn as sns
from scipy import sparse


def ensure_log_space_and_umap(adata: sc.AnnData, n_top_hvgs: int, n_pcs: int, n_neighbors: int, random_state: int) -> sc.AnnData:
    adata = adata.copy()
    if "counts" in adata.layers:
        adata.X = adata.layers["counts"].copy()

    if sparse.issparse(adata.X):
        adata.X = adata.X.tocsr().astype(np.float32)
        counts_per_cell = np.asarray(adata.X.sum(axis=1)).ravel()
        counts_per_cell[counts_per_cell == 0] = 1.0
        scale = np.divide(10000.0, counts_per_cell, dtype=np.float32)
        adata.X = sparse.diags(scale) @ adata.X
        adata.X = adata.X.log1p()
    else:
        adata.X = np.asarray(adata.X, dtype=np.float32)
        counts_per_cell = adata.X.sum(axis=1, keepdims=True)
        counts_per_cell[counts_per_cell == 0] = 1.0
        adata.X = np.log1p((adata.X / counts_per_cell) * 10000.0)

    sc.pp.highly_variable_genes(adata, n_top_genes=min(n_top_hvgs, adata.n_vars), flavor="seurat")
    if "highly_variable" in adata.var:
        adata = adata[:, adata.var["highly_variable"]].copy()
    sc.pp.scale(adata, max_value=10)
    sc.tl.pca(adata, n_comps=min(n_pcs, adata.n_vars, max(2, adata.n_obs - 1)), random_state=random_state)
    sc.pp.neighbors(adata, n_neighbors=min(n_neighbors, max(2, adata.n_obs - 1)), n_pcs=min(n_pcs, adata.obsm["X_pca"].shape[1]))
    sc.tl.umap(adata, random_state=random_state)
    return adata


def save_umap_plot(adata: sc.AnnData, color: str, output_path: Path, title: str) -> None:
    coords = adata.obsm["X_umap"][:, :2]
    plot_df = pd.DataFrame(
        {
            "UMAP1": coords[:, 0],
            "UMAP2": coords[:, 1],
            color: adata.obs[color].astype(str).to_numpy(),
        }
    )
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=plot_df, x="UMAP1", y="UMAP2", hue=color, s=10, linewidth=0)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def process_one(input_path: Path, color: str, output_path: Path, title: str, max_cells: int, n_top_hvgs: int, n_pcs: int, n_neighbors: int, random_state: int) -> None:
    adata = sc.read_h5ad(input_path)
    if color not in adata.obs.columns:
        raise KeyError(f"Column '{color}' not found in {input_path}")
    if max_cells and adata.n_obs > max_cells:
        sc.pp.subsample(adata, n_obs=max_cells, random_state=random_state, copy=False)
    adata = ensure_log_space_and_umap(adata, n_top_hvgs=n_top_hvgs, n_pcs=n_pcs, n_neighbors=n_neighbors, random_state=random_state)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_umap_plot(adata, color=color, output_path=output_path, title=title)
    print(f"Wrote {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate standalone UMAP figures from scored public-reference h5ad outputs.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--color", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--max-cells", type=int, default=1500)
    parser.add_argument("--n-top-hvgs", type=int, default=2000)
    parser.add_argument("--n-pcs", type=int, default=30)
    parser.add_argument("--n-neighbors", type=int, default=15)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    process_one(
        input_path=Path(args.input),
        color=args.color,
        output_path=Path(args.output),
        title=args.title,
        max_cells=args.max_cells,
        n_top_hvgs=args.n_top_hvgs,
        n_pcs=args.n_pcs,
        n_neighbors=args.n_neighbors,
        random_state=args.random_state,
    )


if __name__ == "__main__":
    main()
