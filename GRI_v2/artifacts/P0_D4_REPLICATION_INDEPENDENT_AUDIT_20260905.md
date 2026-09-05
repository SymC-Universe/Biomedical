# P0 D4 REPLICATION independent audit
Status: **CLOSED PASS WITH ONE PRE-RESULT METADATA COUNT CORRECTION**

## Provenance
- D4 was completed from the exact uploaded resilient-run methylation and RNA projection checkpoints.
- Checkpoint SHA sidecars matched their files exactly.
- Embedded checkpoint keys matched the exact resilient implementation/config/source identities.
- Both projected score tables passed the package's frozen shape, participant, cancer, duplicate, and finite-value validators.
- The frozen small inputs remained the exact 18/18 hashed D4 dependencies.
- FINAL_HOLDOUT remained sealed.

## Mechanical count correction
The original D4 config asserted 1,478 composition-complete REPLICATION participants and BRCA=195. Independent reconstruction of the already-frozen B1 covariate attachment rule from the exact frozen split/purity/leukocyte files yields **1,479 total and BRCA=196**. Every other cancer matches the frozen count. This is a metadata/assertion error, not a scientific retuning: no participant was reassigned, imputed, or selectively excluded, and no replication audit statistic or prediction error was used to choose the correction. The correction is committed separately as a mechanical metadata correction.

## Independent output integrity checks
- `SHA256SUMS.txt` matches every listed output.
- `Replication_Result.zip` is internally clean and contains the expected 16 result members.
- Replication methylation scores: 146,250 rows = 1,625 participants × 2 technical tracks × 45 source Hallmarks; zero duplicate score keys; zero non-finite scores.
- Replication RNA scores: 81,250 rows = 1,625 participants × 50 RNA Hallmarks; zero duplicate score keys; zero non-finite scores.
- All output rows map only to frozen REPLICATION participants. No FINAL_HOLDOUT participant appears in methylation, RNA, or covariate outputs.
- Prediction metrics were independently reconstructed from the frozen D3 model parameters and D3 target-reference means/variances with zero material mismatches.
- Replication states were independently reconstructed from the frozen D4 metric/state logic with zero state mismatches.

## D4 result
- Five-state agreement: **18/19 cancers = 0.9474**.
- Replication states: **18 GLOBAL_SHARED_ONLY; 1 WITHIN_LAYER_ONLY (PCPG)**.
- Decisions: **18 CAUTION; 1 REFUSE (PCPG); 0 ACCEPT**.
- Discovery ACCEPT prediction was zero in all cancers and replication ACCEPT was also zero in all cancers, so ACCEPT/non-ACCEPT accuracy is 19/19 but precision/recall/MCC are not evaluable because the positive class is absent.
- PCPG is the only five-state disagreement: discovery `GLOBAL_SHARED_ONLY/CAUTION` → replication `WITHIN_LAYER_ONLY/REFUSE`. Its PRIMARY_PUBLICATION raw global CKA screen fails the frozen permutation criterion, while within-layer organization remains detectable.
- PRAD remains `GLOBAL_SHARED_ONLY/CAUTION`; a masked-technical raw semantic screen passes, but the full frozen cross-track/composition semantic rule does not, so it is not promoted.

## P1 held-out prediction
- `ALL_METHYLATION_RIDGE` has lower cancer-median normalized MSE than `COVARIATE_ONLY` in **18/19 cancers**.
- Exact one-sided paired sign test: **18 wins / 19 non-ties, p=3.8146973e-05**. Per the preregistration, this remains descriptive because 19 < the frozen 24-cancer pan-cancer promotion floor.
- Median cancer-level normalized MSE: ALL_METHYLATION_RIDGE ≈ **0.4755** vs COVARIATE_ONLY ≈ **0.6708**.
- Median cancer-level held-out R² relative to the discovery target mean: ALL_METHYLATION_RIDGE ≈ **0.4901** vs COVARIATE_ONLY ≈ **0.2694**.
- PCPG is the lone cancer where the all-methylation model is worse than the covariate-only model on the frozen primary cancer-median nMSE contrast.

## P2 replication of discovery audit state
- Raw PRIMARY_PUBLICATION global CKA passes in 18/19 cancers; PCPG fails.
- Adjusted PRIMARY_PUBLICATION global CKA passes in 18/19 cancers; COAD fails.
- No cancer satisfies the full Hallmark-label-specific semantic promotion rule. The discovery semantic failure therefore replicates at the full decision level.
- Hallmark `PRESERVED_POSITIVE_BOTH` fraction median across cancers ≈ **0.4222**, range **0.2222–0.5556**. This is a sign/effect-preservation diagnostic, not a new significance claim.

## Claim boundary
D4 now supports **held-out internal TCGA replication/prediction under the frozen architecture**: the all-methylation model generally improves over the composition-only comparator, and the discovery-level global-shared/caution state is reproduced in 18/19 cancers. It also confirms that the stronger Hallmark-label-specific semantic claim should remain rejected. D4 does not establish external validation, clinical utility, mechanism, causal substrate inheritance, temporal dynamics, damping, exceptional points, or biological χ.

## Decision
**D4 is CLOSED PASS WITH ONE PRE-RESULT METADATA COUNT CORRECTION.** The scientific architecture is not retuned from REPLICATION. The next gate is to freeze the P3 FINAL_HOLDOUT implementation before opening FINAL_HOLDOUT.
