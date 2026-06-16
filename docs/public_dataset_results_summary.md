# Public Dataset Results Summary

## What was run

I reran the public plant reference workflow using:

- **Training dataset:** `GSE227564_callus`
- **Test dataset:** `GSE141730_root_phosphate`
- **Script:** [scripts/10_public_reference_statistical_prediction.py](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/scripts/10_public_reference_statistical_prediction.py)
- **Config:** [config/config.yaml](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/config/config.yaml)

The rerun finished successfully on **June 15, 2026** and refreshed the outputs in:

- [results/public_reference](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/results/public_reference)
- [figures/public_reference](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/figures/public_reference)

## Core numerical results

- classifier: `logistic_regression`
- train cells used: `1500`
- test cells predicted: `2000`
- shared selected genes: `2000`
- test set label mode: `unlabeled`

Predicted labels on the test dataset:

- label `5`: `475` cells
- label `3`: `438` cells
- label `12`: `416` cells
- label `0`: `163` cells
- label `6`: `155` cells
- label `1`: `123` cells
- label `2`: `63` cells
- all remaining labels: smaller groups

## Main conclusion

The workflow **works as a proof of concept**.

It successfully:

- loads two public plant single-cell datasets,
- normalizes and scores them,
- trains a classifier on one dataset,
- transfers predictions onto the second dataset,
- and produces structured outputs and visualization files.

The predictions are **not random**. They concentrate into a few dominant states instead of being
distributed evenly across all labels. That means the pipeline is detecting transferable
transcriptional structure across datasets.

At the same time, this is still a **method-validation result**, not a final biological discovery,
because the training labels are currently raw cluster IDs (`0`, `1`, `2`, etc.) rather than
carefully curated biological cell types.

## Biological interpretation

The current run suggests that:

1. the test dataset contains several recurring transcriptional states rather than one uniform cell population
2. only a subset of the train states dominate the test dataset
3. broad biological signal can be recovered across datasets
4. this pipeline is suitable for future transfer analysis into `Wolffia`, once we move from
   cluster-number labels to better biological reference labels

## Marker recovery results

### Training dataset

The training marker recovery table is all zero:

- aquatic/stress: `0/2`
- developmental transition: `0/3`
- epidermal/surface: `0/2`
- photosynthetic/assimilation: `0/4`
- proliferative/meristematic: `0/3`
- reproductive/floral: `0/2`
- vascular/transport: `0/3`

Interpretation:

- this does **not** mean the pipeline failed
- it means the current training setup uses **direct cluster labels**
- the cluster names are numeric, so the broad regex label rules were not used to define biological programs
- as a result, the program-score summary plots are flat and should be treated as a limitation of the
  current labeling scheme

### Test dataset

The test marker recovery is more informative:

- aquatic/stress: `1/2` (`ZAT12`)
- developmental transition: `3/3` (`PLT1, SCR, IAA19`)
- epidermal/surface: `2/2` (`ATML1, PDF1`)
- photosynthetic/assimilation: `2/4` (`LHCB1.1, LHCB2.1`)
- proliferative/meristematic: `0/3`
- reproductive/floral: `2/2` (`AP1, LFY`)
- vascular/transport: `3/3` (`SUC2, SWEET11, CESA7`)

Interpretation:

- the test dataset contains recognizable developmental, epidermal, transport, and stress-related
  signals
- some programs are easier to recover than others
- proliferative markers were not recovered in this run, which could reflect either biology or dataset context

## Figures and explanations

### 1. Training PCA

![Training PCA](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/figures/public_reference/train_broad_program_pca.png)

What this figure is:

- a PCA scatter plot of the **training dataset**
- each dot is one cell
- colors show the current assigned training labels

What it tells us:

- the training dataset has structure and subpopulations
- but the populations are only **partially separated**
- that is realistic for plant single-cell data, where many states are continuous or overlapping

Important limitation:

- because the current labels are cluster IDs instead of curated biology labels, this plot is best
  interpreted as **dataset structure**, not as final biological annotation

### 2. Training Heatmap

![Training Heatmap](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/figures/public_reference/train_program_score_heatmap.png)

What this figure is:

- a heatmap of **mean marker-program scores** across the training labels

What it currently shows:

- the heatmap is essentially flat

Why:

- the broad biological marker sets do not map cleanly onto the current numeric training labels
- this is a label-definition issue, not a crash or plotting error

Meaning:

- the next improvement should be to replace numeric train labels with broader biological categories

### 3. Training Boxplots

![Training Boxplots](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/figures/public_reference/train_program_score_boxplots.png)

What this figure is:

- a boxplot summary of program scores across the training labels

What it currently shows:

- values are essentially centered near zero for all groups

Interpretation:

- same issue as the heatmap
- the underlying scoring step ran, but the current train labeling scheme is not biologically aligned

### 4. Test PCA with predicted labels

![Predicted Test PCA](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/figures/public_reference/test_predicted_broad_program_pca.png)

What this figure is:

- a PCA plot of the **test dataset**
- colors show the **predicted labels transferred from the training dataset**

What it tells us:

- predictions are not scattered uniformly at random
- several regions of PCA space are enriched for a few dominant predicted labels
- this suggests the classifier is capturing reproducible transcriptomic structure

Why this figure matters most:

- this is the strongest visual evidence that the transfer workflow is functioning
- it shows that one dataset can be used to organize another dataset in a meaningful way

## Practical conclusion for the Wolffia project

This public-data run supports three important claims:

1. the computational pipeline is functional
2. cross-dataset transfer is feasible
3. the next meaningful improvement is biological relabeling of the training reference, followed by
   transfer into public `Wolffia` datasets

## Recommended next step

The best next move is:

- convert the training dataset from raw cluster IDs into broad biological program labels
- rerun the transfer workflow
- then apply the same logic to the public `Wolffia` scRNA-seq and snRNA-seq datasets

That will produce conclusions that are much more biologically interpretable for the real project question:

> does `Wolffia australiana` show preservation, reduction, or compression of canonical plant cell programs?
