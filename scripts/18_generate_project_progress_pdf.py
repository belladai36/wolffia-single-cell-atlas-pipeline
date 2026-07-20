#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "output" / "pdf" / "wolffia_project_progress_summary.pdf"
FIGURE_WT_SHR = PROJECT_ROOT / "figures" / "public_reference_gse123818_wt_train_to_shr" / "test_predicted_broad_program_umap.png"
FIGURE_WT_GSE121619 = PROJECT_ROOT / "figures" / "public_reference_gse123818_wt_train_to_gse121619" / "test_predicted_broad_program_umap.png"
FIGURE_HEATMAP = PROJECT_ROOT / "figures" / "public_reference_gse123818_wt_train_to_shr" / "train_program_score_heatmap.png"


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleSmall",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            spaceAfter=12,
            textColor=colors.HexColor("#153B50"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#1F5A75"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTight",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            spaceAfter=5,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallNote",
            parent=styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#555555"),
            spaceAfter=6,
        )
    )
    return styles


def bullet_list(items: list[str], styles) -> ListFlowable:
    return ListFlowable(
        [
            ListItem(Paragraph(item, styles["BodyTight"]), leftIndent=8)
            for item in items
        ],
        bulletType="bullet",
        start="circle",
        bulletFontName="Helvetica",
        bulletFontSize=8,
        leftIndent=18,
    )


def figure_block(path: Path, caption: str, analysis: str, styles) -> list:
    block = []
    if path.exists():
        img = Image(str(path))
        img._restrictSize(6.8 * inch, 3.8 * inch)
        block.append(img)
        block.append(Spacer(1, 0.06 * inch))
        block.append(Paragraph(f"<b>Figure:</b> {caption}", styles["BodyTight"]))
        block.append(Paragraph(f"<b>Interpretation:</b> {analysis}", styles["BodyTight"]))
        block.append(Spacer(1, 0.14 * inch))
    else:
        block.append(Paragraph(f"Figure missing: {path.name}", styles["SmallNote"]))
    return block


