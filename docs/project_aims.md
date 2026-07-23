# Project Aims: Prediction-First Wolffia Cell Atlas

## Working Title

Comparative prediction of cell states and developmental programs in `Wolffia australiana`

## Project Motivation

`Wolffia australiana` is an extremely morphologically simplified flowering plant. Because it lacks many obvious organs seen in larger angiosperms, it is an interesting system for asking whether developmental simplification at the organism level is matched by simplification at the cellular and transcriptional levels.

At the moment, the most realistic path is a prediction-first project:

1. use public plant single-cell references and Wolffia genomic resources to generate hypotheses
2. start with well-annotated Arabidopsis root data as a conservative benchmark
3. prioritize Arabidopsis leaf or aerial-tissue references as the main Wolffia-facing biological layer because Wolffia is reduced, photosynthetic, and not root-like
4. use statistical analyses on public single-cell references to quantify broad cell programs and their separability
5. define candidate cell states and marker programs expected in Wolffia
6. use incoming Wolffia single-cell expression data to test and refine those predictions

## Central Question

Can we predict the cellular organization of `Wolffia australiana` by integrating public plant single-cell references with Wolffia genomic and transcriptomic resources, and then test those predictions with future Wolffia single-cell expression data?

## Specific Aims

### Aim 1

Build a curated reference framework of plant cell states using public single-cell RNA-seq datasets from better-annotated species.

Near-term refinement:

- keep the Arabidopsis root atlas as the first benchmark because root markers are well established
- build an Arabidopsis leaf or aerial-tissue matrix into the primary reference layer because Wolffia is expected to be more photosynthetic and frond-like than root-like

### Aim 2

Map conserved marker programs from reference species to `Wolffia australiana` using ortholog relationships and available Wolffia resources.

### Aim 3

Use statistical analyses on public reference data to estimate which broad cell programs are stable, transferable, and likely to remain detectable in `Wolffia australiana`.

### Aim 4

Generate explicit predictions about which cell states and developmental programs are likely to be:

- preserved
- reduced
- merged
- absent
- novel or ambiguous

### Aim 5

Design computational validation analyses for future Wolffia single-cell data.

Near-term update:

- prepare the pipeline to analyze incoming Wolffia single-cell count matrices as soon as counts or processed matrices are available

## Biological Hypotheses

### Hypothesis 1

`Wolffia` retains core angiosperm developmental programs, but these programs may be compressed into fewer transcriptional states.

### Hypothesis 2

Some canonical organ-associated programs from model plants may be reduced or partially merged because of Wolffia's simplified morphology.

### Hypothesis 3

`Wolffia` may contain aquatic or highly reduced plant-specific transcriptional states that do not map cleanly onto standard Arabidopsis cell type labels.

### Hypothesis 4

Future single-cell data may reveal a continuum of developmental states rather than many sharply separated cell types.

## Expected Outputs

- a written comparative framework for Wolffia cell-state prediction
- a curated marker-gene reference table
- an ortholog-mapped Wolffia candidate marker table
- a ranked list of predicted Wolffia cell programs
- a root-versus-leaf Arabidopsis reference comparison
- a leaf-prioritized interpretation rule for future Wolffia predictions
- a statistical summary of which public plant programs are most robust and transferable
- a validation plan for downstream computational analysis

## Success Criteria

This summer project will be successful if it produces a credible, testable hypothesis framework that can guide interpretation of future Wolffia single-cell expression data rather than waiting for the sequencing results before asking biological questions.
