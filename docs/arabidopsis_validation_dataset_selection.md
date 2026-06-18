# Arabidopsis Validation Dataset Selection

## Why we need one more Arabidopsis dataset

Our current transfer framework already works, but the present training and test pair still leaves one major limitation:

- we can recover broad programs
- but we have only one transfer target so far

That means we still do not know whether the current pattern is:

- robust across Arabidopsis datasets
- specific to the phosphate-root test dataset
- or biased by the current training reference

Before moving onto large public Wolffia files, the best next step is to add at least one more Arabidopsis validation dataset.

## Selection criteria

We want the next dataset to satisfy as many of these conditions as possible:

1. public GEO accession with processed files available
2. manageable size for local work
3. biologically interpretable context
4. enough metadata to support transfer validation
5. useful contrast with our current train and test pair

## Verified candidates

The candidate list is recorded in [data/metadata/arabidopsis_public_dataset_manifest.csv](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/data/metadata/arabidopsis_public_dataset_manifest.csv).

### 1. GSE121619

GEO record: [GSE121619](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121619)

Why it is useful:

- root single-cell dataset
- includes control and heat-shock conditions
- GEO lists processed supplementary files including `pData.tsv.gz`
- good for testing whether our broad programs are stable under a strong perturbation

Main caveat:

- the metadata file clearly contains cluster-level information such as `louvain_component`, but not obviously curated biological cell-type labels on first inspection

Best use in our project:

- near-term validation dataset for trajectory and stress-response transfer

### 2. GSE123818

GEO record: [GSE123818](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123818)

Why it is useful:

- classic Arabidopsis root atlas
- explicitly framed around developmental fate and time
- GEO provides processed wild-type and `shr` single-cell count matrices as compressed CSV files
- this is a strong dataset for asking whether broad developmental programs are preserved, weakly separable, or compressed

Main caveat:

- GEO confirms processed matrices, but cell-level biological labels may need to be reconstructed rather than read directly from a ready-made annotation file

Best use in our project:

- best broad atlas-style follow-up to the current Arabidopsis reference phase

### 3. GSE181999

GEO record: [GSE181999](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE181999)

Why it is useful:

- 10x scRNA-seq focused on phloem pole cell populations
- much more targeted than a whole-root atlas
- especially valuable for testing `vascular_like_or_transport` predictions

Main caveat:

- not a whole-plant or whole-root atlas
- less suitable as the only broad validation dataset

Best use in our project:

- targeted follow-up for transport-program validation after the broad program framework is stable

## Recommendation

The strongest order for our next Arabidopsis phase is:

1. `GSE121619` for immediate validation because the processed metadata are lightweight and already verified
2. `GSE123818` as the next broad atlas dataset for deeper developmental transfer analysis
3. `GSE181999` as a focused vascular validation dataset

## What this will let us test

Adding these datasets will sharpen the logic of our Wolffia predictions.

### If the same broad programs transfer repeatedly across Arabidopsis datasets

That supports the idea that these are real, reusable plant transcriptional programs.

### If some programs transfer only weakly or collapse across multiple Arabidopsis datasets

That suggests those programs are intrinsically hard to separate, which is important because we should not over-interpret compressed states in Wolffia as necessarily novel.

### If vascular-like signatures become strong only in the phloem-focused dataset

That would support a more nuanced prediction:

- transport programs may be real
- but they may require enriched or targeted sampling to appear as distinct states

This is directly relevant to Wolffia, where reduced morphology may make vascular-like states even harder to isolate.

## Practical next move

The best immediate computational move is:

1. intake `GSE121619`
2. inspect whether its metadata can be translated into broad biological programs
3. rerun the transfer workflow with `GSE227564` training versus `GSE121619` validation
4. compare its prediction distribution against the current `GSE141730` result

If the patterns agree, we can say with more confidence that our Arabidopsis-trained framework is stable enough to generate first-pass Wolffia predictions.