def build_story():
    styles = build_styles()
    story = []

    story.append(Paragraph("Wolffia Project Progress Summary", styles["TitleSmall"]))
    story.append(
        Paragraph(
            "Prediction-first single-cell framework for <i>Wolffia australiana</i> before new Wolffia single-cell data arrive.",
            styles["BodyTight"],
        )
    )
    story.append(
        Paragraph(
            "Status: Wolffia-facing transfer preparation stage",
            styles["SmallNote"],
        )
    )

    story.append(Paragraph("Project Goal", styles["Section"]))
    story.append(
        Paragraph(
            "Use public plant single-cell datasets plus Wolffia biology to predict whether Wolffia preserves, reduces, merges, or compresses major flowering-plant cell programs.",
            styles["BodyTight"],
        )
    )

    story.append(Paragraph("What Has Been Built", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Prediction-first transfer workflow plus a legacy FASTQ-level alignment-and-counting scaffold for custom raw-data processing.",
                "Public-reference transfer workflow that computes broad program scores, trains a classifier, and tests transfer across public datasets.",
                "Arabidopsis validation layer using GSE227564, GSE141730, GSE121619, and GSE123818.",
                "Wolffia-facing interpretation framework that treats labels as transferable biological programs rather than literal Arabidopsis tissue identities.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Most Important Results So Far", styles["Section"]))
    data = [
        ["Question", "What We Learned"],
        ["Callus vs root reference", "Callus-trained references over-collapsed target cells into one stress-like sink."],
        ["Root-derived training", "Root-derived references were much more biologically interpretable."],
        ["Stress bucket refinement", "The old stress-like category split into interface/water-balance and abiotic-stress components."],
        ["Vascular refinement", "Vascular signal remains weaker than interface/stress axes at this broad level."],
    ]
    table = Table(data, colWidths=[1.8 * inch, 4.7 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEAF2")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#153B50")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#8CA3AF")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FBFD")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(table)

    story.append(Spacer(1, 0.14 * inch))
    story.append(Paragraph("Current Working Broad Program Set", styles["Section"]))
    story.append(
        bullet_list(
            [
                "proliferative_or_meristematic",
                "photosynthetic_or_assimilation",
                "vascular_like_or_transport",
                "developmental_transition",
                "epidermal_or_surface_identity",
                "reproductive_or_floral",
                "transport_interface_or_water_balance",
                "abiotic_stress_response",
            ],
            styles,
        )
    )

    story.append(Paragraph("What Is Still Missing", styles["Section"]))
    story.append(
        bullet_list(
            [
                "No usable Wolffia matrices are present locally yet.",
                "The Wolffia raw-data folders currently exist only as placeholders.",
                "Actual Wolffia training requires FASTQ download plus count-matrix generation or a processed matrix.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Immediate Blocker", styles["Section"]))
    story.append(
        Paragraph(
            "The main blocker is data availability and format, not project design. We need external storage, the first public Wolffia scRNA runs from PRJNA1124135, and a count matrix or h5ad before training can begin.",
            styles["BodyTight"],
        )
    )

    story.append(Paragraph("Best Next Steps", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Get an external SSD and download the four PRJNA1124135 scRNA runs.",
                "Generate a Wolffia count matrix and convert it into h5ad.",
                "Cluster the first Wolffia dataset conservatively and compute module scores with the frozen broad program set.",
                "Use PRJNA809022 later as validation after the first Wolffia-native reference is built.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Best Files for a New Viewer", styles["Section"]))
    story.append(
        bullet_list(
            [
                "README.md",
                "docs/project_progress_summary.md",
                "docs/root_derived_reference_update.md",
                "docs/wolffia_first_transfer_note.md",
                "docs/wolffia_reference_training_plan.md",
            ],
            styles,
        )
    )

    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "Bottom line: the project now has a working computational scaffold, validated Arabidopsis reference tests, an improved broad-program ontology, and a clear operational path to the first real Wolffia training run.",
            styles["BodyTight"],
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("Representative Analysis Figures", styles["Section"]))
    story.append(
        Paragraph(
            "These figures show low-dimensional UMAP embeddings generated from the scored public-reference outputs. They are useful for seeing whether broad programs form structured neighborhoods or collapse into one diffuse cloud.",
            styles["BodyTight"],
        )
    )

    story.extend(
        figure_block(
            FIGURE_WT_SHR,
            "UMAP projection of predicted broad programs for GSE123818 WT-trained transfer into GSE123818 SHR.",
            "This plot shows that the SHR target does not collapse into one completely uniform cloud. Instead, the cells are partitioned mainly between transport/interface-water-balance and abiotic-stress-response structure, with a smaller proliferative component. That supports the idea that the old monolithic stress label was hiding two interpretable biological axes.",
            styles,
        )
    )

    story.extend(
        figure_block(
            FIGURE_WT_GSE121619,
            "UMAP projection of predicted broad programs for GSE123818 WT-trained transfer into GSE121619.",
            "This cross-study result is noisier, which is expected, but it still shows that the refined reference produces more than one dominant program. The most important takeaway is that proliferative cells remain recoverable while interface- and stress-associated programs account for much of the remaining structure.",
            styles,
        )
    )

    story.extend(
        figure_block(
            FIGURE_HEATMAP,
            "Mean program-score heatmap across broad programs in the root-derived training reference.",
            "This heatmap is one of the best diagnostics for whether the broad ontology is behaving sensibly. Strong diagonal-like signal means the assigned program usually has the highest average score within its own group. Off-diagonal signal shows overlap, which is exactly what tipped us off that stress, interface, and transport biology were initially being mixed together.",
            styles,
        )
    )

    story.append(
        Paragraph(
            "Why these graphs matter: they let us judge whether the classifier is finding biologically structured programs or just inventing labels. For this project, the most reassuring change was not that every program separated perfectly, but that the refined reference stopped acting like one giant stress sink and started showing more interpretable axes.",
            styles["BodyTight"],
        )
    )
    return story


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Wolffia Project Progress Summary",
        author="OpenAI Codex",
    )
    doc.build(build_story())
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
