# P0 D2 RNA DISCOVERY target audit

Status: CLOSED PASS

## Returned artifact integrity

All four D2 result tables match the returned SHA-256 manifest exactly:

- `Common_Hallmarks.csv`: `c7c4ee59447dd1b29c6ccf329560abfbf61b9285978ca98cea73c625c2474a64`
- `RNA_Discovery_Scores.csv.gz`: `b37a6b14fb588185496d7d7ca205b782eb22378c0dc77f577e78e711fe39888a`
- `RNA_Target_Eligibility.csv`: `95cdb15cfe9a212ef265184fffd32cca3933ee90503d561a949e1ea9eded96a4`
- `RNA_Target_Transforms.csv.gz`: `f06ad6b9a10b5cb19c1eaf6a4ae411aa38f869e9e08d033e9b063c1f32e78a5d`

Returned `RUN_SUMMARY.json` SHA-256: `306619c74e06c30b8bc0c9374a6234ccdb9e32744283dfda503a53ca9aa59a66`.

## Independent reconstruction

The audit independently reconstructed the following from the returned tables:

- exact DISCOVERY participant identity set equals the audited D1 DISCOVERY identity set: 4,863 unique cancer/participant pairs;
- exact cancer set is the frozen 19-cancer P0 evaluable set;
- `RNA_Discovery_Scores.csv.gz` contains 243,150 rows = 4,863 participants x 50 RNA Hallmarks, with zero duplicate cancer/participant/Hallmark keys;
- every cancer contains exactly 50 RNA Hallmarks;
- all RNA PC1 scores are finite;
- maximum absolute within-cancer/Hallmark DISCOVERY score mean is approximately `1.38e-15`, consistent with discovery-centered PC1 construction;
- minimum within-group PC1 variance is positive (`~3.286`), so no returned target score group is degenerate;
- `RNA_Target_Eligibility.csv` contains 950 rows = 19 cancers x 50 Hallmarks, with zero duplicate cancer/Hallmark keys;
- all 950 RNA Hallmarks pass the frozen target mapping rule and all 950 have `PC1_EVALUABLE` status;
- minimum retained discovery gene count is 18, above the frozen >=10 Hallmark target mapping floor;
- `RNA_Target_Transforms.csv.gz` contains 132,966 unique cancer/Hallmark/gene transform rows;
- every evaluable cancer/Hallmark transform row count exactly equals the eligibility table's retained discovery gene count;
- all transform means, loadings, and explained-variance fractions are finite;
- explained-variance fractions lie in `[0.0937863, 0.745547]`;
- every cancer/Hallmark loading vector has Euclidean norm 1 to floating-point precision; maximum absolute norm deviation from 1 is approximately `1.89e-15`;
- orientation method is internally constant within every cancer/Hallmark and all returned groups use `NONNEGATIVE_CORRELATION_WITH_DISCOVERY_MODULE_MEAN`;
- `Common_Hallmarks.csv` contains 1,900 rows = 19 cancers x 2 technical tracks x 50 Hallmarks, with zero duplicate cancer/track/Hallmark keys;
- common-eligibility logic reconstructs exactly as D1-source eligible AND D2-RNA mapping eligible AND D2-RNA PC1 evaluable, with zero mismatches;
- D1 source mapping flags in the returned common table match the audited D1 Hallmark table exactly;
- every cancer/track has exactly 45 common eligible Hallmarks, exceeding the frozen >=25 semantic-branch floor;
- the same five source-limited Hallmarks are refused in all 38 cancer/track groups: `HALLMARK_ANGIOGENESIS`, `HALLMARK_HEDGEHOG_SIGNALING`, `HALLMARK_NOTCH_SIGNALING`, `HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY`, and `HALLMARK_WNT_BETA_CATENIN_SIGNALING`.

The five common-Hallmark exclusions are therefore inherited from the methylation-source mapping gate. They are not RNA-PC1 failures: all 50 RNA targets are evaluable in every cancer.

## Leakage / claim firewall

The returned summary records:

- RNA values used only from `DISCOVERY`;
- no REPLICATION target scores generated;
- no FINAL_HOLDOUT target scores generated;
- no held-out values used for fit or decision;
- no partition reassignment;
- no biological chi;
- Stage C1 science unchanged.

The Stage A profile cache and Hallmark membership hashes match the frozen P0 inputs.

## Decision

P0 D2 is CLOSED PASS as a DISCOVERY-only RNA target-construction gate.

This gate does not establish predictive performance, cross-layer biological mechanism, clinical utility, temporal dynamics, biological chi, or a promoted pan-cancer result. The frozen P0 pan-cancer promotion floor remains 24 cancers; only 19 cancers are P0-evaluable, so pan-cancer summaries remain descriptive.

## Next gate

Proceed to a pre-result freeze and implementation of the DISCOVERY-only cross-layer audit-state machinery plus P1 model fitting. No REPLICATION or FINAL_HOLDOUT target values may be generated or inspected during that gate.
