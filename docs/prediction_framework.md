# Prediction Framework for Wolffia Cell States

## Purpose

This document defines how we will move from public reference datasets to explicit, testable biological predictions for `Wolffia australiana`.

These predictions should increasingly be supported by quantitative analyses on existing public datasets, not only by literature interpretation.

## Framework Overview

### Step 1: Define Reference Cell Programs

From public plant single-cell references, identify marker genes and transcriptional programs for major plant cell states.

Outputs:

- marker gene lists
- summary of each reference cell state
- evidence level for each marker set

Current reference logic:

- use Arabidopsis root data first because its cell identities and marker genes are well established
- add Arabidopsis leaf or aerial-tissue data next because Wolffia is a highly reduced, photosynthetic plant body and may be better represented by leaf-like programs than root-specific labels

### Step 1b: Quantify Programs in Existing Data

Use public reference datasets to measure how strongly each broad program is recovered and how separable it is from other programs.

Example methods:

- module scoring
- logistic regression or random forest classification
- cluster separability metrics
- cross-dataset transfer testing
- pseudotime summary statistics

### Step 2: Map Markers to Wolffia

Translate reference markers into Wolffia candidate markers through ortholog mapping and annotation comparison.

Outputs:

- reference gene
- Wolffia ortholog candidate
- mapping confidence
- functional notes

### Step 3: Score Predicted Programs

For each candidate cell program, classify the expected status in Wolffia:

- `preserved`
- `partially preserved`
- `reduced`
- `merged`
- `missing`
- `uncertain`

Scoring should be based on:

- presence of orthologs
- robustness in public reference datasets
- conservation of multiple markers in the same pathway or program
- known morphology of Wolffia
- known duckweed adaptations

### Step 4: Build Biological Predictions

Each prediction should be phrased in a directly testable way.

Example structure:

- predicted state or process
- supporting evidence
- expected single-cell expression signature
- possible alternative explanation
- proposed validation experiment

## Prediction Categories

### Category A: Conserved Programs

Programs expected to remain clearly detectable despite morphological simplification.

Examples to evaluate:

- cell cycle and proliferative programs
- photosynthesis-associated programs
- basic epidermal identity programs

### Category B: Reduced or Merged Programs

Programs that may exist, but not as distinct clusters or cell identities.

Examples to evaluate:

- vascular-like signatures
- organ-boundary-like programs
- reproductive precursor programs

### Category C: Novel or Atypical Programs

Programs that may reflect aquatic adaptation or extreme body-plan reduction.

Examples to evaluate:

- stress-tolerant floating plant programs
- nutrient acquisition or aquatic adaptation signatures
- highly transitional developmental states

## Validation Logic

When Wolffia single-cell data arrive, predictions will be checked by asking:

1. do clusters or gradients support the predicted states?
2. do predicted marker genes co-occur in the same cells or states?
3. are conserved programs clearly separable or collapsed together?
4. do unexpected clusters suggest genuinely novel Wolffia biology?
5. do interface/water-balance signatures separate from true abiotic-stress signatures?

## Follow-Up Experiments

Predictions should lead naturally to specific validation strategies:

- targeted marker validation by qRT-PCR
- RNA in situ or other spatial assays if feasible
- microscopy guided by predicted cell states
- perturbation experiments such as hormone, nutrient, or stress treatments

## Final Deliverable

The final product of this framework should be a prediction table with columns such as:

- predicted cell state
- reference evidence
- Wolffia support
- prediction confidence
- expected single-cell data outcome
- validation experiment
- interpretation if prediction fails

## First-Pass Prediction Table

The table below converts the current reference panel and Wolffia mapping notes into explicit, testable predictions.

