# Root-Derived Reference Update

We tested whether the dominant stress-like transfer pattern was mainly caused by the current training reference rather than by the target datasets themselves.

## What Changed

Instead of training on the callus dataset `GSE227564`, we:

1. converted `GSE123818 WT` into a local `.h5ad`
2. clustered it with [scripts/17_cluster_public_reference.py](../scripts/17_cluster_public_reference.py)
3. assigned broad programs to `WT` clusters by marker-score dominance
4. used that clustered root atlas as the new training reference

New configs:

- [config/public_reference_gse123818_wt_train_to_shr.yaml](../config/public_reference_gse123818_wt_train_to_shr.yaml)
- [config/public_reference_gse123818_wt_train_to_gse121619.yaml](../config/public_reference_gse123818_wt_train_to_gse121619.yaml)

## Main Comparison

### Old reference: callus -> root atlas

`GSE227564 callus -> GSE123818 WT`

- stress-like: `95.17%`
- developmental transition: `2.57%`
- proliferative: `1.33%`

`GSE227564 callus -> GSE123818 SHR`

- stress-like: `94.45%`
- photosynthetic: `3.28%`
- developmental transition: `1.91%`

### New reference: root WT -> root targets

`GSE123818 WT -> GSE123818 SHR`

- stress-like: `50.23%`
- photosynthetic: `29.75%`
- reproductive/floral: `13.01%`
- proliferative: `7.01%`

`GSE123818 WT -> GSE121619`

- proliferative: `52.20%`
- stress-like: `40.50%`
- reproductive/floral: `7.05%`
- photosynthetic: `0.25%`

## Marker-Refinement Rerun

We then refined the broad-program marker panel to make it more root-aware and tightened the cluster pseudo-label thresholds:

- expanded proliferative markers
- expanded vascular markers
- expanded developmental-transition markers
- replaced weak epidermal markers with more root-relevant epidermal markers
- expanded stress markers
- required a minimum top score of `0.05`
- required a minimum score margin of `0.02`

### Refined `WT -> SHR`

- stress-like: `93.81%`
- proliferative: `6.19%`

### Refined `WT -> GSE121619`

- stress-like: `76.75%`
- proliferative: `23.25%`

### What improved

- spurious `reproductive_or_floral` transfer disappeared
- spurious photosynthetic transfer into root-heavy targets disappeared
- low-signal or ambiguous training clusters were more often marked `unmapped`

### What got worse

- the dominant stress-like mapping returned strongly
- root-state diversity became less visible in the final transfer output

This means the stricter thresholds helped remove obvious annotation artifacts, but the current `aquatic_adaptation_or_stress` module is still too broad and is capturing too much of the root atlas.

## Interpretation

This is the clearest sign yet that the original stress-dominant outcome was heavily influenced by the training reference.

Moving from a callus reference to a root-derived reference:

- sharply reduced the near-total stress collapse in `GSE123818 SHR`
- changed the cross-study `GSE121619` transfer from mostly stress-like to a mixed proliferative-plus-stress pattern
- showed that training context matters at least as much as target-dataset identity

## What It Does Not Mean Yet

This does **not** mean the current broad labels are already biologically correct.

There are still signs that the marker system is too coarse:

- `reproductive_or_floral` appears in root datasets, which is unlikely to be literal
- `developmental_transition` remains underused
- several root identities are still being compressed into a few broad programs
- the current stress module likely mixes water transport / membrane-interface biology with genuine abiotic-stress response

## Practical Conclusion

The project has now passed an important checkpoint:

> the framework is sensitive to reference choice, so improving the reference can materially improve predictions

That is good news for the Wolffia direction, because it means we are not locked into the original stress-heavy outcome.

## Best Next Move

The next high-value step is to refine the marker panel and broad program ontology for root biology, especially:

- proliferative / meristematic
- vascular / transport
- epidermal / surface
- developmental transition
- stress response

