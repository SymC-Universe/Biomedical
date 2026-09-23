# BioSystems independent prostate P1 confirmation freeze - 22 September 2026

**Status:** FROZEN BEFORE EXTERNAL MOLECULAR OUTCOME OPENING  
**Manuscript:** *Regulatory Architecture Across Human Cancers: Multiomic Evidence for Recurrent Methylation–Transcriptomic Organization*  
**Program authority:** SymC General Operations Manual v0.8.3  
**Revision branch:** `gri-biosystems-revision-20260922`  
**Purpose:** close the remaining BioSystems reviewer request for genuinely independent cohort validation without reopening biological chi or expanding the paper into the separate recovery program.

## 1. Why this source is selected

The decisive external source is the independent prostate multiomic family:

- RNA-seq: GSE237995;
- 450K methylation: GSE262522;
- EPIC methylation: GSE262524.

Selection is based only on source architecture and pre-outcome readiness already documented before any GRI result was opened:

- exact 121/121 RNA-to-methylation title crosswalk already closed;
- 68 samples use 450K and 53 use EPIC;
- exact metadata crosswalk artifact: GitHub Actions run `35733020358`, artifact `GRI_EXTERNAL_GEO_SOURCE_MANIFEST_SET_V01`, artifact ID `10696736434`, digest `sha256:f133746616509943ba385f4964b70ee66e4c3b8c028c909ef98382e61a362d36`;
- no GRI molecular quantity has been computed in this cohort.

The frozen crosswalk contains 63 unique participants. Platform/state inventory is:

| Platform | Tumor | Adjacent non-tumor | Complete paired participants |
|---|---:|---:|---:|
| 450K | 36 | 32 | 32 |
| EPIC | 27 | 26 | 26 |

The 450K paired subset is chosen as the primary P1 lane because it is closest to the array representation inherited by the TCGA C1 program and provides at least 30 complete paired participants. EPIC is a prospectively secondary platform-transport sensitivity and cannot rescue a failed 450K primary.

No cohort was chosen based on agreement with TCGA results.

## 2. Transported claim

The primary external claim is deliberately narrower than a new oncology theory:

> An independently acquired prostate cohort contains the same **static cross-layer architecture family** that defines the revised C1 claim: methylation organization above a construction floor, methylation-RNA patient geometry above patient shuffling, and patient-specific Hallmark coupling above its patient-shuffle null.

The primary transported endpoints are:

1. **P1-H1:** methylation spectral organization `delta_s > 0`;
2. **P1-H2:** methylation-RNA patient geometry `delta_cka > 0`;
3. **P1-H3a:** patient-specific Hallmark correspondence `delta_a_patient > 0`.

H3b same-label semantic advantage is not a primary confirmation endpoint because the internal program already established that it is small and support-sensitive.

No biological chi, damping ratio, critical boundary, treatment response, causal methylation direction, or clinical utility claim is transported.

## 3. Primary cohort and sample freeze

Primary cohort:
- platform: 450K only;
- participants: the 32 complete RNA+methylation tumor/adjacent pairs defined in the frozen metadata crosswalk;
- primary analysis size: n=30 paired participants;
- primary participant set: one deterministic outcome-blind draw of 30 from the 32 complete pairs;
- seed namespace: `GRI_BIOSYS_EXT_PROSTATE_P1_20260922`;
- seed token: `PRIMARY_450K_N30`;
- the same 30 participant identities are used in tumor and adjacent tissue.

The two participants not selected for the primary n=30 are not discarded from the record. A full n=32 sensitivity is mandatory and cannot rescue a failed primary.

No sample may be removed after molecular outcome opening except for a predeclared source-integrity failure that makes the sample scientifically unusable under the same rule in both tissue states.

## 4. Source and preprocessing rules

### RNA

Source: GSE237995 raw counts.

The external RNA representation must not reuse the TCGA EB++ values because the source platform and upstream processing are different.

