# Protocol for Generating New Wolffia Transcriptomic Data

## Title

Stepwise pilot-to-discovery protocol for generating a first `Wolffia australiana`
single-cell or single-nucleus transcriptomic dataset

## Purpose

This protocol is designed to generate a first Wolffia dataset that is good enough to:

- recover broad transcriptional programs reproducibly
- distinguish biological structure from preparation artifacts
- support the first Wolffia-native atlas analysis

The central operational question is:

> which upstream input route gives cleaner Wolffia transcriptomes: intact cells or nuclei?

For that reason, this is a **staged protocol** with a pilot comparison before any larger sequencing run.

## Scope

This protocol covers:

1. Wolffia culture standardization
2. pre-harvest QC
3. matched pilot comparison of intact-cell and nuclei preparation
4. route-selection criteria
5. execution of the first full Wolffia discovery run
6. required post-sequencing QC readouts

It does **not** claim one universally optimal recipe for every Wolffia line or platform. However, it does include a literature-based **benchmark intact-cell workflow** that can be used as the first pilot starting point for `Wolffia australiana`.

## Experimental principle

Because plant single-cell experiments frequently fail at the sample-preparation stage, the first experiment should maximize:

- biological consistency
- handling speed
- sterility
- low-stress preparation
- reproducibility across replicates

The first experiment should **not** try to solve every developmental condition at once.

## Recommended baseline biological design

Use:

- one Wolffia line or stock
- one baseline vegetative growth condition
- three biological replicates for the first real run
- one fixed harvest window within the light cycle

For a first-pass standardization condition, cultivate Wolffia:

- as an **axenic liquid culture** if possible
- in the lab's established duckweed maintenance medium for that line
- under a **stable light-dark cycle**
- at a **stable room-temperature or growth-chamber temperature**
- with minimal crowding, visible stress, or contamination

If the line is already maintained successfully in the lab, keep the maintenance environment unchanged during the pilot phase unless there is a strong reason to switch. The most important rule is consistency, not unnecessary re-optimization.

## Recommended starting culture environment

If a local standard already exists, use that standard.

If no local standard exists, use the following as a **recommended benchmark baseline** adapted from the `Wolffia australiana` workflow reported in *Genome Research* (2024):

- axenic liquid culture
- `0.5x` Schenk and Hildebrandt medium
- `0.1%` sucrose
- medium adjusted to `pH 6.7`
- `12-hour light / 12-hour dark` photoperiod
- `24 C` growth temperature
- approximately `100 uE` light intensity
- weekly subculture by transferring about `10 fronds`
- harvest at the same time of day for all matched replicates
- if following the published benchmark closely, use `200 to 300` plants per sample and avoid very old material

These values are intended as a practical benchmark for pilot work, not as a claim that every Wolffia line must be grown under one universal condition.

## Required materials and equipment

### Culture and sampling

- healthy Wolffia stock
- growth medium
- sterile culture vessels
- sterile pipettes and tips
- sterile forceps or sampling tools
- metadata sheet or electronic sample log

### Pre-harvest QC

- brightfield microscope or stereomicroscope
- imaging device
- optional balance for wet-weight estimation

### Intact-cell pilot

- fresh sterile razor blade or similarly fine disruption tool
- osmotic stabilization buffer
- plant cell-wall digestion reagents
- `100 um` sieve or mesh filter
- `40 um` cell strainer
- low-speed centrifuge
- hemocytometer or automated counter
- optional viability dye

### Nuclei pilot

- ice bucket or cold block
- nuclei isolation buffer
- gentle homogenization setup such as a Dounce homogenizer
- mesh filters or strainers
- refrigerated centrifuge
- nuclei counting setup
- optional DNA stain

### Library preparation and sequencing

- chosen library-prep kit or core-facility workflow
- low-bind tubes
- RNase-free plastics
- PCR or amplification equipment as required by the platform
- library quantification system
- sequencing core or sequencing platform access
- written platform specifications from the core or lab for acceptable input concentration, loading range, and cleanup expectations

## Metadata that must be recorded for every sample

- sample ID
- biological replicate ID
- stock or genotype ID
- medium
- temperature
- photoperiod
- harvest date and time
- operator
- prep route: cell or nucleus
- preparation condition ID
- viability or nuclei-integrity observation
- library batch
- sequencing batch

## Protocol

## Step 1: Establish and stabilize Wolffia cultures

1. Start with one Wolffia line or stock only.
2. Grow the material under one defined baseline vegetative condition.
3. Maintain the same medium, light schedule, and temperature across all pilot cultures.
4. Avoid mixing very old and very young cultures in the same experimental batch.
5. Keep a culture log for at least several days before harvest.

### Output

- healthy, standardized Wolffia cultures
- stable maintenance conditions
- clear metadata records

## Step 2: Perform pre-harvest culture QC

