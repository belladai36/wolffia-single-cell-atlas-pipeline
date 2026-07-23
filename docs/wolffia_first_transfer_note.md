# Wolffia First Transfer Note

## Current Working Reference Set

For the first Wolffia-facing transfer pass, we should freeze the current broad program set as:

- `proliferative_or_meristematic`
- `photosynthetic_or_assimilation`
- `vascular_like_or_transport`
- `developmental_transition`
- `epidermal_or_surface_identity`
- `reproductive_or_floral`
- `transport_interface_or_water_balance`
- `abiotic_stress_response`

## Why This Is the Right Freeze Point

The Arabidopsis tuning phase already taught us four useful things:

1. callus-trained references over-collapsed root states into a stress-like sink
2. root-derived training references are much more informative as a benchmark
3. splitting interface/water-balance from abiotic-stress biology gives a more believable interpretation than one monolithic stress label
4. the root-derived model is not enough for leaf-like biology, so the leaf/aerial model should become the primary Wolffia-relevant reference layer

At the same time, the latest reruns suggest we are reaching diminishing returns from repeatedly retuning the same root-derived marker table.

That means this is a good point to stop treating the root model as the final biological frame and instead refine the project around a leaf-prioritized Wolffia transfer strategy.

## How to Interpret the First Wolffia Pass

For the first pass, treat these labels as **transferable biological programs**, not literal one-to-one organ identities.

The current frozen root-derived model should be interpreted as a conservative baseline. It can show whether the transfer machinery works and where the model refuses uncertain labels, but it should not receive the final biological vote when leaf/aerial evidence becomes available.

That matters especially for:

- `vascular_like_or_transport`
- `transport_interface_or_water_balance`
- `abiotic_stress_response`

If Wolffia cells score strongly for these programs, we should interpret them as evidence for:

- transport-associated function
- aquatic interface or water-balance regulation
- dynamic stress-response biology

and not over-claim that they correspond exactly to canonical Arabidopsis tissue classes.

## Primary Questions for the First Wolffia Transfer

1. do proliferative and photosynthetic programs remain easy to recover?
2. are transport-associated and interface-associated signals separated or merged?
3. do developmental signals appear as gradients rather than clean clusters?
4. are apparent stress-like states broad and diffuse, or confined to small subsets?
5. do any Wolffia cells remain weakly mapped or ambiguous under this improved reference?

## Practical Next Execution Step

Once the first public Wolffia dataset is locally available and converted:

1. cluster conservatively
2. apply the frozen root-derived model as a benchmark
3. apply or train the Arabidopsis leaf/aerial reference layer as the primary Wolffia-facing model
4. compute module scores using the frozen broad program set
5. inspect whether the dominant Wolffia signals are:
   - preserved
   - reduced
   - merged
   - compressed
   - ambiguous
6. only after that decide whether another round of marker refinement is actually necessary

## Bottom Line

The Arabidopsis phase is now strong enough to support a first Wolffia-facing interpretation pass, but the interpretation should be leaf-prioritized.

We should keep the root model as a conservative benchmark, build the leaf/aerial model as the primary biological layer, and let the Wolffia data tell us where the next refinement really belongs.
