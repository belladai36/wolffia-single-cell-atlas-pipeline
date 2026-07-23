# Ortholog-Aware Root and Leaf Model Comparison

## Purpose

This document defines the current model hierarchy for Wolffia-facing prediction.

The project now uses three linked layers:

1. Arabidopsis-to-Wolffia ortholog mapping
2. root-derived benchmark model
3. leaf-primary biological model

The key refinement is that the leaf/aerial model should carry the main biological interpretation for
`Wolffia australiana`, while the root model remains useful as a conservative benchmark.

## Why Ortholog Mapping Comes First

The models are trained in Arabidopsis, but future application will be in Wolffia. Therefore, every
model feature used for Wolffia transfer must have a defensible Arabidopsis-to-Wolffia gene mapping.

Orthology is species-level, not tissue-level:

- a gene's Arabidopsis-to-Wolffia ortholog relationship is the same whether that gene is used in a root model or a leaf model
- root and leaf models can still differ because different genes and programs are informative in different tissues

The current transfer feature set comes from reciprocal DIAMOND protein mapping:

| Mapping class | Genes |
|---|---:|
| High confidence | 217 |
| Medium confidence | 123 |
| Low confidence | 874 |
| Unmapped or below threshold | 786 |

Only high- and medium-confidence mappings are used as strict model-transfer features:

```text
217 high + 123 medium = 340 transfer-ready genes
```

## Current Model Roles

| Model layer | Role | Dataset | Label source | Transfer features | Main use |
|---|---|---|---|---:|---|
| `v1_root_benchmark` | secondary benchmark | GSE123818 / GSE121619 root references | marker-derived Arabidopsis root broad-program pseudo-labels | 340 | test conservative transfer mechanics |
| `v2_leaf_primary` | primary biological layer | GSE161332 / PSCB leaf atlas | PSCB/Kim et al. published clusters collapsed to broad programs | 340 | Wolffia-relevant photosynthetic/aerial interpretation |

## Current Benchmark Results

| Metric | Root benchmark | Leaf-primary model |
|---|---:|---:|
| Training/reference cells | 4,727 root cells | 4,587 labeled leaf cells after filtering |
| Transfer features present | 340 | 340 |
| Feature coverage | 100.0% | 100.0% |
| Consensus acceptance rate | 26.5% on GSE121619 target cells | 43.3% on held-out leaf cells |
| Selective recovery/accuracy | 95.3% in held-out root pseudo-label benchmark | 93.6% held-out broad-label recovery |
| Main accepted programs | transport/interface, proliferative, stress | photosynthetic, vascular/transport, epidermal/surface, interface/water |

The exact benchmark contexts differ, so these numbers should not be interpreted as a direct
head-to-head accuracy contest. The important conclusion is qualitative:

- the root model is highly conservative and useful for stress-testing rejection behavior
- the leaf model captures photosynthetic and surface/leaf-associated programs that the root model cannot represent
- both models are restricted to the same 340 cross-species-compatible genes

## Final Interpretation Rule for Future Wolffia Data

When Wolffia expression matrices become available, predictions should be interpreted in this order:

1. Apply the leaf-primary model first.
2. Apply the root benchmark model as secondary evidence.
3. Check global feature coverage against the 340 transfer genes.
4. Preserve `ambiguous` when model agreement, confidence, or marker evidence is weak.
5. Require marker-module and cluster-level support before naming biological states.

Recommended decision rule:

| Leaf-primary result | Root-benchmark result | Interpretation |
|---|---|---|
| confident | agrees | strongest transferable support |
| confident | ambiguous | use leaf result as primary, root gives no contradiction |
| confident | disagrees | keep as review-required; inspect markers and clusters |
| ambiguous | confident | secondary/root-like signal only, not final label |
| ambiguous | ambiguous | leave ambiguous |

## What This Means for Wolffia

Because Wolffia is a reduced floating photosynthetic plant body, the leaf/aerial model is more
biologically relevant than the root model. However, Wolffia may still reorganize, merge, or compress
canonical Arabidopsis programs. The correct output should therefore be:

- a primary leaf-derived prediction when evidence is strong
- a root-derived comparison signal when useful
- confidence scores
- ambiguity status
- marker-module support
- cluster-level support

## Next Coding Step

The combined Wolffia application script is:

```text
scripts/36_apply_leaf_primary_and_root_benchmark.py
```

Expected input:

- normalized, log1p-transformed Wolffia `.h5ad`
- raw counts preserved separately
- Wolffia gene IDs compatible with the ortholog table

Expected output:

- leaf-primary prediction and confidence
- root-benchmark prediction and confidence
- agreement/disagreement flags
- final interpretation label
- ambiguous/review-required calls
- summary tables and figures

Smoke-test command:

```bash
python scripts/36_apply_leaf_primary_and_root_benchmark.py --smoke-test
```

Future real-data command:

```bash
python scripts/36_apply_leaf_primary_and_root_benchmark.py \
  input_wolffia_normalized.h5ad \
  --gene-id-column wolffia_gene_id
```

## Bottom Line

The refined project is now:

> A leaf-prioritized, ortholog-aware framework for transferring Arabidopsis reference information to
> Wolffia single-cell data, with a root-derived benchmark retained as conservative secondary evidence.