Frozen external RNA normalization:
1. retain source genes with valid identifiers;
2. remove genes with zero total count across the primary paired cohort;
3. library-size normalize by the DESeq-style median-ratio size factor using the primary paired cohort without tissue labels entering the size-factor formula;
4. transform normalized counts by `log2(normalized_count + 1)`;
5. map to gene symbol using source annotation frozen before endpoint computation;
6. duplicate symbols are resolved by deterministic source order, retaining the first source feature;
7. Hallmark membership uses the same MSigDB release and minimum-gene rules as the revised manuscript where source support permits.

A source/namespace mapping audit is mandatory before endpoint opening. If gene identity cannot be frozen unambiguously, RNA-dependent endpoints refuse rather than using a result-guided mapping.

### Methylation

Primary source: GSE262522 450K processed normalized beta representation or, if the processed file identity cannot be independently bound, raw IDAT reconstructed with a prospectively fixed minfi/funnorm workflow.

Primary probe universe:
- 450K probe IDs present in the external source;
- intersect with the frozen C1 annotation/probe-gene-region map;
- apply the same C1 technical-mask sensitivity as a secondary track;
- no EPIC-only probe enters the primary 450K lane.

Within the primary cohort/state, the same 95% finite-completeness rule and state-symmetric common-probe intersection logic used in TN-C1 are retained where technically applicable.

## 5. Endpoint construction

The primary P1 endpoints transport the revised C1 constructions rather than inventing new external statistics.

### P1-H1

Use the C1 methylation spectral-concentration statistic and its probe-marginal construction floor.

Report:
- observed `S_spec`;
- null distribution;
- `delta_s = observed - null`;
- uncertainty;
- primary and masked-technical tracks.

### P1-H2

Use centered-kernel CKA between the paired methylation and RNA patient representations.

Use B=999 deterministic patient permutations of methylation patient labels relative to RNA.

Report:
- observed CKA;
- null median/mean/dispersion;
- `delta_cka`;
- headroom-normalized effect as a supporting effect size.

### P1-H3a

Use the frozen same-Hallmark methylation/RNA patient-coupling definition on the common evaluable Hallmark set.

Use B=999 deterministic patient permutations.

Report:
- observed same-Hallmark coupling;
- patient-null distribution;
- `delta_a_patient`.

Minimum common-Hallmark support remains prospectively enforced. If support is insufficient, H3a is `NOT_EVALUABLE`; H1/H2 may still stand separately.

## 6. Primary decision rule

The external cohort is a single cancer, so the internal pan-cancer sign test is not transplanted.

For each primary endpoint, the decisive inferential object is its own construction/patient permutation null.

The primary family is H1/H2/H3a. Use two-sided or upper-tail null probability as mathematically appropriate to the frozen endpoint construction, then control the three primary endpoint p-values by Benjamini-Hochberg.

Outcome classes:

- `P1_FULL_TRANSPORT`: H1, H2, and H3a all remain positive with BH q<0.05 on the primary 450K lane.
- `P1_PARTIAL_TRANSPORT`: at least one but not all primary endpoints passes; report exactly which architecture layers transport.
- `P1_NO_TRANSPORT`: none passes.
- `P1_REPRESENTATION_DEPENDENT`: primary and mandatory justified representation/technical sensitivity materially conflict.
- `P1_INDETERMINATE`: source/support/identity failure prevents a valid decision.

No endpoint may rescue another endpoint.

## 7. Independent tumor-normal corroboration, secondary

Because this cohort contains paired tumor and adjacent tissue, a secondary external corroboration asks whether the newly closed TCGA tumor-normal RNA direction transports.

Using the same primary 30 paired participants:
- compute Stage-A-style RNA `C_in,pair`, `C_in,PC1`, and `C_out` separately by state;
- compute tumor-minus-adjacent effect;
- evaluate the cohort-level difference by B=999 deterministic within-participant tumor/adjacent label swaps;
- BH across the three RNA quantities.

The transported directional hypothesis, now frozen from the internal result, is **tumor < adjacent** for all three RNA coordinates.

