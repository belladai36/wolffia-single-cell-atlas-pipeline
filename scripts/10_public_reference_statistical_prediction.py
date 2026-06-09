#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

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


def read_program_markers(path: Path) -> dict[str, list[str]]:
    marker_df = pd.read_csv(path)
    required = {"program", "gene"}
    missing = required.difference(marker_df.columns)
    if missing:
        raise ValueError(f"Program marker file is missing columns: {sorted(missing)}")

    markers: dict[str, list[str]] = {}
    for program, subdf in marker_df.groupby("program"):
        genes = [str(gene) for gene in subdf["gene"].dropna().unique()]
        if genes:
            markers[str(program)] = genes
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


def normalize_for_reference_analysis(adata: sc.AnnData) -> sc.AnnData:
    adata = adata.copy()
    if "counts" in adata.layers:
        adata.X = adata.layers["counts"].copy()
    sc.pp.normalize_total(adata, target_sum=10000)
    sc.pp.log1p(adata)
    return adata


def ensure_embedding(adata: sc.AnnData, n_pcs: int, random_state: int) -> None:
    if "X_umap" in adata.obsm:
        return
    n_comps = min(n_pcs, adata.n_vars, max(2, adata.n_obs - 1))
    sc.pp.pca(adata, n_comps=n_comps, svd_solver="arpack", random_state=random_state)
    sc.pp.neighbors(adata, n_pcs=min(n_pcs, adata.obsm["X_pca"].shape[1]), random_state=random_state)
    sc.tl.umap(adata, random_state=random_state)


def compute_program_scores(
    adata: sc.AnnData,
    markers: dict[str, list[str]],
) -> tuple[sc.AnnData, pd.DataFrame]:
    adata = adata.copy()
    score_rows: list[dict[str, object]] = []
    gene_index = pd.Index(adata.var_names.astype(str))

    for program, genes in markers.items():
        present = [gene for gene in genes if gene in gene_index]
        score_rows.append(
            {
                "program": program,
                "n_input_markers": len(genes),
                "n_markers_found": len(present),
                "markers_found": ",".join(present),
            }
        )
        if present:
            sc.tl.score_genes(adata, gene_list=present, score_name=f"{program}_score", use_raw=False)
        else:
            adata.obs[f"{program}_score"] = 0.0

    score_df = pd.DataFrame(score_rows)
    return adata, score_df


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


def save_umap(adata: sc.AnnData, color: str, output_path: Path, title: str, n_pcs: int, random_state: int) -> None:
    ensure_embedding(adata, n_pcs=n_pcs, random_state=random_state)
    sc.pl.umap(adata, color=color, show=False, title=title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close("all")


def dense_matrix(x) -> np.ndarray:
    if sparse.issparse(x):
        return x.toarray()
    return np.asarray(x)


def prepare_classifier_inputs(
    train_adata: sc.AnnData,
    test_adata: sc.AnnData,
    n_top_hvgs: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]:
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
    y_test = test_selected.obs["broad_program"].astype(str).to_numpy()
    return x_train, x_test, y_train, y_test, selected_genes


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
                    multi_class="multinomial",
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

    train_adata = sc.read_h5ad(project_path(analysis_cfg["train_h5ad"]))
    test_adata = sc.read_h5ad(project_path(analysis_cfg["test_h5ad"]))

    rule_df = read_label_rules(project_path(analysis_cfg["label_rules_csv"]))
    markers = read_program_markers(project_path(analysis_cfg["program_markers_csv"]))

    train_adata = apply_label_rules(
        train_adata,
        label_column=analysis_cfg["train_label_column"],
        rule_df=rule_df,
        dataset_name=analysis_cfg["train_dataset_name"],
    )
    test_adata = apply_label_rules(
        test_adata,
        label_column=analysis_cfg["test_label_column"],
        rule_df=rule_df,
        dataset_name=analysis_cfg["test_dataset_name"],
    )

    train_adata = normalize_for_reference_analysis(train_adata)
    test_adata = normalize_for_reference_analysis(test_adata)

    train_adata, train_marker_summary = compute_program_scores(train_adata, markers)
    test_adata, test_marker_summary = compute_program_scores(test_adata, markers)

    train_marker_summary.to_csv(output_dir / "train_marker_recovery.csv", index=False)
    test_marker_summary.to_csv(output_dir / "test_marker_recovery.csv", index=False)

    save_umap(
        train_adata,
        "broad_program",
        figure_dir / "train_broad_program_umap.png",
        "Train Broad Programs",
        n_pcs=n_pcs,
        random_state=random_state,
    )
    save_umap(
        test_adata,
        "broad_program",
        figure_dir / "test_broad_program_umap.png",
        "Test Broad Programs",
        n_pcs=n_pcs,
        random_state=random_state,
    )
    plot_program_heatmap(train_adata, list(markers), figure_dir / "train_program_score_heatmap.png")
    plot_program_heatmap(test_adata, list(markers), figure_dir / "test_program_score_heatmap.png")
    plot_program_boxplots(train_adata, list(markers), figure_dir / "train_program_score_boxplots.png")

    train_labeled = train_adata[train_adata.obs["broad_program"] != "unmapped"].copy()
    test_labeled = test_adata[test_adata.obs["broad_program"] != "unmapped"].copy()

    valid_programs = train_labeled.obs["broad_program"].value_counts()
    valid_programs = valid_programs[valid_programs >= min_cells].index.tolist()
    train_labeled = train_labeled[train_labeled.obs["broad_program"].isin(valid_programs)].copy()
    test_labeled = test_labeled[test_labeled.obs["broad_program"].isin(valid_programs)].copy()

    if train_labeled.n_obs == 0 or test_labeled.n_obs == 0:
        raise ValueError("No labeled cells remained after applying broad-program rules and minimum cell thresholds.")

    x_train, x_test, y_train, y_test, selected_genes = prepare_classifier_inputs(train_labeled, test_labeled, n_top_hvgs)
    n_components = min(30, x_train.shape[0] - 1, x_train.shape[1])
    if n_components < 2:
        raise ValueError("Too few dimensions are available for PCA-based classifier training.")

    model = build_classifier(classifier_name, n_components=n_components, random_state=random_state)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    labels = sorted(np.unique(y_train).tolist())
    report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()
    report_df.to_csv(output_dir / "cross_dataset_classification_report.csv")

    metrics = {
        "classifier": classifier_name,
        "train_dataset_name": analysis_cfg["train_dataset_name"],
        "test_dataset_name": analysis_cfg["test_dataset_name"],
        "n_train_cells": int(x_train.shape[0]),
        "n_test_cells": int(x_test.shape[0]),
        "n_selected_genes": int(len(selected_genes)),
        "selected_genes_preview": selected_genes[:50],
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "labels_used": labels,
    }
    write_json(metrics, output_dir / "cross_dataset_metrics.json")

    plot_confusion_matrix(y_test, y_pred, labels, figure_dir / "cross_dataset_confusion_matrix.png")

    test_labeled.obs["predicted_broad_program"] = y_pred
    save_umap(
        test_labeled,
        "predicted_broad_program",
        figure_dir / "test_predicted_broad_program_umap.png",
        "Predicted Broad Programs on Test Dataset",
        n_pcs=n_pcs,
        random_state=random_state,
    )

    train_adata.write_h5ad(output_dir / "train_reference_scored.h5ad")
    test_adata.write_h5ad(output_dir / "test_reference_scored.h5ad")
    print(f"Wrote outputs to {output_dir}")


if __name__ == "__main__":
    main()
