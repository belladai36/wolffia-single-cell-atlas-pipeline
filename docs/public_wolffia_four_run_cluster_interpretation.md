# Public Wolffia Four-Run Cluster Interpretation

## Summary

The combined four-run Wolffia notebook adds the first native cell-level review of the public `PRJNA1124135` runs. The strongest current result is that the `photosynthetic_or_assimilation` transfer label is reproducible and partly supported by native Wolffia marker genes. The model remains intentionally conservative: every Leiden cluster is still majority `ambiguous`, and the accepted labels should be interpreted as broad program signals rather than final cell-type identities.

The marker review supports using the public Waus8730 dataset as a baseline for future Wolffia single-cell analyses, but it also shows that additional cluster-level annotation is needed before making stronger biological claims.

## Source Files

The cluster interpretation is based on outputs from:

- [Public Wolffia combined UMAP and marker review notebook](../notebooks/10_public_wolffia_combined_umap_marker_review.ipynb)
- `/Volumes/LaCie/wolffia_single_cell/results/combined_public_wolffia/four_run_cluster_label_composition.csv`
- `/Volumes/LaCie/wolffia_single_cell/results/combined_public_wolffia/four_run_leiden_marker_genes.csv`

The external CSV files are not committed because they are generated analysis outputs on the external data drive.

## Main Cluster-Level Pattern

The clusters with the highest `photosynthetic_or_assimilation` fractions are:

| Leiden cluster | Ambiguous fraction | Photosynthetic/assimilation fraction | Vascular/transport-like fraction | Interpretation |
|---:|---:|---:|---:|---|
| 1 | 73.8% | 23.7% | 2.3% | Strongest accepted photosynthetic-associated region |
| 8 | 77.8% | 20.8% | 1.4% | Photosynthetic/light-harvesting marker support |
| 0 | 85.4% | 13.9% | 0.6% | Photosystem/electron-transfer marker support |
| 14 | 86.7% | 13.3% | 0.0% | More stress/transport-like; needs review |
| 6 | 88.7% | 10.8% | 0.5% | Photosynthesis and carbon-fixation marker support |

No cluster is dominated by an accepted transfer label. This is expected under the conservative decision rule. The more important observation is that the accepted photosynthetic/assimilation-like cells are not random; they are enriched in a subset of native Wolffia clusters whose marker genes often support photosynthetic biology.

## Marker Evidence for the Photosynthetic/Assimilation Signal

Several clusters enriched for `photosynthetic_or_assimilation` have marker genes with clear chloroplast, photosystem, light-harvesting, carbon-fixation, or electron-transfer annotations.

Examples:

- Cluster 1 has chloroplast-associated markers including `atpB`, `psbE`, `ccsA`, `rpoA`, `rps3`, `rps8`, and `ycf1`.
- Cluster 8 has light-harvesting and carbon-assimilation markers, including light-harvesting complex genes, `RCA`, fructose-bisphosphate aldolase, and ferredoxin-related genes.
- Cluster 0 includes fructose-bisphosphate aldolase, `PETE`, `psaD`, ferredoxin-related markers, and a RuBisCO-related annotation.
- Cluster 6 includes `RCA`, light-harvesting complex markers, RuBisCO-related annotation, cytochrome b6-f complex annotation, chlorophyll A-B binding protein, and carbonic-anhydrase-related annotation.

This supports the current positive result: the leaf-primary transfer model is detecting a reproducible photosynthetic/assimilation-like broad program in public Wolffia data.

## Weak or Provisional Signals

The `vascular_like_or_transport` label appears in all four runs but remains weak at the cluster level. Its highest fraction is only about 2.3% in cluster 1, and the same clusters enriched for this label are also enriched for photosynthetic/assimilation-like labels. At this stage, the vascular/transport-like signal should remain provisional.

The `transport_interface_or_water_balance` label is extremely rare. It should not be interpreted as a stable cluster identity yet.

The `review_required` label is also rare and appears only as a small disagreement signal between model layers.

## Ambiguous Clusters Are Biologically Interesting

The ambiguous label should not be treated as failure. Some highly ambiguous clusters have informative marker patterns that may represent Wolffia-native programs not well captured by the current Arabidopsis-derived model.

Examples:

- Cluster 13 is almost entirely ambiguous and has markers related to lipid transfer, cadmium resistance, multidrug resistance, and DnaJ/chaperone biology.
- Cluster 7 is highly ambiguous and has nutrient-associated markers such as high-affinity nitrate transporters, inorganic phosphate transporter annotation, and glutamine synthetase.
- Cluster 9 is highly ambiguous and includes lipid-transfer, plasma membrane ATPase, sulfate transporter, and sterol-desaturase annotations.
- Cluster 14 has stress and ion-transport annotations, including universal stress protein, potassium transporter, and sodium/hydrogen exchanger family markers.

These ambiguous clusters may be especially useful for future Wolffia-specific annotation, because they may represent programs that are weakly represented in the current Arabidopsis reference labels.

## Current Interpretation

The combined public Wolffia analysis supports three conclusions:

1. **The photosynthetic/assimilation-like signal is the strongest current model-supported result.** It is reproducible across runs and has native marker support in several clusters.
2. **The model remains conservative in the intended way.** All clusters are majority ambiguous, which prevents overconfident transfer of Arabidopsis labels onto Wolffia cells.
3. **Ambiguous clusters should become a main annotation target.** Several ambiguous-enriched clusters have stress, nutrient-transport, lipid, ion-balance, or unknown-function marker patterns that may be biologically meaningful.

## Limitations

- The cluster-marker interpretation is based on computational marker enrichment and functional annotation text, not direct experimental validation.
- The exact library chemistry and barcode whitelist remain unconfirmed.
- The model labels are broad program labels, not final cell-type identities.
- The apparent dawn-versus-dusk pattern in model acceptance should remain tentative until batch, QC, and cluster composition are reviewed more deeply.
- Marker descriptions come from available Waus8730 functional annotation and may be incomplete or noisy.

## Recommended Next Steps

1. Manually review top marker genes for clusters 1, 8, 0, 6, 7, 9, 13, and 14.
2. Create a focused marker panel for photosynthesis, carbon fixation, nutrient transport, ion transport, stress response, lipid/surface biology, and unknown Wolffia-enriched programs.
3. Use the combined public dataset as the baseline for future Waus8730 salt-stress data.
4. Keep `photosynthetic_or_assimilation` as the strongest supported broad transfer label.
5. Keep `vascular_like_or_transport`, `transport_interface_or_water_balance`, and root-benchmark labels provisional until stronger marker and cluster-level evidence accumulates.

## Working Conclusion

The public Waus8730 analysis now has a coherent first biological signal: a conservative, reproducible photosynthetic/assimilation-like program supported by native Wolffia marker genes. The next modeling improvement should focus less on forcing labels onto ambiguous cells and more on using native cluster markers to define Wolffia-specific programs that the current Arabidopsis-derived model cannot yet name confidently.
