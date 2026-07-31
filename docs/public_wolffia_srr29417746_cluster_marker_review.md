# Public Wolffia SRR29417746 Cluster Marker Review

## Technical Summary

The first public Wolffia run processed through the project workflow shows biologically interpretable structure. After STARsolo counting, normalization, Waus8730-to-Arabidopsis feature bridging, and leaf-primary/root-benchmark transfer prediction, the native Waus8730 UMAP produced 9 Leiden clusters from 2,718 filtered cells.

The current transfer model remained conservative: 2,350 cells were ambiguous, while 347 cells were provisionally labeled `photosynthetic_or_assimilation` and 21 cells were provisionally labeled `vascular_like_or_transport`. The marker review supports the main direction of the model: several native clusters with higher photosynthetic/assimilation label fractions also have photosystem, RuBisCO, light-harvesting complex, chloroplast, or carbon-assimilation marker annotations.

This does not establish final Wolffia cell types. It does show that the model's accepted photosynthetic/assimilation-like predictions are not random; they align with interpretable native Wolffia marker structure in this first public run.

## Source and Scope

Primary evidence comes from the executed notebook:

- [Public Wolffia SRR29417746 QC, UMAP, and transfer-label review](../notebooks/08_public_wolffia_srr29417746_qc_umap.ipynb)

Input data and model outputs used by the notebook:

- public run: `SRR29417746`
- public project: `PRJNA1124135`
- genome/reference: `Waus8730.v1`
- counting method: STARsolo
- filtered matrix: 2,718 cells by 15,080 Waus8730 genes
- Waus8730-to-Arabidopsis model feature coverage: 309 of 340 features, or 90.9%
- UMAP feature set: 2,000 highly variable Waus8730 genes
- Leiden clustering resolution: 0.6

## Transfer Labels Align With a Subset of Native Wolffia Clusters

The model did not label most cells, which is expected for a conservative cross-species transfer model. The accepted labels were concentrated unevenly across native Waus8730 clusters rather than distributed uniformly.

| Leiden cluster | Ambiguous cells | Photosynthetic/assimilation cells | Vascular/transport-like cells | Photosynthetic/assimilation fraction |
|---:|---:|---:|---:|---:|
| 0 | 450 | 47 | 0 | 9.5% |
| 1 | 369 | 91 | 10 | 19.4% |
| 2 | 397 | 12 | 0 | 2.9% |
| 3 | 250 | 93 | 10 | 26.3% |
| 4 | 307 | 22 | 0 | 6.7% |
| 5 | 304 | 20 | 0 | 6.2% |
| 6 | 165 | 28 | 0 | 14.5% |
| 7 | 53 | 20 | 1 | 27.0% |
| 8 | 55 | 14 | 0 | 20.3% |

Clusters 1, 3, 7, and 8 had the largest photosynthetic/assimilation fractions. Clusters 1 and 3 also contained the largest numbers of photosynthetic/assimilation-labeled cells.

The vascular/transport-like signal remains small in this run. Only 21 cells received that final label, mostly in clusters 1 and 3, so it should be treated as a weak provisional signal until replicated in additional runs or supported by marker analysis.

## Marker Annotations Support Photosynthetic and Chloroplast Programs

The annotated marker review gives biological support for the photosynthetic/assimilation direction.

Cluster 1 had marker annotations including:

- Photosystem II 10 kDa polypeptide
- RuBisCO-related gene
- light-harvesting complex gene
- peroxisomal hydroxy-acid oxidase

Cluster 3 had chloroplast/plastid-associated markers including:

- `rpoA`
- `rps8`
- `atpB`
- `ccsA`
- `ycf1`

Cluster 4 also had photosynthesis and carbon-assimilation-related annotations including:

- RuBisCO-related genes
- glyceraldehyde-3-phosphate dehydrogenase-related gene
- Photosystem I reaction center subunit XI

Cluster 6 had annotations that may relate to transport, water balance, or structural programs, including:

- MIP aquaporin family genes
- proline-rich gene
- actin-family gene
- thiamine biosynthesis gene

These annotations support the decision to give more biological weight to the leaf-primary model layer than the older root-benchmark layer for Wolffia interpretation.

## Ambiguous Clusters Remain Biologically Important

Ambiguous cells are not simply failures. Many ambiguous cells fall into native Wolffia clusters with marker genes that may represent real Wolffia-specific or poorly annotated states.

Examples:

- Cluster 0 includes unknown-function, 3-ketoacyl-CoA synthase, and late embryogenesis abundant protein markers.
- Cluster 2 includes lipid-transfer protein, sterol desaturase, and chitinase-related markers.
- Cluster 5 includes tetraspanin, ethylene-responsive transcription factor, heavy-metal-associated, EXORDIUM-like, and protein phosphatase markers.
- Cluster 8 includes germin-like and flowering-time-related annotations.

These clusters should remain conservative in the current model output. They may become useful Wolffia-native programs after deeper marker review, functional annotation, and comparison across additional public runs.

## Methodological Notes

The marker review used native Waus8730 expression structure, not only the 340-feature model input. The workflow was:

1. load the normalized Waus8730 AnnData object,
2. attach transfer predictions from the combined leaf-primary/root-benchmark model,
3. select 2,000 highly variable Waus8730 genes,
4. run PCA, neighbor graph construction, UMAP, and Leiden clustering,
5. rank marker genes for each Leiden cluster,
6. annotate top Waus8730 marker genes using the Waus8730 functional annotation table derived from eggNOG-mapper output.

This is important because it checks whether the model labels make sense in the native Wolffia expression space rather than only in the projected Arabidopsis model-feature space.

## Limitations

- This review is based on one public run only.
- The transfer labels are provisional broad-program labels, not final cell-type annotations.
- Several Waus8730 marker genes have unknown or missing functional descriptions.
- Waus8730-to-Arabidopsis feature bridging uses orthogroups, so one-to-many and many-to-many mappings remain biologically imperfect.
- The model was run without a confirmed barcode whitelist for this first public-data test.
- The current analysis does not yet compare biological replicates, treatment groups, or additional public Wolffia runs.

## Recommended Next Steps

1. Process the remaining public runs from `PRJNA1124135` using the same STARsolo-to-model workflow.
2. Build a combined public-Wolffia summary notebook comparing all processed runs.
3. Test whether the photosynthetic/assimilation-like clusters and marker annotations reproduce across runs.
4. Review the ambiguous clusters as possible Wolffia-native states rather than discarding them.
5. Use the Waus8730 marker review to prepare for future Waus8730 salt-stress data, where sample metadata will allow treatment-aware comparisons.

## Current Conclusion

The first public Wolffia run supports the project direction. The accepted transfer labels are conservative, but the strongest accepted signal is biologically plausible: photosynthetic/assimilation-like predictions align with native clusters enriched for photosystem, RuBisCO, light-harvesting, and chloroplast-associated marker annotations. The next critical test is reproducibility across the remaining public Wolffia runs.
