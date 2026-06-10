from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _resolve_from_project_root(path_value: str | Path) -> Path:
    path = Path(path_value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (PROJECT_ROOT / path).resolve()


def load_config(config_path: str | Path) -> dict[str, Any]:
    resolved_config = _resolve_from_project_root(config_path)
    with open(resolved_config, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def project_path(path_value: str | Path) -> Path:
    return _resolve_from_project_root(path_value)


def ensure_dirs(config: dict[str, Any]) -> None:
    for key in ["counts_dir", "scanpy_dir", "figure_dir", "log_dir"]:
        path = config["paths"].get(key)
        if path:
            project_path(path).mkdir(parents=True, exist_ok=True)
    for subdir in ["qc", "umap", "markers", "paga"]:
        (project_path(config["paths"]["figure_dir"]) / subdir).mkdir(parents=True, exist_ok=True)


def write_json(data: dict[str, Any], path: str | Path) -> None:
    path = project_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def add_gene_flags(adata, config: dict[str, Any]) -> None:
    qc = config["qc"]
    gene_names = adata.var_names.astype(str)

    mito_prefixes = tuple(qc.get("mitochondrial_gene_prefixes") or [])
    plastid_prefixes = tuple(qc.get("plastid_gene_prefixes") or [])

    adata.var["mito"] = [name.startswith(mito_prefixes) for name in gene_names]
    adata.var["plastid"] = [name.startswith(plastid_prefixes) for name in gene_names]
