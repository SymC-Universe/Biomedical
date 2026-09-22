# GRI oncology handoff - 22 September 2026

**Purpose:** Preserve the work accidentally advanced in the oncology/GRI lane before returning to NSD.  
**Status:** HANDOFF ONLY. No editor contact sent. No new biological outcome was opened by the work below.

## Work completed

1. **SCC25 scalar-admission post-result audit**
   - Workflow run 35671381706 completed.
   - Rank 2: no complex-conjugate pair in 33/33 required fits.
   - Rank 3: complex-pair structure in 32/33 required fits but representation-dependent across frozen rank alternatives.
   - No continuous generator or logarithm branch licensed.
   - rho(T) not promoted to biological chi.
   - Current SCC25 scalar-chi branch is refused for this representation.
   - Joint chi/capital-Chi investigation must proceed through the no-scalar local/modal branch unless a future prospective derivation earns a scalar independently.
   - Canonical record added: GRI_v2/docs/GRI_SCC25_G2_SCALAR_ADMISSION_POSTRESULT_AUDIT_20260922.md
   - Joint-meaning packet and current-status note updated.

2. **Next SCC25 joint-meaning science decision packet**
   - Added GRI_v2/docs/GRI_SCC25_JOINT_MEANING_NEXT_SCIENCE_DECISION_PACKET_20260922.md
   - Freezes the scientific decisions that still require user approval before the next outcome-bearing SCC25 run: local/modal object, capital-Chi block construction, normalization, CoGAPS role, held-out temporal task, incremental-value metric, refusal/representation-dependence rules, and stopping rule.

3. **External GEO source/identity freeze**
   - Workflow run 35733020358 succeeded.
   - Exact GEO MINiML source identities were frozen for:
     - prostate: GSE237995, GSE262522, GSE262524;
     - breast: GSE57968, GSE58999;
     - melanoma: GSE65183, GSE65184, GSE65185.
   - No GRI features were computed and no P1 cohort was selected.
   - Breast: 72/72 expression samples matched one methylation sample across 36 complete patient pairs; 16 methylation-only samples retained outside the paired expression crosswalk.
   - Prostate: 121/121 RNA samples matched one methylation sample; 68 450K + 53 EPIC.
   - Melanoma: 218 rows inventoried; 192 human + 26 cell-model; three title/description identity conflicts found and quarantined:
     - GSM1588907 Pt22-DDP1 vs description naming Patient 21;
     - GSM1588908 Pt22-DDP2 vs description naming Patient 21;
     - GSM1588909 Pt22-DDP3 vs description naming Patient 21.
   - Canonical record added: GRI_v2/docs/GRI_EXTERNAL_GEO_IDENTITY_POSTRESULT_AUDIT_20260922.md
   - MFR-14 readiness matrix updated accordingly.
   - Artifact: GRI_EXTERNAL_GEO_SOURCE_MANIFEST_SET_V01, run 35733020358, artifact 10696736434.

4. **Large R/S source verification**
   - Initial combined streamed verifier failed mechanically when GDC dropped one byte-range connection during the large methylation stream. No hash mismatch occurred.
   - Verifier was hardened and split into independent R and S jobs using 16 MiB ranges and 8 retries.
   - RNA R block completed successfully:
     - bytes: 1,882,540,959
     - SHA-256: 674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658
     - exact hash match: TRUE
     - run 35733676268, job 106765830019
   - Methylation S block was still in progress when this handoff was written.
   - Workflow: .github/workflows/gri-conglomerate-rs-stream-verify.yml
   - Script: GRI_v2/src/stream_verify_conglomerate_rs_sources.py

5. **Stage C1 recovery/run-economy audit**
   - Historical Stage C1 was confirmed complete and immutable from retained artifacts:
     - 32 cancers;
     - 9,457 shared eligible samples;
     - 100 resamples/cancer;
     - C1-1/C1-2/C1-3 historically passed under the frozen contract;
     - biological chi not used.
   - Full per-cancer top-five probe-contribution NPY arrays were intentionally retained as local-heavy outputs. Their filenames/sizes/SHA-256s survive, but connected project/library surfaces do not expose the raw NPY bytes.
   - Conclusion: do not rerun the ~5 GB Stage C1 merely to materialize a new patient-level capital-Chi carrier. Recover original heavy bytes if possible; otherwise rerun only if a prospectively frozen future task proves those exact patient-level values are necessary.
   - Canonical record added: GRI_v2/docs/GRI_C1_CARRIER_MATERIALIZATION_RECOVERY_BOUNDARY_20260922.md

## Editor-contact status

No BioSystems editor was contacted. Gmail search did not surface a usable manuscript-id/handling-editor thread. Any editor update should remain a later oncology task after the current investigation matures.

## Resume point for GRI

When oncology is resumed:
1. inspect the S-block streamed verification result from run 35733676268;
2. close exact R/S source identity if S passes;
3. do not run the next SCC25 joint-meaning outcome until the A-H science decisions in the 20260922 decision packet are approved/frozen;
4. preserve the melanoma source-identity anomalies explicitly;
5. do not rerun Stage C1 unless the next frozen task truly requires unavailable patient-level heavy outputs.