1. Inspect representative fronds by brightfield microscopy or stereomicroscopy.
2. Record visible morphology, frond size, budding status, and contamination.
3. Estimate available biomass by frond count, wet weight, or both.
4. Exclude cultures that are obviously stressed, contaminated, senescent, or highly heterogeneous.

### Go / no-go rule

Proceed only if the cultures are:

- visibly healthy
- reasonably uniform
- free of obvious contamination
- sufficient in biomass for a split pilot

## Step 3: Harvest fresh Wolffia fronds or pooled plant material

In this protocol, "tissue" means the harvested Wolffia material itself: usually pooled fronds or pooled whole plants from culture, not a large leaf or organ.

1. Harvest fronds or pooled plant material gently to avoid unnecessary mechanical damage.
2. Use the same harvest method and timing for all matched pilot samples.
3. Minimize the time between harvest and the start of preparation.
4. For nuclei preparations, place the harvested material on ice immediately after harvest.
5. For intact-cell preparations, move the harvested material rapidly into the chosen wash or stabilization buffer.

### Critical rule

Record the harvest-to-processing time for every sample.

## Step 4: Split the matched pilot into two preparation routes

From the same starting biological material, divide the sample into:

- Route A: intact-cell preparation
- Route B: nuclei preparation

The purpose of the pilot is technical comparison, not biological comparison.

## Step 5A: Intact-cell preparation pilot

### Goal

Recover intact, viable single cells with minimal preparation-induced stress.

### Practical starting workflow

1. Rinse freshly harvested Wolffia briefly to remove residual medium.
2. If using the published `Wolffia australiana` benchmark route, collect a pooled sample of about `200 to 300` plants and gently dice the pooled fronds or whole plants with a fresh sterile razor blade. This step is used to improve enzyme access through the thick waterproof cuticle; it does **not** mean trying to cut one tiny plant at a time.
3. Transfer the diced plant material into a benchmark digestion solution containing `0.1 M KCl`, `0.02 M MgCl2`, `0.1% BSA`, `0.08 M MES`, `0.6 M mannitol`, adjusted to `pH 5.5`, plus `1.5% cellulase R-10`, `1% maceroenzyme`, and `0.5% pectolyase`.
4. Incubate under gentle agitation, keeping the shaker below `200 rpm`, for a short pilot time course that does not exceed about `90 minutes` unless the lab deliberately tests a longer condition.
5. Filter the digest first through a `100 um` sieve and then through a `40 um` cell strainer to remove large debris.
6. Wash the recovered cells in the same buffer formulation without enzymes.
7. Pellet and wash using gentle centrifugation consistent with the benchmark route, for example an initial spin near `1000 g` at `20 C` followed by a later wash near `500 g` at `20 C`.
8. Resuspend the final pellet in about `500 uL` wash buffer, minimize total washing time, and aim to finish the wash steps within about `30 minutes`.
9. Count cells immediately by light microscopy and hemocytometer, inspect morphology, and measure viability if the workflow supports it.

### Pilot variables to compare

Do not assume one final condition on day one. Start close to the published benchmark, then compare a small matrix such as:

- shorter versus longer digestion time
- lower versus moderate enzyme strength
- with versus without gentle agitation
- with versus without a pre-infiltration step if the lab routinely uses one
- whole-frond handling versus gentle razor dicing if the lab wants to test whether cutting is truly necessary for its line and growth condition

### What must be measured

- total recovered cell count
- cell concentration
- viability
- visible clumping
- debris burden
- approximate time from harvest to stabilization

### Success criteria

- reproducible recovery of intact-looking cells
- acceptable viability
- manageable debris
- limited clumping

### Failure criteria

- mostly broken material
- very low viability
- extreme clumping
- very low yield
- harsh treatment required just to recover any cells

If the failure criteria dominate, do not force the cell route. Continue with the nuclei route as the likely preferred option.

## Step 5B: Nuclei preparation pilot

### Goal

Recover clean, intact single nuclei while avoiding the stress burden of full wall digestion.

### Practical starting workflow

1. Keep freshly harvested Wolffia cold from the start of processing.
2. Transfer the harvested plant material into a cold nuclei isolation buffer.
3. Homogenize gently just enough to release nuclei.
4. Filter the homogenate to remove large debris.
5. Pellet and wash nuclei carefully under cold conditions.
6. Count nuclei and inspect nuclear integrity.
7. If appropriate, use a standard nuclei stain for counting or gating.

### What must be measured

- nuclei count
- clumping
- visible nuclear integrity
- debris burden
- apparent plastid carryover
- apparent ambient contamination

### Success criteria

- clean single nuclei
- reproducible yield
- manageable debris
- better overall sample quality than the cell route

### Failure criteria

- extensive rupture
- severe aggregation
- extreme contamination
- very poor recovery

## Step 6: Choose the route for the full experiment

Select the route using evidence, not preference.

### Choose the intact-cell route if

