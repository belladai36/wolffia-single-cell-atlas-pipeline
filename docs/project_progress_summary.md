# Project Progress Summary

## Project in One Sentence

This project is building a prediction-first single-cell analysis framework for `Wolffia australiana` so that we can make biologically meaningful hypotheses before new Wolffia `PIP-seq` data are available.

## Central Question

Can we use public plant single-cell datasets plus Wolffia biology to predict whether Wolffia preserves, reduces, merges, or compresses major flowering-plant cell programs?

## Current Stage

We are now at the **Wolffia-facing transfer preparation stage**.

That means:

- the Arabidopsis reference framework is working
- the broad program ontology has been refined several times
- the current program set is good enough to support a first Wolffia-facing pass
- the provisional 340-feature dual-model transfer rule is frozen for first application
- actual Wolffia training is waiting on download and preprocessing of public Wolffia data

## What We Have Completed

### 1. Core computational scaffold

The repo already supports:

- a legacy FASTQ QC, alignment, and counting route for per-cell raw-read workflows
- count matrix assembly
- Scanpy QC, clustering, marker analysis, and trajectory-style analysis
- public-reference transfer analysis for prediction-first work

Important note:

- the experimental platform now planned in the lab is `PIP-seq`
- the legacy STAR and featureCounts scaffold remains in the repo as a backup or custom-processing route, but it is no longer the main project identity

Main entry point:

- [README.md](../README.md)

### 2. Public reference transfer workflow

We built a public-reference statistical workflow that can:

- read public `.h5ad` reference datasets
- compute broad program scores
- collapse labels into interpretable biological programs
- train a simple classifier
- test transfer on a second dataset

Main script:

- [scripts/10_public_reference_statistical_prediction.py](../scripts/10_public_reference_statistical_prediction.py)

### 3. Arabidopsis validation phase

We tested the framework on several Arabidopsis datasets:

- `GSE227564` callus
- `GSE141730` root phosphate
- `GSE121619` root control/heat shock
- `GSE123818` broader root atlas

Key summaries:

- [Arabidopsis reference phase summary](arabidopsis_reference_phase_summary.md)
- [GSE121619 validation run summary](gse121619_validation_run_summary.md)
- [GSE123818 validation run summary](gse123818_validation_run_summary.md)

### 4. Root-derived reference improvement

We learned that training on callus over-collapsed many target cells into a stress-like sink.

Switching to a root-derived training reference improved biological interpretation substantially.

Key summary:

- [Root-derived reference update](root_derived_reference_update.md)

### 5. Broad program refinement

The broad program set has now been refined to include:

- `proliferative_or_meristematic`
- `photosynthetic_or_assimilation`
- `vascular_like_or_transport`
- `developmental_transition`
- `epidermal_or_surface_identity`
- `reproductive_or_floral`
- `transport_interface_or_water_balance`
- `abiotic_stress_response`

This is the current frozen working set for the first Wolffia-facing transfer pass.

### 6. Wolffia-facing interpretation layer

We updated the project so that first-pass Wolffia labels are treated as **transferable biological programs**, not literal Arabidopsis tissue identities.

Key docs:

- [Prediction framework](prediction_framework.md)
- [Wolffia mapping notes](wolffia_mapping_notes.md)
- [Wolffia first transfer note](wolffia_first_transfer_note.md)

### 7. Frozen provisional Wolffia transfer model

The cross-species model is restricted to 340 high- or medium-confidence reciprocal mappings. The
v1 rule requires calibrated logistic-regression and random-forest agreement, at least `0.60`
confidence from each model, and an explicit `ambiguous` result otherwise. High-confidence
biological annotation will additionally require independent marker-module and cluster evidence.

Key specification:

- [Frozen Wolffia transfer model v1](final_wolffia_transfer_model.md)

## Most Important Biological Lessons So Far

### 1. Reference choice matters a lot

Callus-trained references produced much less believable transfer behavior than root-derived references.

### 2. One giant stress bucket was misleading

The earlier `aquatic_adaptation_or_stress` category was too broad.

Splitting it into:

- `transport_interface_or_water_balance`
- `abiotic_stress_response`

gave a much more interpretable result.

### 3. Some plant programs transfer cleanly, others do not

The framework consistently recovers:

- proliferative programs
- photosynthetic programs

But vascular-like identity remains weak or partially merged at this broad level.

### 4. That is actually useful for Wolffia

This means future Wolffia results should not be over-interpreted as “novel” just because some classical programs appear weak, merged, or compressed.

## What We Have Not Completed Yet

We have **not** yet trained on real Wolffia data.

Why not:

- the two public Wolffia dataset directories exist only as placeholders right now
- no FASTQs or processed matrices are present locally
- the repo cannot train directly from empty `raw_fastq_dir` folders

Current Wolffia candidates:

- `PRJNA1124135` = first training candidate
- `PRJNA809022` = validation candidate

## Immediate Blocker

The real blocker is now **data availability and format**, not project design.

To proceed with real Wolffia training, we need:

1. download `PRJNA1124135` to larger storage
2. generate a count matrix or processed matrix
3. convert it into `.h5ad`
4. cluster and pseudo-label it
5. then validate on `PRJNA809022`

## Current Best Next Step

The next meaningful project step is:

1. obtain an external SSD
2. download the four `PRJNA1124135` scRNA runs
3. generate the first Wolffia count matrix
4. run the first Wolffia-facing transfer pass with the frozen broad program set

## Best Files for a New Viewer

If someone wants the shortest useful path through the repo, they should read:

1. [README.md](../README.md)
2. [Project aims](project_aims.md)
3. [Project progress summary](project_progress_summary.md)
4. [Root-derived reference update](root_derived_reference_update.md)
5. [Wolffia first transfer note](wolffia_first_transfer_note.md)

## Bottom Line

This project has moved beyond a vague idea.

It now has:

- a working computational scaffold
- validated Arabidopsis reference tests
- an improved broad-program ontology
- a Wolffia-facing interpretation framework
- a clear operational blocker and a clear next execution step

In short: the project is scientifically organized and computationally ready for the first real Wolffia dataset as soon as storage and download capacity are available.
