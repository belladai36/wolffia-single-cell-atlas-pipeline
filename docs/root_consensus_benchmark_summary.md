# Root Reference Consensus Benchmark

## Purpose

This benchmark tests whether broad Arabidopsis root expression programs are stable enough to support later hypothesis generation in *Wolffia australiana*. It compares logistic regression with random forest, evaluates both models on held-out GSE123818 clusters, and builds a conservative GSE121619 consensus set.

## Data

- GSE123818 wild-type root: 4,727 cells used as the seed reference
- GSE121619 control and heat-shock root: 2,085 cells used as the second root dataset
- Shared feature set: 2,000 highly variable genes selected from the GSE123818 reference and present in both datasets
- Seed labels: three broad programs inferred previously from GSE123818 cluster-average marker-module scores

The seed labels are marker-derived pseudo-labels, not expert-curated cell-type truth.

## Validation Design

Random cell-level splitting would allow highly similar cells from the same Leiden cluster to appear in both training and testing. To reduce that leakage, the benchmark uses two-fold stratified group cross-validation with Leiden cluster as the held-out group. Entire clusters are excluded from model training and then predicted.

Two folds are used because the proliferative/meristematic seed program contains only two independent Leiden clusters. More folds would not preserve that program in every training and test partition.

The two evaluated classifiers are:

1. class-balanced logistic regression after scaling and PCA
2. class-balanced random forest after scaling and PCA

## Cluster-Held-Out Results

| Model | Accuracy | Balanced accuracy | Macro F1 | Log loss | Mean confidence | Calibration error |
|---|---:|---:|---:|---:|---:|---:|
| Logistic regression | 0.720 | 0.650 | 0.637 | 2.061 | 0.955 | 0.233 |
| Random forest | 0.698 | 0.588 | 0.586 | 0.781 | 0.752 | 0.062 |

Logistic regression has better pseudo-label recovery, but it is substantially overconfident. Random forest has somewhat weaker discrimination but much better calibrated confidence. Temperature parameters were learned from cluster-held-out predictions and then applied to final-model probabilities. Logistic calibration error fell from 0.233 to 0.055, while random-forest calibration error fell from 0.062 to 0.028. For this reason, neither model is used alone to admit GSE121619 cells into the consensus set.

Class-level recall from the normalized confusion matrices shows:

- stress: 0.88 logistic regression and 0.89 random forest
- proliferative/meristematic: 0.51 logistic regression and 0.31 random forest
- transport/water balance: 0.53 logistic regression and 0.52 random forest

The models recover the stress pseudo-label most reliably. The other two programs remain only moderately separable and frequently collapse toward stress.

## Conservative GSE121619 Consensus

A GSE121619 cell is accepted only when:

1. logistic regression and random forest predict the same program
2. both model confidences are at least 0.60
3. the model consensus agrees with the highest marker-module score
4. the top marker score exceeds the second score by at least 0.05

After temperature calibration, this retained 820 of 2,085 cells, or 39.3%:

- transport/interface or water balance: 705 cells
- abiotic stress response: 55 cells
- proliferative or meristematic: 60 cells
- ambiguous or rejected: 1,265 cells

The accepted GSE121619 cells are down-weighted to 0.5 relative to GSE123818 seed cells when fitting the final root consensus models.

## Ortholog-Restricted Sensitivity Test

The reciprocal Arabidopsis-to-Wolffia protein analysis retained 340 high- or medium-confidence model features. Retraining on only those cross-species-compatible genes reduced performance:

| Model | Balanced accuracy | Macro F1 | Calibrated confidence error |
|---|---:|---:|---:|
| Logistic regression | 0.528 | 0.535 | 0.078 |
| Random forest | 0.474 | 0.463 | 0.099 |

The ortholog-restricted consensus retained 552 of 2,085 GSE121619 cells, or 26.5%. This loss of performance means that the unrestricted 2,000-gene model should remain an Arabidopsis benchmark. Only the ortholog-restricted model is technically transferable to Wolffia, and its predictions must be treated as coarse hypotheses with a large ambiguous category.

## Interpretation

The root-based approach is more balanced than the earlier callus-to-root transfers, but the benchmark is not an independent cell-type accuracy test. Its targets were inferred from marker scores at the cluster level, and the marker agreement filter uses related biological information. The results support a provisional coarse-program model, not definitive annotations.

The final logistic-regression and random-forest artifacts should therefore be used together. A future Wolffia cell should be considered confidently mapped only when both models agree, confidence and marker evidence pass explicit thresholds, ortholog coverage is adequate, and the mapping is stable across reference choices.

## Reproduction

Run:

```bash
python scripts/27_root_reference_consensus.py
```

Review:

```text
notebooks/02_root_consensus_benchmark.ipynb
results/root_reference_consensus/
figures/root_reference_consensus/
```
