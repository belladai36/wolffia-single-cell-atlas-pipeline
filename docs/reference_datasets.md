# Reference Datasets and Resource Plan

## Goal

This document locks the first-pass public reference set for a prediction-first `Wolffia australiana` cell atlas project.

The emphasis is not on collecting every possible dataset. It is on choosing a compact, defensible reference panel that is good enough to support marker transfer, trajectory thinking, and early biological predictions.

## Locked Phase 1 Reference Panel

### Primary Reference 1

`Arabidopsis thaliana` root single-cell atlas from Jean-Baptiste et al.

Why we are using it:

- one of the foundational early plant single-cell references
- useful for canonical root and developmental marker genes
- good starting point for conservative cell-program definitions

Best use in this project:

- broad marker collection
- initial cell-program naming
- comparison against other Arabidopsis references

Priority:

- high

### Primary Reference 2

`Arabidopsis thaliana` root single-cell atlas from Shulse et al.

Why we are using it:

- independent Arabidopsis root reference for cross-checking marker stability
- helpful for avoiding dependence on a single publication's annotation scheme
- strengthens confidence in conserved root-associated programs

Best use in this project:

- confirm marker consistency across references
- compare cluster definitions
- identify robust versus publication-specific markers

Priority:

- high

### Primary Reference 3

`Arabidopsis thaliana` developmental root trajectory reference from Denyer et al.

Why we are using it:

- especially useful for developmental gradients rather than only discrete cell labels
- aligns well with our interest in whether Wolffia has compressed or continuous cell states
- provides a conceptual anchor for pseudotime and trajectory analysis later

Best use in this project:

- developmental transition markers
- trajectory expectations
- hypotheses about merged or compressed states in Wolffia

Priority:

- high

## Secondary Reference Layer

These are not required to finish Phase 1, but they are useful once the core marker framework is stable.

### Primary Reference 4

`Arabidopsis thaliana` leaf or aerial-tissue single-cell references

Why they matter:

- respond directly to the concern that root cells differ from leaf-like or frond-like cells
- improve coverage of photosynthetic programs
- help distinguish surface, mesophyll-like, guard-cell-like, and stress-responsive states
- provide a more biologically relevant comparison for the reduced photosynthetic body of Wolffia

Priority:

- high for the next analysis phase

Current status:

- first selected dataset: `GSE161332`
- processed matrix files are available from GEO
- additional published matrices can still be added later as a second leaf/aerial validation layer

### Secondary Reference A

Duckweed or other Lemnaceae transcriptomic resources

Why they matter:

- provide evolutionary context closer to Wolffia than Arabidopsis alone
- help identify aquatic-adaptation signatures
- reduce the risk of over-transferring terrestrial plant labels

Priority:

- medium

## Wolffia-Specific Resource Set

These are locked as the Wolffia background layer for Phase 1.

### Resource 1

`Genome of the world's smallest flowering plant, Wolffia australiana, helps explain its specialized physiology and unique morphology`

Use:

- morphology background
- genome context
- project framing

### Resource 2

`The genome of Wolffia australiana facilitates discovery of genetic basis for aquatic adaptation in duckweeds`

Use:

- genome and annotation context
- ortholog reasoning
- aquatic adaptation interpretation

### Resource 3

Available public Wolffia or duckweed transcriptome resources, if they can be tied to a clear accession or supplement

Use:

- expression plausibility checks
- support for predicted program presence
- priority genes for later validation

## Why This Reference Set Is Enough for Phase 1

This panel is intentionally small, but it covers the main needs of the project:

- canonical plant marker programs
- developmental trajectories
- photosynthetic and surface-state follow-up
- Wolffia-specific evolutionary context

That is enough to complete the first serious round of:

- marker collection
- Wolffia mapping notes
- hypothesis generation

## Reference Strategy Rules

To keep the project biologically careful, we will follow these rules:

1. use broad cell programs before fine-grained labels
2. prefer markers supported by more than one Arabidopsis reference when possible
3. treat root-derived labels as transferable programs, not literal Wolffia organs
4. mark Wolffia mappings as `high`, `medium`, or `low` confidence rather than pretending orthology is fully resolved
5. compare root-derived and leaf-derived reference behavior before deciding whether Wolffia ambiguity reflects true biological compression
6. leave room for Wolffia-specific or aquatic-specific states that do not map neatly to Arabidopsis

## Phase 1 Output Expected from This Reference Set

Using this locked panel, we should now be able to produce:

- a populated marker template
- first-pass Wolffia mapping notes
- ranked predictions for preserved, merged, reduced, or novel programs
- root-versus-leaf reference comparison