The most specific next move is now:

1. split `aquatic_adaptation_or_stress` into a narrower abiotic-stress program and a separate transport / interface-oriented program
2. rerun the same root-derived reference tests
3. only then move on to Wolffia prediction transfer

## Stress-Module Split Rerun

We then split the old `aquatic_adaptation_or_stress` category into:

- `transport_interface_or_water_balance`
- `abiotic_stress_response`

This was meant to test whether the old stress-heavy behavior was partly caused by mixing membrane/interface biology with true stress-response biology.

### Split `WT -> SHR`

- `transport_interface_or_water_balance`: `46.22%`
- `abiotic_stress_response`: `43.86%`
- `proliferative_or_meristematic`: `9.92%`

### Split `WT -> GSE121619`

- `transport_interface_or_water_balance`: `48.05%`
- `abiotic_stress_response`: `34.50%`
- `proliferative_or_meristematic`: `17.45%`

### What improved

- the old stress-heavy bucket no longer behaves like a single undifferentiated sink
- the root-derived reference now separates one branch of interface/water-balance biology from one branch of broader abiotic-stress biology
- proliferative cells remain recoverable as a smaller but consistent population

### What this suggests

This is a more believable outcome than the previous monolithic stress mapping.

It suggests that at least part of what we first called "stress-like" was really capturing:

- water transport / membrane-interface programs
- osmotic or interface-associated physiology
- and only partly genuine stress-response modules

That is directly relevant to Wolffia, because an aquatic plant may also show strong interface- and water-balance-associated programs that should not automatically be interpreted as generic stress artifacts.

## Updated Best Next Move

Now the best next step is to:

1. review whether `transport_interface_or_water_balance` is still partly overlapping with vascular/transport markers
2. strengthen vascular and epidermal separation if needed
3. then move toward Wolffia transfer with this improved program set

## Vascular-Interface Boundary Check

We then tested whether strengthening vascular markers and narrowing the interface marker set would separate a clearer vascular-like program from the interface/water-balance program.

Changes made:

- added stronger vascular markers such as `ATHB8`, `PXY`, and `XCP1`
- removed more generic membrane/interface markers from `transport_interface_or_water_balance`
- kept aquaporin- and water-balance-oriented interface markers

### Updated `WT -> SHR`

- `abiotic_stress_response`: `53.23%`
- `transport_interface_or_water_balance`: `37.76%`
- `proliferative_or_meristematic`: `9.01%`

### Updated `WT -> GSE121619`

- `transport_interface_or_water_balance`: `45.35%`
- `abiotic_stress_response`: `33.90%`
- `proliferative_or_meristematic`: `20.75%`

### What changed

- the interface category became slightly less dominant in `WT -> SHR`
- proliferative signal increased slightly in `WT -> GSE121619`
- vascular markers contributed more as second-best signal in some clusters

### What did not change

- `vascular_like_or_transport` still did **not** emerge as a stable top-assigned broad program
- the root-derived training clusters are still mostly partitioning into:
  - `abiotic_stress_response`
  - `transport_interface_or_water_balance`
  - `proliferative_or_meristematic`

## Interpretation of This Check

This suggests that, in the current coarse ontology, vascular-associated biology is still not strong enough to stand on its own across these root reference transfers.

That does **not** necessarily mean vascular biology is absent. It more likely means one of these is true:

- vascular programs are genuinely weaker than the interface/stress axes in these particular references
- our broad vascular marker panel is still too small or too mixed
- vascular structure is being partially absorbed into interface/transport biology at this level of resolution

## Practical Next Move Now

At this point, we have probably reached diminishing returns from repeatedly tuning the same broad Arabidopsis marker table.

The best next step is now:

1. freeze this improved broad-program set as the current working reference
2. use it for first-pass Wolffia-oriented transfer and interpretation
3. treat vascular resolution as a secondary refinement question rather than blocking all forward progress
