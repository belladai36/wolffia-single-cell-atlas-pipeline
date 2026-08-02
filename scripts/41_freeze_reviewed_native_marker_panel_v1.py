#!/usr/bin/env python3
"""Freeze the reviewed Wolffia-native marker panel v1.

The input is the manual review recommendation table. Rows recommended as
``keep``, ``maybe``, or ``unknown_interesting`` are retained. The output panel is
the current best review-ready marker panel for future Wolffia program scoring.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("data/metadata/wolffia_trusted_marker_panel_manual_review_recommendations.csv")
DEFAULT_OUTPUT = Path("data/metadata/wolffia_reviewed_native_marker_panel_v1.csv")

KEEP_DECISIONS = {"keep", "maybe", "unknown_interesting"}


def reviewed_marker_tier(decision: str) -> str:
    """Convert manual recommendation decision into the v1 panel tier."""
    if decision == "keep":
        return "reviewed_core"
    if decision == "maybe":
        return "reviewed_supporting"
    if decision == "unknown_interesting":
        return "reviewed_unknown_watchlist"
    return "excluded"


def build_reviewed_panel(recommendations: pd.DataFrame) -> pd.DataFrame:
    required = {
        "native_program_id",
        "native_program_name",
        "waus8730_gene_id",
        "preferred_name",
        "manual_recommended_decision",
        "manual_review_confidence",
        "annotation_fit_to_program",
        "suggested_program_adjustment",
        "manual_review_notes_recommended",
    }
    missing = sorted(required - set(recommendations.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    panel = recommendations[
        recommendations["manual_recommended_decision"].isin(KEEP_DECISIONS)
    ].copy()
    panel["reviewed_panel_version"] = "v1"
    panel["reviewed_panel_tier"] = panel["manual_recommended_decision"].map(reviewed_marker_tier)
    panel["reviewed_decision_source"] = "manual_review_recommendation"

    output_columns = [
        "reviewed_panel_version",
        "native_program_id",
        "native_program_name",
        "reviewed_panel_tier",
        "waus8730_gene_id",
        "preferred_name",
        "source_leiden_clusters",
        "best_marker_rank",
        "max_marker_score",
        "evidence_level",
        "annotation_summary",
        "manual_recommended_decision",
        "manual_review_confidence",
        "annotation_fit_to_program",
        "suggested_program_adjustment",
        "manual_review_notes_recommended",
        "reviewed_decision_source",
    ]
    return panel[output_columns].sort_values(
        [
            "native_program_name",
            "reviewed_panel_tier",
            "best_marker_rank",
            "max_marker_score",
            "waus8730_gene_id",
        ],
        ascending=[True, True, True, False, True],
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Freeze reviewed Wolffia-native marker panel v1."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    recommendations = pd.read_csv(args.input)
    panel = build_reviewed_panel(recommendations)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(args.output, index=False)

    print(f"Wrote: {args.output}")
    print(f"Rows: {len(panel)}")
    print("Rows by reviewed tier:")
    print(panel["reviewed_panel_tier"].value_counts().sort_index().to_string())
    print("Rows by program:")
    print(panel["native_program_name"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
