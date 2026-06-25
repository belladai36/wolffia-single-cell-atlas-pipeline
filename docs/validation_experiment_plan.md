# Validation Experiment Plan for Wolffia Predictions

## Purpose

This document completes Phase 1 Step 5 by translating first-pass predictions into feasible validation strategies.

The goal is not to lock in one experimental design too early. It is to make sure each computational prediction already points toward a concrete biological follow-up.

## Validation Principles

1. start with simple, feasible assays before high-complexity validation
2. validate broad programs before fine-grained cell labels
3. interpret negative results carefully, especially when a program may be condition-specific or technically hard to recover
4. use perturbation logic when a predicted state may be dynamic rather than a fixed cell identity

## Program-by-Program Validation Plan

### 1. Proliferative / Meristematic Program

Prediction:

- Wolffia should retain a detectable proliferative program.

Primary validation:

- qRT-PCR or targeted expression assay for cell-cycle and replication-associated markers

Secondary validation:

- microscopy focused on actively growing regions or budding structures

What success would look like:

- division-associated markers are enriched in samples expected to contain active growth

What failure would mean:

- either proliferative cells were rare in the sampled material or the program is less spatially restricted than expected

### 2. Photosynthetic / Assimilation Program

Prediction:

- Wolffia should show a strong photosynthetic transcriptional program, possibly broad rather than sharply localized.

Primary validation:

- targeted expression assay for photosynthesis-associated genes such as light-harvesting and carbon-fixation candidates

Secondary validation:

- microscopy of chloroplast-rich tissues
- condition comparisons such as light intensity or growth stage

What success would look like:

- reproducible enrichment of photosynthesis-related markers

What failure would mean:

- either the annotation of photosynthetic genes is incomplete or the program is too globally distributed to act as a discrete cell-state marker

### 3. Vascular-Like / Transport Program

Prediction:

- transport-associated functions may be present, but could be merged into broader multifunctional states.

Primary validation:

- qRT-PCR panel for transporter candidates such as sugar or solute transport families

Secondary validation:

- anatomical or section-based localization if feasible
- comparison across nutrient or transport-demand conditions

What success would look like:

- a reproducible transport-related expression module, even if it does not define a clean cluster

What failure would mean:

- transport functions may be broadly distributed or may not align with canonical vascular labels in Wolffia

### 4. Developmental Transition Program

Prediction:

- Wolffia may organize part of its developmental biology as gradients or continua rather than sharply discrete cell types.

Primary validation:

- computational re-analysis of trajectory structure once `PIP-seq` data arrive

Secondary validation:

- hormone perturbation experiments, especially auxin-related treatments
- sampling across developmental time or growth conditions

What success would look like:

- reproducible pseudotime structure and gradual transitions among marker programs

What failure would mean:

- either states are more discrete than expected or the dataset lacks the dynamic range needed to recover transitions

### 5. Epidermal / Surface Identity Program

Prediction:

- surface-associated programs may exist but be weakly separated.

Primary validation:

- targeted assay for broad surface-identity markers

Secondary validation:

- microscopy-based comparison of outer versus inner tissue features if resolvable

What success would look like:

- modest but reproducible enrichment of candidate surface markers

What failure would mean:

- surface-associated biology may be transcriptionally merged with other programs in Wolffia

### 6. Reproductive / Floral Program

Prediction:

- floral or reproductive regulators are likely absent from baseline vegetative datasets unless induction conditions are used.

Primary validation:

- targeted expression assay under flowering-induction or stress-induction conditions

Secondary validation:

- repeat `PIP-seq` or bulk expression profiling after induction

What success would look like:

- reproductive regulators appear only under specific conditions

What failure would mean:

- either induction was insufficient or Wolffia reproductive transitions are rarer or differently regulated than expected

### 7. Aquatic Adaptation / Stress-Responsive Program

Prediction:

- aquatic or stress-responsive programs may behave as dynamic states rather than classic cell types.

Primary validation:

- perturbation experiments involving nutrient, osmotic, redox, or other aquatic-relevant conditions

Secondary validation:

- targeted expression assays for aquaporin-like and stress-response modules

What success would look like:

- condition-dependent activation of predicted aquatic or stress modules

What failure would mean:

- either the chosen perturbations missed the relevant biology or the inferred signatures were technical artifacts

## Ranked Validation Priority

Best early validation targets:

1. proliferative / meristematic
2. photosynthetic / assimilation
3. vascular-like / transport
4. developmental transition

These are the best starting points because they are:

- biologically central
- interpretable even with coarse labels
- likely to be informative whether they succeed or fail

## Practical Next Use

Once Wolffia `PIP-seq` data arrive, this validation plan should be used alongside the prediction table to decide:

- which signatures to check first
- which negative results are meaningful
- and which follow-up wet-lab experiments would most strongly test the computational model
