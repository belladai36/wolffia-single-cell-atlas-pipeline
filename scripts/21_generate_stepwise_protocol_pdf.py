#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "output" / "pdf" / "wolffia_stepwise_protocol.pdf"


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ProtocolTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            spaceAfter=8,
            textColor=colors.HexColor("#163A4D"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="ProtocolSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            spaceAfter=7,
            textColor=colors.HexColor("#355C6B"),
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
            spaceAfter=5,
            textColor=colors.HexColor("#1E607A"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Step",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            spaceBefore=8,
            spaceAfter=4,
            textColor=colors.HexColor("#214A5A"),
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
            leading=10.5,
            textColor=colors.HexColor("#666666"),
            spaceAfter=6,
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


def numbered_list(items: list[str], styles, left_indent: int = 20) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodyTight"]), leftIndent=8) for item in items],
        bulletType="1",
        leftIndent=left_indent,
    )


def info_table(rows: list[list[str]], widths: list[float]) -> Table:
    cell_style = ParagraphStyle(
        name="TableCell",
        parent=getSampleStyleSheet()["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=10,
        spaceAfter=0,
        alignment=TA_LEFT,
        wordWrap="CJK",
    )
    header_style = ParagraphStyle(
        name="TableHeader",
        parent=cell_style,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#153B50"),
    )
    wrapped_rows = []
    for row_index, row in enumerate(rows):
        style = header_style if row_index == 0 else cell_style
        wrapped_rows.append([Paragraph(str(cell), style) for cell in row])

    table = Table(wrapped_rows, colWidths=widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEAF2")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#153B50")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#8CA3AF")),
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


def step_block(styles, title: str, goal: str, actions: list[str], checks: list[str], outputs: list[str]):
    block = [
        Paragraph(title, styles["Step"]),
        Paragraph(f"<b>Goal:</b> {goal}", styles["BodyTight"]),
        Paragraph("<b>Actions:</b>", styles["BodyTight"]),
        numbered_list(actions, styles),
        Paragraph("<b>QC or decision points:</b>", styles["BodyTight"]),
        bullet_list(checks, styles),
        Paragraph("<b>Expected outputs:</b>", styles["BodyTight"]),
        bullet_list(outputs, styles),
        Spacer(1, 0.08 * inch),
    ]
    return KeepTogether(block)


def build_story():
    styles = build_styles()
    story = []

    story.append(Paragraph("Step-by-Step Protocol for Generating Wolffia Transcriptomic Data", styles["ProtocolTitle"]))
    story.append(
        Paragraph(
            "Pilot-to-discovery workflow for generating a first <i>Wolffia australiana</i> single-cell or single-nucleus transcriptomic dataset.",
            styles["ProtocolSubtitle"],
        )
    )
    story.append(
        Paragraph(
            "This document is written as a clean, stepwise experimental protocol. It is designed for the first Wolffia data-generation effort and emphasizes route selection between intact cells and nuclei before scaling to a larger sequencing run.",
            styles["SmallNote"],
        )
    )

    story.append(Paragraph("Purpose", styles["Section"]))
    story.append(
        Paragraph(
            "The purpose of this protocol is to generate a first Wolffia dataset that can recover broad transcriptional programs reproducibly, distinguish biological structure from preparation artifacts, and support the first Wolffia-native atlas analysis.",
            styles["BodyTight"],
        )
    )
    story.append(
        Paragraph(
            "The key operational question is whether Wolffia yields cleaner transcriptomes through intact-cell preparation or nuclei preparation.",
            styles["BodyTight"],
        )
    )

    story.append(Paragraph("Experimental Scope", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Wolffia culture standardization",
                "Pre-harvest culture quality control",
                "Matched pilot comparison of intact-cell and nuclei routes",
                "Route-selection criteria",
                "Execution of the first full discovery run",
                "Immediate post-sequencing quality control",
            ],
            styles,
        )
    )

    story.append(Paragraph("Recommended Baseline Culture Framework", styles["Section"]))
    story.append(
        Paragraph(
            "If a successful local Wolffia maintenance condition already exists, use that condition without unnecessary re-optimization during the pilot phase. If no standard exists, use the following pilot baseline for consistency:",
            styles["BodyTight"],
        )
    )
    story.append(
        bullet_list(
            [
                "Axenic liquid culture if possible",
                "One Wolffia line or stock only",
                "One baseline vegetative growth condition",
                "16-hour light / 8-hour dark photoperiod",
                "22 to 25 C stable growth temperature",
                "Low-to-moderate constant light appropriate for healthy duckweed growth",
                "Harvest at the same time of day for all replicates",
            ],
            styles,
        )
    )

    story.append(Paragraph("Required Materials and Equipment", styles["Section"]))
    story.append(
        info_table(
            [
                ["Category", "Key items"],
                ["Culture and sampling", "Healthy Wolffia stock, growth medium, sterile vessels, sterile pipettes and tips, sterile forceps or sampling tools, metadata sheet or electronic log"],
                ["Pre-harvest QC", "Brightfield microscope or stereomicroscope, imaging device, optional balance for wet-weight estimation"],
                ["Intact-cell pilot", "Fine blade or gentle disruption tool, osmotic stabilization buffer, plant cell-wall digestion reagents, mesh filters or strainers, low-speed centrifuge, hemocytometer or automated counter, optional viability dye"],
                ["Nuclei pilot", "Ice bucket or cold block, nuclei isolation buffer, gentle homogenization setup such as a Dounce homogenizer, mesh filters or strainers, refrigerated centrifuge, nuclei counting setup, optional DNA stain"],
                ["Library preparation and sequencing", "Chosen library-prep kit or core-facility workflow, low-bind tubes, RNase-free plastics, PCR or amplification equipment, library quantification system, sequencing core or sequencing platform access"],
            ],
            [1.6 * inch, 4.8 * inch],
        )
    )

    story.append(Paragraph("Required Metadata", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Sample ID",
                "Biological replicate ID",
                "Stock or genotype ID",
                "Medium",
                "Temperature",
                "Photoperiod",
                "Harvest date and time",
                "Operator",
                "Preparation route: cell or nucleus",
                "Preparation condition ID",
                "Viability or nuclei-integrity observation",
                "Library batch",
                "Sequencing batch",
            ],
            styles,
        )
    )

    story.append(Paragraph("Protocol", styles["Section"]))
    story.append(
        step_block(
            styles,
            "Step 1: Establish and stabilize Wolffia cultures",
            "Create standardized starting material before any pilot preparation begins.",
            [
                "Start with one Wolffia line or stock only.",
                "Grow the material under one defined baseline vegetative condition.",
                "Maintain the same medium, light schedule, and temperature across all pilot cultures.",
                "Avoid mixing very old and very young cultures in the same experimental batch.",
                "Keep a culture log for at least several days before harvest.",
            ],
            [
                "Cultures should be visibly healthy and not overcrowded.",
                "No obvious contamination should be present.",
                "Growth conditions should be consistent across vessels.",
            ],
            [
                "Healthy, standardized Wolffia cultures",
                "Stable maintenance conditions",
                "Clear metadata records",
            ],
        )
    )

    story.append(
        step_block(
            styles,
            "Step 2: Perform pre-harvest culture QC",
            "Confirm that the material is worth processing.",
            [
                "Inspect representative fronds by brightfield microscopy or stereomicroscopy.",
                "Record visible morphology, frond size, budding status, and contamination.",
                "Estimate available biomass by frond count, wet weight, or both.",
                "Exclude cultures that are obviously stressed, contaminated, senescent, or highly heterogeneous.",
            ],
            [
                "Proceed only if cultures are visibly healthy, reasonably uniform, and sufficient in biomass for a split pilot.",
            ],
            [
                "Microscopy images",
                "Biomass estimate",
                "Go or no-go decision for each planned replicate",
            ],
        )
    )

    story.append(
        step_block(
            styles,
            "Step 3: Harvest fresh Wolffia tissue",
            "Collect material in a way that minimizes artificial damage.",
            [
                "Harvest tissue gently to avoid mechanical damage.",
                "Use the same harvest method and timing for all matched pilot samples.",
                "Minimize the time between harvest and the start of preparation.",
                "For nuclei preparations, place tissue on ice immediately after harvest.",
                "For intact-cell preparations, move tissue rapidly into the chosen wash or stabilization buffer.",
            ],
            [
                "Record harvest-to-processing time for every sample.",
                "Do not allow one sample to sit substantially longer than another.",
            ],
            [
                "Fresh matched material ready for route comparison",
                "Documented handling times",
            ],
        )
    )

    story.append(
        step_block(
            styles,
            "Step 4: Split the matched pilot into two preparation routes",
            "Create a fair technical comparison between the cell and nuclei approaches.",
            [
                "From the same starting biological material, divide the sample into Route A and Route B.",
                "Assign Route A to intact-cell preparation.",
                "Assign Route B to nuclei preparation.",
            ],
            [
                "This split is for technical comparison, not biological comparison.",
                "The starting material for both routes should be as similar as possible.",
            ],
            [
                "Matched pilot material for the two routes",
            ],
        )
    )

    story.append(
        step_block(
            styles,
            "Step 5A: Run the intact-cell preparation pilot",
            "Test whether intact, viable single cells can be recovered with acceptable quality.",
            [
                "Rinse freshly harvested Wolffia briefly to remove residual medium.",
                "Disrupt the tissue gently using a fine blade or similarly mild mechanical method.",
                "Transfer tissue into a plant cell-wall digestion solution.",
                "Incubate under gentle conditions for a short pilot time course.",
                "Filter the digest through a suitable mesh to remove large debris.",
                "Wash the recovered cells into an osmotic stabilization buffer.",
                "Count cells immediately and inspect morphology.",
                "Measure viability if the workflow supports it.",
            ],
            [
                "Compare a small pilot matrix rather than assuming one final recipe on day one.",
                "Track total recovered cell count, concentration, viability, visible clumping, debris burden, and time from harvest to stabilization.",
                "Failure criteria include mostly broken material, very low viability, extreme clumping, very low yield, or harsh treatment required just to recover any cells.",
            ],
            [
                "Cell yield and viability measurements",
                "Morphology notes",
                "Evidence for or against continuing the cell route",
            ],
        )
    )

    story.append(
        step_block(
            styles,
            "Step 5B: Run the nuclei preparation pilot",
            "Test whether nuclei provide a cleaner and more reproducible Wolffia input.",
            [
                "Keep freshly harvested Wolffia cold from the start of processing.",
                "Transfer tissue into a cold nuclei isolation buffer.",
                "Homogenize gently just enough to release nuclei.",
                "Filter the homogenate to remove large debris.",
                "Pellet and wash nuclei carefully under cold conditions.",
                "Count nuclei and inspect nuclear integrity.",
                "If appropriate, use a standard nuclei stain for counting or gating.",
            ],
            [
                "Track nuclei count, clumping, visible nuclear integrity, debris burden, apparent plastid carryover, and apparent ambient contamination.",
                "Failure criteria include extensive rupture, severe aggregation, extreme contamination, or very poor recovery.",
            ],
            [
                "Nuclei yield and integrity measurements",
                "Evidence for or against continuing the nuclei route",
            ],
        )
    )

    story.append(
        step_block(
            styles,
            "Step 6: Choose the route for the full experiment",
            "Select the best upstream route using evidence rather than preference.",
            [
                "Review the intact-cell and nuclei pilot outputs side by side.",
                "Select the intact-cell route only if viable cell recovery is reproducible and debris, clumping, and harshness remain manageable.",
                "Select the nuclei route if the cell route is harsh, inconsistent, or low-yield and nuclei are clearly cleaner and more reproducible.",
            ],
            [
                "Do not force the intact-cell route if nuclei are clearly superior.",
                "Choose the route most likely to preserve interpretable biology.",
            ],
            [
                "One selected preparation route for the full discovery run",
            ],
        )
    )

    story.append(
        step_block(
            styles,
            "Step 7: Run the first full Wolffia discovery experiment",
            "Generate the first real Wolffia dataset under a simple, controlled design.",
            [
                "Lock the upstream preparation route chosen from the pilot.",
                "Run one defined vegetative condition only.",
                "Collect three biological replicates.",
                "Use one fixed preparation route and one fixed library-prep workflow.",
            ],
            [
                "Do not combine multiple perturbations or rare-state enrichment schemes in the first run.",
                "The first experiment should remain simple and interpretable.",
            ],
            [
                "A balanced first discovery dataset",
                "Three biological replicates processed under one route",
            ],
        )
    )

    story.append(
        step_block(
            styles,
            "Step 8: Prepare libraries and sequence",
            "Generate libraries in a balanced and consistent way.",
            [
                "Use the selected input type consistently across all replicates.",
                "Keep library preparation as uniform as possible across replicates.",
                "Sequence replicates in a balanced way to avoid obvious batch imbalance.",
                "Prioritize library quality and replicate consistency over scale inflation.",
            ],
            [
                "If the lab uses PIP-seq, upstream preparation quality, low debris, and the correct loading range remain the key Wolffia-specific variables.",
                "If the lab uses another lower-throughput full-length workflow or a higher-throughput nuclei-compatible workflow later, the same principle still applies.",
            ],
            [
                "Sequence-ready libraries",
                "Balanced sequencing submission",
            ],
        )
    )

    story.append(
        step_block(
            styles,
            "Step 9: Perform immediate post-sequencing QC",
            "Determine whether the experiment produced useful and interpretable data.",
            [
                "Evaluate reads per cell or per nucleus.",
                "Evaluate genes detected per cell or per nucleus.",
                "Measure organellar fraction.",
                "Assess ambient-RNA-like background.",
                "Check replicate mixing.",
                "Check stress-like artifact burden.",
                "Assess the stability of recovered clusters or neighborhoods.",
            ],
            [
                "Minimum biological success is recovery of at least some broad expected programs in a reproducible way.",
                "Examples include proliferative or meristematic signal, photosynthetic or assimilation signal, transport or interface-associated signal, and developmental transition-like signal.",
            ],
            [
                "Immediate QC summary",
                "Evidence that the first Wolffia run is biologically usable or needs revision",
            ],
        )
    )

    story.append(Paragraph("What Not to Do", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Do not change culture conditions immediately before harvest.",
                "Do not process stressed or mixed-quality material.",
                "Do not force an intact-cell route if nuclei are clearly cleaner.",
                "Do not over-optimize indefinitely without generating a real test dataset.",
                "Do not over-interpret technical stress as novel Wolffia biology.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Recommended Timeline", styles["Section"]))
    story.append(
        info_table(
            [
                ["Week", "Main goal"],
                ["1", "Standardize cultures and finalize metadata tracking."],
                ["2", "Run matched intact-cell and nuclei pilots."],
                ["3", "Choose the cleaner route and repeat on fresh material if needed."],
                ["4", "Prepare the first full libraries and submit sequencing."],
                ["5+", "Run computational QC and first-pass biological interpretation."],
            ],
            [0.8 * inch, 5.8 * inch],
        )
    )

    story.append(Paragraph("References", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Park J. et al. 2021. Genome of the world's smallest flowering plant, Wolffia australiana, helps explain its specialized physiology and unique morphology. Communications Biology. doi:10.1038/s42003-021-02389-w",
                "Hoang P.T.N. et al. 2022. The genome of Wolffia australiana facilitates discovery of genetic basis for aquatic adaptation in duckweeds. The Plant Cell. doi:10.1093/plcell/koac068",
                "Public Wolffia reference datasets already identified in this project and useful for assay benchmarking: PRJNA1124135 Wolffia scRNA-seq and PRJNA809022 Wolffia snRNA-seq",
            ],
            styles,
        )
    )

    story.append(
        Paragraph(
            "Reference use note: the papers above provide the biological context for Wolffia as a reduced but developmentally competent flowering plant. The exact dissociation chemistry for the first pilot should still be treated as a laboratory optimization variable unless a validated Wolffia or closely related duckweed workflow already exists locally.",
            styles["SmallNote"],
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
        title="Step-by-Step Protocol for Generating Wolffia Transcriptomic Data",
        author="OpenAI Codex",
    )
    doc.build(build_story())
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
