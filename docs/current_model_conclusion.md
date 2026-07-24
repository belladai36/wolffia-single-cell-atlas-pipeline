# Current Model Conclusion

## One-Sentence Conclusion

The project is now a leaf-prioritized, ortholog-aware Wolffia single-cell prediction framework: the
leaf model is the primary biological interpretation layer, the root model is a conservative
benchmark, and the ortholog map controls which Arabidopsis features can be transferred to Wolffia.

## What the Model Currently Does

The current workflow can:

1. map Arabidopsis genes to Wolffia orthologs
2. restrict model features to high- or medium-confidence Arabidopsis-to-Wolffia mappings
3. train and evaluate a root-derived benchmark model
4. train and evaluate a leaf-primary model using PSCB/Kim et al. Arabidopsis leaf cluster labels
5. apply both root and leaf models to a future Wolffia `.h5ad`
6. preserve `ambiguous` and `review_required` categories instead of forcing labels

## Why the Leaf Model Is Primary

`Wolffia australiana` is a reduced floating photosynthetic plant body, not a normal root system.
Therefore, Arabidopsis leaf/aerial reference data are more biologically relevant for Wolffia
interpretation than Arabidopsis root data.

The root model remains useful because root datasets are well annotated and provide a strong
benchmark for testing whether the pipeline behaves conservatively. But root-derived predictions
should not be treated as the final biological answer for Wolffia.

## What the Ortholog Layer Contributes

The model is trained in Arabidopsis, but future application is in Wolffia. Ortholog mapping is the
bridge between the two species.

Current ortholog result:

```text
2,000 Arabidopsis benchmark genes
↓
340 high- or medium-confidence Arabidopsis-to-Wolffia transfer genes
```

Only those 340 genes are used for strict cross-species model transfer.

## Current Benchmark Results

Root benchmark:

- reference: GSE123818 / GSE121619 Arabidopsis root
- role: conservative benchmark
- transfer features: 340
- consensus acceptance on target root cells: 26.5%
- selective benchmark recovery: about 95.3%

Leaf-primary model:

- reference: GSE161332 / PSCB Arabidopsis leaf atlas
- role: primary Wolffia-relevant model
- transfer features: 340
- labeled leaf cells after filtering: 4,587
- consensus acceptance on held-out leaf cells: 43.3%
- selective broad-label recovery: 93.6%

Combined application smoke test:

- synthetic Wolffia-like cells tested: 64
- feature coverage: 100%
- final label result: all ambiguous
- interpretation: good conservative behavior, because random fake data should not receive forced labels

## What We Can Claim Now

We can claim that:

- the repository has a reproducible Arabidopsis-to-Wolffia transfer framework
- the model is restricted to defensible ortholog features
- the root-derived model is a conservative benchmark
- the leaf-primary model is the better biological direction for Wolffia
- the combined application script is ready for a normalized Wolffia `.h5ad`

## What We Cannot Claim Yet

We cannot yet claim:

- true Wolffia cell-type accuracy
- validated Wolffia cell identities
- absence of specific Wolffia cell types
- final biological annotation of Wolffia clusters

Those claims require real Wolffia expression data plus marker, cluster, QC, and replicate support.

## Immediate Next Step

Now that external project storage is available, the next practical step is to move large public data and future
Wolffia downloads onto that external volume, then prepare a Wolffia `.h5ad` matrix for the combined application
script.

The current application command will be:

```bash
python scripts/36_apply_leaf_primary_and_root_benchmark.py \
  input_wolffia_normalized.h5ad \
  --gene-id-column wolffia_gene_id
```

## Bottom Line

The project is no longer waiting on design. The computational framework is ready. The next bottleneck
is real Wolffia data storage, download, conversion, and validation.