- viable cell recovery is reproducible
- debris and clumping are manageable
- the preparation does not appear excessively harsh
- the route is likely to preserve real biological structure

### Choose the nuclei route if

- the cell route is harsh, inconsistent, or low-yield
- nuclei are clearly cleaner and more reproducible
- the fronds or pooled plant material appear difficult to dissociate cleanly as intact cells

## Step 7: Run the first full Wolffia discovery experiment

Once a route is selected, lock the upstream preparation and run the first full experiment with:

- one defined vegetative condition
- three biological replicates
- one fixed preparation route
- one fixed library-prep workflow

### Sample-design rule

The first full experiment should remain simple.

Do **not** combine:

- multiple perturbations
- mixed developmental conditions
- rare-state enrichment schemes

until a clean baseline Wolffia reference exists.

## Step 8: Prepare libraries and sequence

1. Use the selected input type consistently across all replicates.
2. Keep library preparation as uniform as possible across replicates.
3. Sequence replicates in a balanced way to avoid obvious batch imbalance.
4. Prioritize library quality and replicate consistency over scale inflation.

### Important note

If the lab uses `PIP-seq`, the most important Wolffia-specific optimization still remains **upstream preparation quality**. In practice, that means:

- confirm with the lab or core whether the `PIP-seq` run expects intact cells, nuclei, or can support both
- deliver a low-clump, low-debris suspension rather than chasing the largest possible yield
- stay within the platform's required concentration or loading window
- keep replicate handling and barcoding uniform across the whole run
- record any cleanup, enrichment, or loading deviations because they may matter later during interpretation

If the lab later uses another lower-throughput workflow instead of `PIP-seq`, the same rule still applies: clean input biology comes first.

## Step 9: Perform immediate post-sequencing QC

As soon as sequencing data are available, evaluate:

- reads per cell or per nucleus
- genes detected per cell or per nucleus
- organellar fraction
- ambient-RNA-like background
- probable doublet burden
- replicate mixing
- stress-like artifact burden
- stability of recovered clusters or neighborhoods

### Minimum biological success criterion

The experiment is successful if it recovers at least some broad expected programs in a reproducible way, such as:

- proliferative or meristematic signal
- photosynthetic or assimilation signal
- transport or interface-associated signal
- developmental transition-like signal

Fine-grained cell labels are not required for the first run to be useful.

## Step 10: Decide on the next experiment

Only after the first clean baseline dataset exists should the project move to:

- developmental contrasts
- light or nutrient perturbations
- osmotic or water-balance experiments
- flowering or reproductive induction designs

## What not to do

Avoid the following mistakes in the first Wolffia experiment:

- changing culture conditions immediately before harvest
- harvesting stressed or mixed-quality material
- forcing an intact-cell route when nuclei are clearly cleaner
- over-optimizing indefinitely without generating a real test dataset
- over-interpreting technical stress as novel Wolffia biology

## Recommended timeline

### Week 1

- standardize cultures
- finalize metadata tracking

### Week 2

- run matched intact-cell and nuclei pilots

### Week 3

- choose the cleaner route
- repeat the chosen route on fresh material if needed

### Week 4

- prepare the first full libraries
- submit sequencing

### Week 5 onward

- run computational QC and first-pass biological interpretation

## Bottom line

The best first Wolffia transcriptomic experiment is the cleanest one:

- stable vegetative cultures
- matched pilot comparison of cells versus nuclei
- evidence-based route selection
- three biological replicates
- immediate computational QC after sequencing

That is the fastest scientifically defensible route to a usable Wolffia-native reference.

## References

1. Park J. et al. Genome of the world's smallest flowering plant, `Wolffia australiana`, helps explain its specialized physiology and unique morphology. *Communications Biology* (2021). DOI: `10.1038/s42003-021-02389-w`
2. Hoang P.T.N. et al. The genome of `Wolffia australiana` facilitates discovery of genetic basis for aquatic adaptation in duckweeds. *The Plant Cell* (2022). DOI: `10.1093/plcell/koac068`
3. Wu Y. et al. Streamlined spatial and environmental expression signatures characterize the minimalist duckweed `Wolffia australiana`. *Genome Research* 34(7):1106-1122 (2024). DOI: `10.1101/gr.279091.124`
4. Public Wolffia reference datasets already identified in this project and useful for assay benchmarking:
   - `PRJNA1124135` Wolffia scRNA-seq
   - `PRJNA809022` Wolffia snRNA-seq

## Reference use note

The Wolffia papers above provide the biological context for why Wolffia is a compelling and unusual system. The 2024 *Genome Research* paper also provides a strong benchmark starting point for culture conditions and protoplast preparation. Even so, the exact dissociation chemistry for your own line, growth state, and library platform should still be treated as a laboratory optimization variable unless your lab or sequencing core already has a validated plant single-cell or plant nuclei workflow that can be adapted directly.
