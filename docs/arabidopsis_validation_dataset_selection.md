# Arabidopsis Validation Dataset Selection

## Why we need one more Arabidopsis dataset

Our current transfer framework already works, but the present training and test pair still leaves two major limitations:

- we can recover broad programs
- but the strongest current reference is root-derived
- and root cells are not the best biological match for a reduced photosynthetic Wolffia body

That means we still do not know whether the current pattern is:

- robust across Arabidopsis datasets
- specific to the phosphate-root test dataset
- or biased by the current training reference

Before moving onto large public Wolffia files, the best next step is to add at least one more Arabidopsis validation dataset.

The most important new reference type is an Arabidopsis leaf or aerial-tissue expression matrix. The root atlas remains valuable because the markers are well established, but the leaf/aerial layer should test whether photosynthetic and surface-associated programs transfer more naturally. We selected `GSE161332` as the first leaf reference because it has processed 10x-style matrix files and captures leaf-relevant populations.

## Selection criteria

We want the next dataset to satisfy as many of these conditions as possible:

1. public GEO accession with processed files available
2. manageable size for local work
3. biologically interpretable context
4. enough metadata to support transfer validation
5. useful contrast with our current train and test pair

For the leaf extension, also prioritize:

6. photosynthetic or aerial-tissue context
7. labels that can distinguish mesophyll-like, epidermal/surface, vascular/transport, and stress/interface programs
8. a processed matrix that can be converted into `.h5ad`

## Verified candidates

The candidate list is recorded in [data/metadata/arabidopsis_public_dataset_manifest.csv](../data/metadata/arabidopsis_public_dataset_manifest.csv).

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

### 4. GSE161332

GEO record: [GSE161332](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE161332)

Why it is useful:

- Arabidopsis leaf single-cell dataset
- processed 10x-style matrix files are available from GEO
- includes leaf-relevant populations such as epidermis, guard cells, hydathodes, mesophyll, and vascular cell types
- directly supports the root-versus-leaf comparison needed for the refined reference strategy

Main caveat:

- detailed cell-type annotation may need to be reconstructed from publication/browser labels or cluster-level marker scoring

Best use in our project:

- first leaf reference extension for photosynthetic, surface, mesophyll-like, and vascular/transport program comparison

## Recommendation

The refined order for our next Arabidopsis phase is:

1. keep `GSE123818` as the root-derived benchmark because it is already converted and supports the frozen transfer model
2. add `GSE161332` as the first Arabidopsis leaf matrix for the next root-versus-leaf comparison
3. use `GSE181999` as a focused vascular validation dataset if transport programs remain weak or merged
4. use `GSE121619` and `GSE308672` as stress and perturbation checks when needed

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

1. download the processed `GSE161332` matrix, features, and barcode files
2. convert `GSE161332` into `.h5ad`
3. map or infer its labels into the eight broad programs where possible
4. compare root-derived and leaf-derived predictions before applying both views to Wolffia

If the root and leaf patterns agree, we can say with more confidence that our Arabidopsis-trained framework is stable enough to generate first-pass Wolffia predictions. If they disagree, that disagreement becomes biologically informative because it shows which Wolffia programs are most sensitive to reference choice.
