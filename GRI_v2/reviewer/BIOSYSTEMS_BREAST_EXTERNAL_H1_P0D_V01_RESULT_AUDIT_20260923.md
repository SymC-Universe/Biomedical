# BioSystems breast external H1 P0-D v0.1 result audit

**Date:** 23 September 2026  
**Status:** `PASS_SECOND_EXTERNAL_H1_P0D`  
**Workflow run:** `35891832779`  
**Workflow head:** `4680bfc7be4298a7b6a64e321aacf1713b80d056`  
**Artifact:** `10765586444`  
**Artifact digest:** `sha256:1503d2c03a672be642215acca261983eb62384dfbe8b1c80b04bfcf2b06b5986`

## Source

- GEO: `GSE58999`
- platform: Illumina HumanMethylation450
- design: 44 matched primary breast tumors and regional/lymph-node metastases
- downloaded series-matrix SHA-256: `3bbde8e6c71a29f3d7609ff5597895a67f231e31d26c6d86e5b50c10a5b9fe4b`

The first workflow attempt failed before source-value parsing because the runner carried a stale hard-coded support-file transport hash. The scientific carrier itself was unchanged. The repair replaced the stale transport-string assertion with semantic validation of the current frozen C1 support payload:
- 3,999 promoter-core rows;
- 579 technical-mask probes;
- all 579 mask probes aligned to the C1 carrier.
The decoded support SHA remained `d45947345007b901e684adf92840889acf1ab00377153d54de2766cd1084c9b2` and the payload SHA remained `1463a4a6ad157dc770278ef97b6fcd2fb80b6e73ce4d774a2ca47aa7870391b1`. No scientific rule changed.

## Frozen sample rule

Thirty patients were selected by ascending SHA-256 of:
`BIOSYSTEMS_BREAST_H1_EXTERNAL_V01|patient_id`

before methylation values were interpreted.

The paired metastases from those same participants were mandatory sensitivities. The full 44-pair source was a second mandatory sensitivity.

## Results

| Lane | n | probes | H1 observed | null median | delta S | p |
|---|---:|---:|---:|---:|---:|---:|
| Primary n30 publication | 30 | 22,462 | 0.150739 | 0.000548 | +0.150191 | 0.001 |
| Primary n30 masked | 30 | 21,886 | 0.151146 | 0.000565 | +0.150581 | 0.001 |
| Metastasis n30 publication | 30 | 22,462 | 0.189926 | 0.000544 | +0.189381 | 0.001 |
| Metastasis n30 masked | 30 | 21,886 | 0.190547 | 0.000564 | +0.189983 | 0.001 |
| Primary full n44 | 44 | 22,543 | 0.166256 | 0.000713 | +0.165543 | 0.005 |
| Metastasis full n44 | 44 | 22,543 | 0.203346 | 0.000713 | +0.202633 | 0.005 |

The full-n44 p-values are at the B=199 Monte-Carlo floor and are not finer-resolution estimates.

Frozen primary P0-D success rule: **PASS**.

## Interpretation

The H1 within-methylation covariance result now has post-result external corroboration in a second cancer type and independent GEO cohort in addition to the prospectively frozen prostate P1 result.

This breast result is scientifically valuable because:
- it is independent of TCGA/PanCan patient data;
- it uses the same frozen C1 probe carrier rather than outcome-selected breast probes;
- the primary-tumor effect (+0.150) is materially closer to the TCGA pan-cancer range than the larger external prostate effect (~+0.303 to +0.358);
- H1 is also present in matched metastases.

## Claim ceiling

`P0_D_POSTRESULT_EXTERNAL_CORROBORATION`

This does not:
- retroactively become untouched P1 evidence for the already-viewed BioSystems claim;
- establish H2/H3 transport in breast;
- prove composition independence;
- establish diagnostic/prognostic utility;
- establish causality, recovery, biological chi, or a universal boundary.

For the current BioSystems revision, no third external H1 cohort is scientifically required unless a new reviewer specifically requests one.
