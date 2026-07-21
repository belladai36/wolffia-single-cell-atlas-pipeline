# Wolffia Public Reference Training Plan

## Goal

Extend the existing Arabidopsis transfer workflow so that public `Wolffia australiana` datasets can
be used as a **Wolffia-native reference layer**.

## Recommended role of each public Wolffia dataset

### Primary training candidate

- `PRJNA1124135`
- whole-plant `Wolffia australiana` scRNA-seq
- best first choice for training or fine-tuning because it is:
  - single-cell rather than single-nucleus
  - Wolffia-native
  - already described as resolving a few major tissue compartments

### Preferred validation candidate

- `PRJNA809022`
- `Wolffia australiana` single-nucleus RNA-seq
- best used for:
  - reproducing broad programs
  - checking whether putative Wolffia states are robust across assay type
  - validation after the first Wolffia reference is built

## Training strategy

Do **not** jump straight to fully supervised training unless clean labels exist.

Instead use a staged approach:

1. preprocess the public Wolffia dataset
2. cluster it conservatively
3. assign broad pseudo-labels or manual labels
4. train a Wolffia-native classifier on those broad labels
5. validate on the second Wolffia dataset
6. later project future Wolffia single-cell data into the Wolffia-trained reference

## Why this is better than Arabidopsis-only training

Arabidopsis is still useful as a biological scaffold, but Wolffia training is better for:

- species-specific transcript structure
- aquatic-state interpretation
- reduced-body-plan biology
- identifying compression or hybrid states that Arabidopsis labels may miss

## New repo pieces added for this

- manifest: [data/metadata/wolffia_public_dataset_manifest.csv](../data/metadata/wolffia_public_dataset_manifest.csv)
- broad-label template: [data/metadata/wolffia_public_label_template.csv](../data/metadata/wolffia_public_label_template.csv)
- preparation script: [scripts/12_prepare_wolffia_public_references.py](../scripts/12_prepare_wolffia_public_references.py)

## What this script does

The preparation script is intentionally generic.

Once local public Wolffia files are available, it can convert:

- `h5ad`
- `10x_h5`
- `10x_mtx_dir`

into standardized `.h5ad` reference files under `data/public_references/processed/`.

## Important limitation

The current manifest keeps `input_format=unknown` because we have **not yet downloaded and inspected
the public Wolffia files locally**.
This has now been refined one step further:

- both public Wolffia projects are currently represented as `raw_fastq_dir`
- that reflects the fact that the archive exposes them as run-level sequencing data rather than
  ready-made matrices

See:

- [data/metadata/wolffia_public_run_accessions.csv](../data/metadata/wolffia_public_run_accessions.csv)

## Next execution step

1. download the selected Wolffia public runs under `data/public_references/raw/`
2. generate a count matrix or processed single-cell matrix
3. update the manifest from `raw_fastq_dir` to one of:
   - `h5ad`
   - `10x_h5`
   - `10x_mtx_dir`
4. run:

```bash
/opt/anaconda3/envs/py311/bin/python scripts/12_prepare_wolffia_public_references.py
```

5. inspect the resulting `.h5ad` files
6. add clustering and annotation logic for first-pass Wolffia pseudo-labels

## Practical target

The immediate computational target is:

> build a first Wolffia-native reference from `PRJNA1124135`, then test whether its broad states
> replicate in `PRJNA809022`.

## Current Interpretation Guardrail

Before that Wolffia-native reference is built, the current Arabidopsis-derived transfer layer should be treated as a **program-level scaffold** rather than a literal tissue-label system.

See:

- [Wolffia first transfer note](wolffia_first_transfer_note.md)
- [Root-derived reference update](root_derived_reference_update.md)

In particular, the first Wolffia-facing pass should preserve the distinction between:

- `transport_interface_or_water_balance`
- `abiotic_stress_response`

because the latest Arabidopsis reruns suggest that those two signals are biologically more interpretable when they are not collapsed into one generic stress category.
