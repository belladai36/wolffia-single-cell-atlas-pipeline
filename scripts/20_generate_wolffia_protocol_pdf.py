#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "output" / "pdf" / "wolffia_data_generation_protocol.pdf"


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ProtocolTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#143B4A"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ProtocolSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#355C6B"),
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#1D5F7A"),
            spaceBefore=10,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subsection",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            textColor=colors.HexColor("#224B5B"),
            spaceBefore=7,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTight",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12.5,
            alignment=TA_LEFT,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallNote",
            parent=styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#666666"),
            spaceAfter=5,
        )
    )
    return styles


def bullet_list(items: list[str], styles, left_indent: int = 18) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodyTight"]), leftIndent=8) for item in items],
        bulletType="bullet",
        start="circle",
        bulletFontName="Helvetica",
        bulletFontSize=8,
        leftIndent=left_indent,
    )


def info_table(rows: list[list[str]], col_widths: list[float]) -> Table:
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF2")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#143B4A")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#8FA7B3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FBFD")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def add_stage(story, styles, title, purpose, samples, instruments, materials, outputs, risks):
    story.append(Paragraph(title, styles["Subsection"]))
    story.append(Paragraph(f"<b>Purpose:</b> {purpose}", styles["BodyTight"]))
    story.append(Paragraph(f"<b>Samples needed:</b> {samples}", styles["BodyTight"]))
    story.append(Paragraph("<b>Instruments needed:</b>", styles["BodyTight"]))
    story.append(bullet_list(instruments, styles))
    story.append(Paragraph("<b>Consumables or reagents:</b>", styles["BodyTight"]))
    story.append(bullet_list(materials, styles))
    story.append(Paragraph("<b>Expected outputs:</b>", styles["BodyTight"]))
    story.append(bullet_list(outputs, styles))
    story.append(Paragraph("<b>Main risks to watch:</b>", styles["BodyTight"]))
    story.append(bullet_list(risks, styles))
    story.append(Spacer(1, 0.08 * inch))


