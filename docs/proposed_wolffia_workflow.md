# Proposed Workflow: Wolffia Single-Cell Data Analysis Project

## Project Goal

Use single-cell RNA-seq data from *Wolffia australiana* to identify major cell populations, propose candidate cell identities, and explore developmental relationships between cell states.

## Core Biological Questions

1. How many transcriptionally distinct cell populations can be detected in Wolffia?
2. Does Wolffia show a reduced cellular landscape consistent with its simplified morphology?
3. Are there transitional or previously uncharacterized cell states involved in growth and development?

## Suggested Computational Workflow

1. **Raw data processing**
   - Start from a processed count matrix when available.
   - If the platform returns a processed cell-by-gene matrix, begin directly with matrix-level QC and Scanpy analysis.
   - If only raw reads are available, follow the appropriate preprocessing route to generate a gene-by-cell count matrix.
   - Record the exact preprocessing and filtering choices used by the platform.

2. **Cell-level quality control**
   - Evaluate reads per cell, detected genes, mapping rate, and organellar transcript fractions.
   - Flag low-quality cells and possible technical outliers.
   - Review potential batch or plate effects.

3. **Exploratory analysis**
   - Normalize expression values.
   - Identify highly variable genes.
   - Perform PCA and UMAP for visualization.

4. **Clustering and markers**
   - Cluster cells across a reasonable range of parameters.
   - Identify marker genes for each cluster.
   - Assess whether clusters are stable and biologically interpretable.

5. **Annotation**
   - Compare marker genes with known plant developmental markers and homologs.
   - Assign conservative candidate labels where possible.
   - Keep uncertain populations labeled as provisional or unknown.

6. **Trajectory analysis**
   - Use graph-based or pseudotime methods to examine developmental relationships.
   - Identify possible transition states or branch points.

7. **Project outputs**
   - Reproducible analysis pipeline.
   - QC summary and clustering figures.
   - Marker gene tables.
   - Preliminary cell atlas with candidate annotations.
   - Hypotheses for future biological validation.

## Feasibility Notes

- This project is strongest once new Wolffia single-cell expression data are available for analysis.
- If the experimental data are not available yet, public single-cell plant datasets could still be used to practice pipeline development and analysis methods.
- Annotation may be challenging if Wolffia reference annotations and marker knowledge are limited, so early conclusions should remain conservative.
