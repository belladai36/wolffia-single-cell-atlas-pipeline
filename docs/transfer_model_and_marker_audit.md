# Transfer-Ready Model Benchmark and Marker Audit

## Questions

1. How much predictive performance is lost when the 2,000-gene Arabidopsis model is restricted to 340 high- or medium-confidence Wolffia orthologs?
2. Which broad biological programs retain enough markers for cautious transfer, and which require marker development?

## Model Benchmark

The comparison uses the same cluster-held-out GSE123818 pseudo-label benchmark and the same conservative GSE121619 consensus rules for both feature sets. This controls the analysis so that the feature restriction is the main difference.

| Model | Feature set | Balanced accuracy | Macro F1 | GSE121619 acceptance |
|---|---|---:|---:|---:|
| Logistic regression | Full, 2,000 genes | 0.650 | 0.637 | 39.3% overall consensus |
| Logistic regression | Transfer-ready, 340 genes | 0.528 | 0.535 | 26.5% overall consensus |
| Random forest | Full, 2,000 genes | 0.588 | 0.586 | 39.3% overall consensus |
| Random forest | Transfer-ready, 340 genes | 0.474 | 0.463 | 26.5% overall consensus |

Restricting the feature space lowers balanced accuracy by 0.123 for logistic regression and 0.114 for random forest. Macro F1 falls by 0.103 and 0.123, respectively. Accepted GSE121619 cells decrease from 820 to 552, while ambiguous cells increase from 1,265 to 1,533.

The restricted model therefore preserves meaningful coarse signal, but it is less discriminative and rejects more cells. This is preferable to forcing unsupported cross-species labels.

![Full and transfer-ready benchmark](../figures/transfer_model_audit/full_vs_transfer_ready_benchmark.png)

## Program Marker Audit

Markers are divided into three evidence classes:

- **transfer-ready:** high- or medium-confidence reciprocal mappings; permitted in strict cross-species prediction
- **family-level candidate:** a strong directional match that is not one-to-one reciprocal; useful for manual family-aware review
- **unresolved:** no acceptable match or insufficient alignment coverage; excluded from prediction

![Program marker audit](../figures/transfer_model_audit/program_marker_transfer_audit.png)

The strongest strict coverage is reproductive/floral (100%), transport/interface/water balance (60%), and photosynthetic/assimilation (50%). Proliferative (40%) and developmental (33%) programs remain interpretable but incomplete. Epidermal (20%), stress (17%), and vascular (0%) programs require additional work.

The vascular result is especially instructive: six of nine markers have plausible family-level directional matches, including `SUC2`, `SWEET11`, `TMO5`, `CESA7`, `ATHB8`, and `XCP1`. Their failure to pass reciprocal-best-hit rules can reflect duplicated gene families, lineage-specific expansion, or a different best Arabidopsis paralog. They should be reviewed with gene trees or orthogroup methods before use, not promoted automatically.

For stress, `HSP101` is transfer-ready, `ZAT12` is a family-level candidate, and `RD29A`, `COR15A`, and `ERD10` are unresolved. A single strict marker is not enough for robust stress annotation. The next marker-development pass should prioritize conserved heat-shock proteins, ROS-response enzymes, ABA-response components, and dehydration-response families represented in the Wolffia annotation.

## Decision

- Keep the 2,000-gene model as the within-Arabidopsis performance reference.
- Use only the 340-gene model for strict Wolffia transfer.
- Preserve an explicit `ambiguous` output.
- Use low-confidence family matches only to design expanded marker panels and orthogroup analyses.
- Do not interpret missing reciprocal markers as proof that a biological program is absent from Wolffia.

## Reproduction

```bash
python scripts/30_transfer_model_benchmark_and_marker_audit.py
```

Outputs are written to `results/transfer_model_audit/` and `figures/transfer_model_audit/`.