def build_story():
    styles = build_styles()
    story = []

    story.append(Paragraph("Wolffia Data-Generation Protocol", styles["ProtocolTitle"]))
    story.append(
        Paragraph(
            "A staged experimental protocol for generating the first <i>Wolffia australiana</i> single-cell or single-nucleus transcriptomic dataset for atlas construction.",
            styles["ProtocolSubtitle"],
        )
    )
    story.append(
        Paragraph(
            "Prepared as a formal planning and execution document. This protocol is intentionally conservative: the critical early decision is to identify the cleanest Wolffia input route before scaling to a larger sequencing run.",
            styles["SmallNote"],
        )
    )

    story.append(Paragraph("Abstract", styles["Section"]))
    story.append(
        Paragraph(
            "The purpose of this protocol is to establish a practical and scientifically defensible workflow for generating a first Wolffia transcriptomic reference dataset. Because the largest technical risk in plant single-cell experiments is often sample preparation rather than downstream sequencing, this protocol emphasizes a matched pilot comparison between intact-cell and nuclei-based inputs. The initial discovery experiment is designed to recover broad biological programs reproducibly, creating a stable foundation for later developmental and perturbation-focused studies.",
            styles["BodyTight"],
        )
    )

    story.append(Paragraph("1. Objective", styles["Section"]))
    story.append(
        Paragraph(
            "The immediate goal is to generate a dataset that can test whether Wolffia preserves broad plant programs such as proliferation, photosynthesis, transport or interface biology, and developmental transition. The first experiment should prioritize clean biology and reproducibility over maximum complexity.",
            styles["BodyTight"],
        )
    )

    story.append(Paragraph("2. Recommended Strategy", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Standardize one healthy vegetative Wolffia growth condition.",
                "Run a pilot comparing intact-cell preparation against nuclei preparation on matched material.",
                "Use QC metrics to choose the cleaner route.",
                "Scale that route to three biological replicates for the first discovery run.",
                "Analyze the resulting data immediately against the current broad-program prediction framework.",
            ],
            styles,
        )
    )

    story.append(Paragraph("3. Why This Matters", styles["Section"]))
    story.append(
        Paragraph(
            "For plant single-cell experiments, the main failure point is often sample preparation rather than sequencing. In Wolffia, harsh digestion, debris release, chloroplast-rich material, and prep-induced stress responses can overwhelm the data. That is why this protocol uses a decision gate before full-scale library preparation. The biological framing of Wolffia as a highly reduced yet developmentally competent flowering plant is supported by genomic and morphology-focused studies [1,2].",
            styles["BodyTight"],
        )
    )

    story.append(Paragraph("4. Stage-by-Stage Execution", styles["Section"]))
    add_stage(
        story,
        styles,
        "Stage 1: Culture Standardization",
        "Reduce biological variability before any single-cell work begins.",
        "One defined Wolffia line or stock under a single baseline vegetative condition.",
        [
            "Controlled growth chamber or culture area",
            "Light source with defined photoperiod",
            "Thermometer or chamber logging",
            "Pipettes",
            "Sterile culture vessels",
        ],
        [
            "Defined growth medium",
            "Sterile water or appropriate rinse buffer",
            "Labels and metadata sheet",
            "Sterile plastics",
        ],
        [
            "Stable healthy Wolffia cultures",
            "Standardized metadata fields",
            "Enough biomass for pilot testing",
        ],
        [
            "Hidden contamination",
            "Mixed healthy and senescent fronds",
            "Growth variation across vessels",
        ],
    )

    add_stage(
        story,
        styles,
        "Stage 2: Pre-Experiment Characterization",
        "Confirm that the input material is visually healthy and comparable across replicates.",
        "Representative material from each planned biological replicate.",
        [
            "Brightfield microscope or stereomicroscope",
            "Camera or phone adapter",
            "Balance if wet-weight estimation is possible",
        ],
        [
            "Notebook or digital metadata file",
            "Sample dishes or slides",
        ],
        [
            "Microscopy images",
            "Biomass estimate",
            "Go or no-go decision for each replicate",
        ],
        [
            "Proceeding with stressed cultures",
            "Ignoring contamination or age heterogeneity",
        ],
    )

    add_stage(
        story,
        styles,
        "Stage 3A: Intact-Cell Pilot",
        "Test whether viable Wolffia cells can be released cleanly enough for a cell-based transcriptomic workflow.",
        "Freshly harvested healthy Wolffia tissue, split across several pilot conditions.",
        [
            "Fine blades or gentle disruption tools",
            "Orbital shaker or gentle rocker if used",
            "Microscope",
            "Cell strainers or mesh filters",
            "Gentle centrifuge setup",
            "Hemocytometer or cell counter",
            "Timer",
        ],
        [
            "Osmotic stabilization buffer",
            "Cellulase-class digestion reagent",
            "Pectinase or macerozyme-like reagent",
            "Calcium and buffering salts",
            "Viability dye if used by the lab",
        ],
        [
            "Recovered-cell counts",
            "Viability measurements",
            "Debris and clumping assessment",
            "Time-to-stabilization notes",
        ],
        [
            "Over-digestion",
            "Broken cells",
            "Severe clumping",
            "Prep-induced stress signatures",
        ],
    )

    add_stage(
        story,
        styles,
        "Stage 3B: Nuclei Pilot",
        "Test whether nuclei give a cleaner Wolffia input than intact cells.",
        "Fresh Wolffia harvested and kept cold throughout preparation.",
        [
            "Ice bucket or cold block",
            "Dounce homogenizer or equivalent",
            "Filters or strainers",
            "Refrigerated centrifuge",
            "Microscope",
            "Hemocytometer or nuclei counter",
        ],
        [
            "Cold nuclei isolation buffer",
            "Appropriate lysis chemistry",
            "RNase-safe plastics and reagents",
            "DNA stain for nuclei counting if used",
        ],
        [
            "Nuclei counts",
            "Integrity assessment",
            "Clumping notes",
            "Ambient-RNA and plastid carryover observations",
        ],
        [
            "Nuclear rupture",
            "Heavy ambient contamination",
            "Aggregation",
            "Poor nuclei purity",
        ],
    )

    story.append(Paragraph("5. Route Selection Criteria", styles["Section"]))
    story.append(
        Paragraph(
            "Choose the route that gives the cleaner and more reproducible biology. Do not choose based on ambition alone.",
            styles["BodyTight"],
        )
    )
    story.append(
        info_table(
            [
                ["Criterion", "Favors intact-cell route", "Favors nuclei route"],
                ["Yield", "High viable-cell recovery", "Higher clean nuclei recovery"],
                ["Stress artifact risk", "Acceptable and limited", "Clearly lower than cell prep"],
                ["Debris burden", "Manageable", "Substantially lower"],
                ["Organellar carryover", "Acceptable", "Lower or easier to interpret"],
                ["Reproducibility", "Consistent across replicates", "More consistent across replicates"],
            ],
            [1.55 * inch, 2.45 * inch, 2.45 * inch],
        )
    )

    story.append(Paragraph("6. First Full Discovery Run", styles["Section"]))
    story.append(
        bullet_list(
            [
                "One defined biological condition: healthy vegetative Wolffia.",
                "Three biological replicates harvested independently.",
                "One locked preparation route selected from the pilot.",
                "One consistent library-prep workflow.",
                "Balanced sequencing across replicates rather than many mixed conditions.",
            ],
            styles,
        )
    )
    story.append(
        Paragraph(
            "If the lab is using PIP-seq, keep the Wolffia-specific optimization concentrated upstream at the sample-preparation step, deliver a low-clump low-debris suspension, and match the core facility's loading requirements. If a different lower-throughput full-length workflow is used later, keep the first run modest and prioritize per-cell quality. If a higher-throughput nuclei-compatible workflow is used, prioritize robust recovery of broad states.",
            styles["BodyTight"],
        )
    )

    story.append(Paragraph("7. Required Metadata", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Sample ID and biological replicate ID",
                "Genotype or stock ID",
                "Medium composition",
                "Light cycle and harvest time within the cycle",
                "Temperature",
                "Operator",
                "Preparation route",
                "Pilot condition or buffer version",
                "Viability or nuclei integrity metric",
                "Library batch",
                "Sequencing run or lane information",
            ],
            styles,
        )
    )

    story.append(Paragraph("8. Immediate Computational Readouts", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Reads and genes detected per cell or nucleus",
                "Organellar fraction summaries",
                "Replicate mixing assessment",
                "Low-dimensional embedding such as UMAP",
                "Marker-gene tables",
                "Module-score plots for broad programs",
                "Detection of prep-induced stress artifacts",
            ],
            styles,
        )
    )
    story.append(
        Paragraph(
            "A successful first experiment should recover at least some of the expected broad Wolffia programs even if fine labels remain uncertain. That is enough to establish a Wolffia-native reference for later perturbation or developmental work.",
            styles["BodyTight"],
        )
    )

    story.append(Paragraph("9. Practical Timeline", styles["Section"]))
    story.append(
        info_table(
            [
                ["Week", "Main goal"],
                ["1", "Stabilize cultures, finalize metadata sheet, and set up microscopy logging."],
                ["2", "Run intact-cell pilot and nuclei pilot on matched material."],
                ["3", "Choose the cleaner route and repeat on fresh biological replicates."],
                ["4", "Prepare libraries and submit sequencing."],
                ["5+", "Run computational QC, clustering, and program-level interpretation."],
            ],
            [0.8 * inch, 5.95 * inch],
        )
    )

    story.append(Paragraph("10. Bottom Line", styles["Section"]))
    story.append(
        Paragraph(
            "The best first Wolffia experiment is the cleanest one, not the largest one: healthy vegetative material, matched cell-versus-nuclei pilot, evidence-based route selection, three biological replicates, and immediate analysis against the current prediction framework.",
            styles["BodyTight"],
        )
    )

    story.append(Paragraph("References", styles["Section"]))
    story.append(
        bullet_list(
            [
                "[1] Park, J., et al. 2021. Genome of the world's smallest flowering plant, Wolffia australiana, helps explain its specialized physiology and unique morphology. Communications Biology. doi:10.1038/s42003-021-02389-w",
                "[2] Hoang, P. T. N., et al. 2022. The genome of Wolffia australiana facilitates discovery of genetic basis for aquatic adaptation in duckweeds. The Plant Cell. doi:10.1093/plcell/koac068",
            ],
            styles,
        )
    )

    return story


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        leftMargin=0.72 * inch,
        rightMargin=0.72 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.68 * inch,
        title="Wolffia Data-Generation Protocol",
        author="OpenAI Codex",
    )
    doc.build(build_story())
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
