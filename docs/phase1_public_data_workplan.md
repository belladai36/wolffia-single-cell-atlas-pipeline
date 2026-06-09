# Phase 1 Workplan: Public Data Before Wolffia SMART-seq

## Goal

Use public reference datasets and existing Wolffia resources to build a testable prediction framework before any new Wolffia SMART-seq data arrive.

## Why This Phase Matters

This gives the project a strong scientific shape even before wet-lab data are available. Instead of waiting passively for sequencing, we can define what we expect to find, what would count as a surprise, and which future experiments would be most informative.

## Phase 1 Questions

1. which broad plant cell programs are most likely to be preserved in Wolffia?
2. which programs may be reduced, merged, or hard to separate?
3. which candidate Wolffia states might reflect aquatic adaptation rather than standard textbook cell types?
4. what signatures should we look for immediately once SMART-seq data arrive?

## Immediate Deliverables

### Deliverable 1: Reference Dataset Set

Assemble a small, high-confidence reference panel rather than too many datasets.

Target:

- 1 to 3 plant single-cell reference atlases
- at least one well-annotated angiosperm reference
- supporting Wolffia genomic or transcriptomic resources

Output files:

- `docs/reference_datasets.md`
- `docs/dataset_inventory.md`

### Deliverable 2: Candidate Program Framework

Define the first-pass biological programs we want to track in Wolffia.

Current categories:

- proliferative / meristematic
- epidermal / surface identity
- photosynthetic / assimilation
- vascular-like / transport
- developmental transition
- reproductive / floral
- aquatic adaptation / stress-responsive

Output files:

- `docs/candidate_cell_programs.md`

### Deliverable 3: Marker and Ortholog Table

Build a structured table that links:

- reference marker genes
- their biological roles
- Wolffia ortholog candidates
- mapping confidence
- expected Wolffia expression pattern

Output files:

- `data/metadata/reference_marker_template.csv`

### Deliverable 4: Prediction Table

Convert marker evidence into explicit predictions.

Each prediction should include:

- predicted state or program
- expected status in Wolffia
- evidence basis
- confidence
- expected SMART-seq outcome
- validation experiment

Output files:

- `docs/prediction_framework.md`
- a later structured prediction table

## Recommended Order of Work

### Step 1: Lock the Reference Set

Pick a compact set of public references that we trust enough to build on.

Success criterion:

- we can name the species, dataset, and why each one is useful

### Step 2: Fill the Marker Template

Start with broad, conservative marker programs rather than fine-grained cell labels.

Success criterion:

- each major candidate program has an initial marker list

### Step 3: Add Wolffia Mapping Notes

For each marker or pathway, record whether a plausible Wolffia counterpart exists and how confident we are.

Success criterion:

- every priority program has at least a first-pass mapping status

### Step 4: Write Testable Predictions

Translate descriptive biology into statements that future SMART-seq data can support or falsify.

Success criterion:

- each priority program has an explicit expected outcome

### Step 5: Draft Validation Experiments

Design follow-up experiments now so the project remains biologically grounded.

Success criterion:

- each major prediction has at least one feasible validation path

## First Priority for Us

The best immediate next move is:

1. finalize a compact reference panel
2. populate the marker template for the top four program categories
3. write first-pass predictions for those same categories

## What Counts as a Good Early Result

Even before real single-cell data, Phase 1 is successful if we can say:

- these are the cell programs most likely to exist in Wolffia
- these are the programs most likely to be merged or reduced
- these are the most interesting places where Wolffia may differ from model plants
- these are the first signatures we will test when SMART-seq data arrive

## Suggested Near-Term Milestone

By the end of the next work block, we should aim to have:

- a finalized short list of reference datasets
- a partially populated marker table
- first-pass predictions for 3 to 4 major cell programs

That would turn the project from an idea into an actual comparative research plan.