This is secondary to P1-H1/H2/H3a and cannot rescue the external architecture result.

A secondary H1 tumor-minus-adjacent contrast may also be reported using the same paired-label-swap framework.

## 8. EPIC platform sensitivity

The 26 complete EPIC pairs are a mandatory platform sensitivity.

They use:
- all 26 complete paired participants;
- the same source gene representation;
- methylation probes restricted to the C1-compatible/common platform carrier;
- the same endpoint formulas and null logic.

EPIC cannot rescue a failed 450K primary.

Material sign reversal or endpoint-class disagreement is reported as platform dependence.

## 9. Native/simple comparator record

The exact confirmatory task is **transport of the previously frozen C1 null-corrected architecture quantities**.

Nearest standard multi-view methods considered include MOFA, similarity network fusion, and DIABLO. These methods answer broader latent-factor, network-fusion, or supervised integration questions rather than the exact transported null-corrected H1/H2/H3a task.

Comparator status for this P1 task is therefore:

`NO_NATIVE_COMPARATOR_FOR_EXACT_TRANSPORT_TASK`

This does not waive domain-native competition. The strongest relevant alternatives are the endpoint-specific construction and patient-shuffle nulls plus the mandatory platform/technical sensitivities. The paper may not claim superiority over MOFA, SNF, DIABLO, or the standard multi-omics toolkit.

## 10. Independence and leakage firewall

- External source is independent of TCGA acquisition/processing.
- External outcomes have not been used to design C1 or TN-A1/TN-C1.
- The internal result determines the transported question, not the external data.
- No external representation dimension, feature threshold, module subset, normalization choice, platform subset, or endpoint is selected because it agrees with TCGA.
- The primary 450K lane and secondary EPIC lane are fixed before biological endpoint computation.
- A failed external result remains failed and is not converted into a new discovery cohort inside this submission lineage.

## 11. MFR-14 disposition

MFR-01 question: frozen above.  
MFR-02 prediction/falsifier: exact transported endpoint outcome classes frozen above.  
MFR-03 provenance: source accessions and metadata crosswalk already frozen; molecular file hashes must be recorded at execution.  
MFR-04 representation/validity regime: frozen above.  
MFR-05 native comparator: `NO_NATIVE_COMPARATOR_FOR_EXACT_TRANSPORT_TASK`, nearest alternatives documented.  
MFR-06 strongest relevant null/alternative: construction null, patient shuffle, paired state-swap, technical-mask and platform sensitivity.  
MFR-07 decision rule: frozen above.  
MFR-08 uncertainty: permutation distributions, construction stability, endpoint effect sizes.  
MFR-09 multiplicity: BH across H1/H2/H3a; RNA secondary family separate.  
MFR-10 dependence/hierarchy: participant pairing preserved; resamples never treated as independent biological observations.  
MFR-11 untouched evidence: external molecular endpoints remain unopened for GRI.  
MFR-12 refusal/error behavior: explicit NOT_EVALUABLE/INDETERMINATE states.  
MFR-13 evidence-independence audit: independent external cohort, with internal question transport declared.  
MFR-14 cold reconstruction: source/config/code/environment/result hashes and reviewer index required before manuscript promotion.

## 12. Stop rule

After this freeze, no change to:
- source family;
- primary platform;
- primary n;
- participant-selection seed;
- normalization family;
- endpoint family;
- Hallmark source;
- null type;
- permutation count;
- multiplicity family;
- primary outcome classes;
- sensitivity role

may be made in response to the external result.

A mechanical source-format correction is versioned and must leave the scientific contract unchanged. A scientifically material change creates a new external lineage and cannot rescue this P1 result.

## 13. Manuscript consequence

If P1 fully or partially transports, the revised manuscript may report genuine external confirmation at the exact layer(s) earned.

If P1 fails, the manuscript will report that the TCGA architecture did not transport under this independent prostate representation and narrow the claim accordingly.

In no outcome does this external task admit biological chi or test the recovery hypothesis.
