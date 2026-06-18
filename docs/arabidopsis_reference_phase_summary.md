# Arabidopsis Reference Phase Summary

## What we completed

We used two public Arabidopsis single-cell datasets as a reference-and-transfer system before moving to large public Wolffia files.

- Training reference: `GSE227564_callus`
- Transfer target: `GSE141730_root_phosphate`
- Main script: [scripts/10_public_reference_statistical_prediction.py](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/scripts/10_public_reference_statistical_prediction.py)
- Marker panel: [data/metadata/public_reference_program_markers.csv](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/data/metadata/public_reference_program_markers.csv)

## Important improvement

The earlier version of this workflow trained on raw numeric cluster labels such as `0`, `1`, and `12`.

That was useful for testing the code path, but it was not biologically interpretable.

We fixed that by:

1. expanding the marker file so that each marker has both a gene symbol and an Arabidopsis locus ID
2. resolving markers against either gene symbols or AGI-style locus IDs in each dataset
3. scoring broad programs in the training dataset
4. collapsing training clusters into broad biological programs based on dominant module scores

## Broad programs used

- `proliferative_or_meristematic`
- `photosynthetic_or_assimilation`
- `vascular_like_or_transport`
- `developmental_transition`
- `epidermal_or_surface_identity`
- `reproductive_or_floral`
- `aquatic_adaptation_or_stress`

## Marker recovery

The updated marker panel now resolves cleanly in both Arabidopsis datasets.

Examples:

- `CYCB1;1 -> AT4G37490`
- `PCNA1 -> AT1G07370`
- `LHCB1.1 -> AT1G29910`
- `SUC2 -> AT1G22710`
- `PLT1 -> AT3G20840`
- `IAA19 -> AT3G15540`
- `ATML1 -> AT4G21750`
- `ZAT12 -> AT5G59820`

This matters because the training dataset stores features mostly as locus IDs, while the test dataset stores many of them as gene symbols.

## Training cluster collapse

The training callus clusters were reassigned into broad programs from module-score summaries.

The strongest examples were:

- cluster `9` -> `epidermal_or_surface_identity`
- clusters `14`, `16`, `18` -> `proliferative_or_meristematic`
- cluster `13` -> `developmental_transition`
- clusters `1`, `4` -> `photosynthetic_or_assimilation`
- many clusters -> `aquatic_adaptation_or_stress`

The current collapsed training distribution is:

- `aquatic_adaptation_or_stress`: `2111` cells
- `proliferative_or_meristematic`: `706` cells
- `photosynthetic_or_assimilation`: `573` cells
- `epidermal_or_surface_identity`: `217` cells
- `reproductive_or_floral`: `216` cells
- `developmental_transition`: `164` cells

No substantial `vascular_like_or_transport` cluster survived as a dominant broad program in this training reference.

## Transfer result on the second Arabidopsis dataset

After retraining on broad programs, the predictions on `GSE141730_root_phosphate` were:

- `aquatic_adaptation_or_stress`: `1644` cells
- `photosynthetic_or_assimilation`: `295` cells
- `proliferative_or_meristematic`: `31` cells
- `developmental_transition`: `22` cells
- `reproductive_or_floral`: `8` cells

This is not a final statement about the biology of the phosphate dataset.

It is a transfer-learning result that tells us which broad transcriptional programs from the training reference are most compatible with the target dataset.

## Working interpretation

At the current stage, the reference workflow supports these conclusions:

1. broad plant transcriptional programs can be recovered across public datasets
2. program transfer is much more interpretable after replacing numeric train labels with biologically named states
3. the current Arabidopsis test dataset maps mostly to a stress-like or adaptive transcriptional regime, with smaller assimilation and proliferative components
4. some classical plant programs are not strongly separable in the training reference, which is exactly the kind of pattern we want to test later in Wolffia

## What this means for Wolffia

This Arabidopsis-only phase already gives us a prediction logic for Wolffia:

- clearly preserved programs should transfer robustly and form dominant score patterns
- weakly separable programs should appear, but not as crisp clusters
- merged or compressed programs should show overlapping marker scores across the same cells
- missing or ambiguous mappings should remain low-confidence during transfer

That sets up the next real Wolffia question:

> does Wolffia preserve major flowering-plant programs, weaken their separation, or compress several canonical programs into fewer multifunctional states?

## Next computational step

The best next move is to keep the Arabidopsis reference system as the training scaffold while we wait for larger storage for Wolffia public data.

Concretely:

1. refine the broad program marker sets
2. add one or more additional Arabidopsis validation datasets with stronger annotation
3. compare whether program compression is dataset-specific or repeatedly observed
4. then transfer the same framework onto public Wolffia references once external storage is available

The current validated candidate list and recommended order are documented in:

- [docs/arabidopsis_validation_dataset_selection.md](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/docs/arabidopsis_validation_dataset_selection.md)
- [data/metadata/arabidopsis_public_dataset_manifest.csv](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/data/metadata/arabidopsis_public_dataset_manifest.csv)
