# Config Guide

This folder contains the configuration files used by different workflows in the repository.

## Recommended Order

1. `config.yaml`
   - main project configuration
   - used for the legacy FASTQ-to-count-matrix scaffold
   - also contains the default public-reference settings

2. `public_reference_gse121619.yaml`
   - transfer validation using `GSE121619`

3. `public_reference_gse123818.yaml`
   - transfer validation using the broader `GSE123818` root atlas

4. `public_reference_gse123818_shr.yaml`
   - alternate `GSE123818` split for comparison

5. `public_reference_gse123818_wt_train_to_shr.yaml`
   - root-derived training reference transferred to the SHR subset

6. `public_reference_gse123818_wt_train_to_gse121619.yaml`
   - root-derived training reference transferred to `GSE121619`

## For Most Viewers

If you are only trying to understand the project, start with:

- `../README.md`
- `../docs/README.md`

If you are trying to run the public-reference prediction workflow, inspect:

- `config.yaml`
- one of the `public_reference_*.yaml` files that matches the comparison you want