| predicted_program | expected_status_in_wolffia | supporting_evidence | prediction_confidence | expected_pip_seq_outcome | alternative_explanation | proposed_validation |
|---|---|---|---|---|---|---|
| Proliferative / meristematic program | preserved | core cell-cycle machinery is broadly conserved across flowering plants; Wolffia must retain actively growing cells | high | one cluster or small group of cells enriched for cell-cycle, DNA replication, and histone-associated genes | sampled tissue lacked actively dividing cells, or sequencing depth was too shallow to separate a proliferative population | qRT-PCR for division-associated markers and microscopy focused on actively growing regions |
| Photosynthetic / assimilation program | preserved | Wolffia is a photosynthetic plant and should retain chloroplast- and carbon-fixation-associated transcriptional programs | high | a large assimilation-associated state enriched for LHCB-, RBCS-, and plastid-related expression | photosynthetic signal is broad across most cells and does not resolve into a distinct cluster because the plant body is highly reduced | targeted expression assay for photosynthesis-related genes across growth conditions and microscopy of chloroplast-rich tissues |
| Vascular-like / transport program | partially preserved or merged | transport genes are likely present, but morphology suggests reduced specialization relative to larger angiosperms | medium | transport-associated markers appear either in a weak subcluster or as a mixed signature embedded within another major state | transport functions are distributed across multifunctional cells rather than specialized cell identities | qRT-PCR panel for transporter candidates plus anatomical imaging or section-based localization if feasible |
| Developmental transition program | preserved as a continuum rather than discrete cell type | developmental trajectory references suggest transitional states may be more informative than strict labels | medium to high | gradual expression shifts, pseudotime structure, or partially overlapping marker programs rather than many sharply separated clusters | limited cell number or technical noise may blur true discrete states | trajectory re-analysis, hormone perturbation experiments, and follow-up marker testing across induced developmental conditions |
| Epidermal / surface identity program | reduced or weakly separable | surface-associated programs may still exist, but Wolffia body-plan reduction may weaken layer-specific specialization | medium | subtle enrichment of surface markers, possibly without a clean standalone cluster | surface functions may be merged with photosynthetic or stress-responsive states | targeted marker assay for surface-identity candidates and microscopy-based surface characterization |
| Reproductive / floral program | condition-specific or absent in baseline samples | floral regulators are biologically relevant but unlikely to be active in ordinary vegetative sampling | low | no strong reproductive cluster in baseline single-cell data, or only rare cells with floral-transition markers | flowering may require specific induction conditions not represented in the sampled material | compare induced or flowering-enriched samples if available |
| Transport / interface / water-balance program | present as a broad interface-associated program | Wolffia aquatic lifestyle likely requires strong membrane, aquaporin, and water-balance regulation that does not map neatly to standard organ labels | medium to high | one broad state or gradient enriched for aquaporin-like, membrane-interface, or water-flux-associated signatures | interface-associated biology may overlap partly with general transport or surface programs | osmotic or nutrient-shift experiments and targeted validation of aquaporin-like modules |
| Abiotic stress-response program | present as a state-like response rather than stable cell type | redox, heat, cold, dehydration, or handling-associated stress programs may appear as real but dynamic signatures | medium | subset-specific or condition-specific signatures enriched for stress-response markers | observed stress signatures may reflect dissociation or handling artifacts rather than stable endogenous states | perturbation experiments with oxidative, osmotic, heat, or cold treatments and targeted validation of responsive modules |

## Interpretation Priority

The first four predictions should drive the earliest analysis once Wolffia single-cell data arrive:

1. proliferative / meristematic
2. photosynthetic / assimilation
3. vascular-like / transport
4. developmental transition

These are the categories most likely to tell us whether Wolffia simplification reflects:

- retention of core programs
- compression of canonical programs into fewer states
- or a more continuous developmental organization than in larger model plants

## Statistical Extension

Prediction in this project should now be interpreted in two layers:

1. biological prediction:
   what programs we think Wolffia should retain, merge, reduce, or rework
2. statistical prediction:
   what structures are consistently recoverable in existing public plant single-cell data and therefore most likely to transfer to Wolffia

The companion document [Statistical prediction strategy](statistical_prediction_strategy.md) defines the quantitative layer of this plan.

## Root-Versus-Leaf Reference Extension

The next refinement is to compare the frozen root-derived reference view with an Arabidopsis leaf or aerial-tissue reference view.

This comparison will test whether the current conservative result is mostly caused by:

- true compression of plant programs in Wolffia
- mismatch between a root reference and a photosynthetic Wolffia body plan
- or insufficient public-reference coverage of surface, mesophyll-like, and aquatic-interface programs

The working plan is documented in [Arabidopsis leaf reference extension plan](leaf_reference_extension_plan.md).
