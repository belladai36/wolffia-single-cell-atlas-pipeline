# Prediction Framework for Wolffia Cell States

## Purpose

This document defines how we will move from public reference datasets to explicit, testable biological predictions for `Wolffia australiana`.

## Framework Overview

### Step 1: Define Reference Cell Programs

From public plant single-cell references, identify marker genes and transcriptional programs for major plant cell states.

Outputs:

- marker gene lists
- summary of each reference cell state
- evidence level for each marker set

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
- conservation of multiple markers in the same pathway or program
- known morphology of Wolffia
- known duckweed adaptations

### Step 4: Build Biological Predictions

Each prediction should be phrased in a directly testable way.

Example structure:

- predicted state or process
- supporting evidence
- expected SMART-seq signature
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

When SMART-seq data arrive, predictions will be checked by asking:

1. do clusters or gradients support the predicted states?
2. do predicted marker genes co-occur in the same cells or states?
3. are conserved programs clearly separable or collapsed together?
4. do unexpected clusters suggest genuinely novel Wolffia biology?

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
- expected SMART-seq outcome
- validation experiment
- interpretation if prediction fails
