# BioSystems independent prostate P1 post-result audit

**Date:** 22 September 2026  
**Status:** COMPLETE / EXTERNAL RESULT OPENED  
**Workflow:** GitHub Actions run `35801966289`  
**Head SHA:** `e410257c95fddc50b39bc147b4780d214f731d0e`  
**Artifact:** `GRI_BIOSYSTEMS_EXTERNAL_PROSTATE_P1_V01`  
**Artifact ID:** `10726636434`  
**Artifact digest:** `sha256:1d7bbef7a4f8ea0cb254c139879e8ec53b9498f8d95c9c97fa28f21367075cde`  
**Parent freeze:** `BIOSYSTEMS_EXTERNAL_PROSTATE_P1_FREEZE_20260922.md`  
**Execution clarification:** `BIOSYSTEMS_EXTERNAL_PROSTATE_P1_EXECUTION_CLARIFICATION_20260922.md`  
**Claim ceiling:** independent external static-architecture transport only. No biological chi, causal methylation-to-RNA direction, recovery, treatment response, clinical utility, or universal boundary claim.

## 1. Execution integrity

The frozen independent prostate task completed successfully on:

- RNA: GSE237995;
- 450K methylation: GSE262522;
- EPIC methylation sensitivity: GSE262524;
- exact frozen MSigDB 2026.1 Hallmark GMT;
- exact frozen 22,601-probe C1 carrier;
- exact frozen C1 promoter-core map and technical mask.

Source hashes matched the outcome-blind source-preflight identities:

- RNA SHA-256 `9f94093f3254e1478d37f0b888d8f652e1d7bbf7f6265dd81f15d4d490f8cc92`;
- 450K SHA-256 `90a7a8c12343831524a9711be7e0b3f33f297fe408662fa68c5efa49a7c862d0`;
- EPIC SHA-256 `b55bf7b2e427c27e84a331c7f8c07f296dd64c07fa54c74445bb40288777e69f`;
- Hallmark GMT SHA-256 `eecaf6dad908334ae885406ec72bdc0646d8917588ed7c219fac92fc5363f596`.

Primary n=30 and full n=32 450K lanes retained all 22,601 C1 probes before technical masking; the EPIC lane retained 21,439 shared C1-compatible probes. The masked-technical tracks removed 579 probes on 450K and 559 on EPIC.

No endpoint, sample set, null, seed, multiplicity family, sensitivity role, or decision rule was altered after outcome opening.

## 2. Frozen primary 450K n=30 result

Primary-publication track:

| Endpoint | Observed | Null median | Effect | p | BH q | Result |
|---|---:|---:|---:|---:|---:|---|
| H1 methylation spectral organization | 0.303894 | 0.000804 | +0.303090 | 0.001 | 0.003 | PASS |
| H2 methylation-RNA patient geometry | 0.257193 | 0.237469 | +0.019724 | 0.271 | 0.4065 | unresolved |
| H3a patient-specific Hallmark coupling | 0.077197 | 0.117686 | -0.040489 | 0.813 | 0.813 | no transport |

Frozen primary classification before sensitivities:

`P1_PARTIAL_TRANSPORT`

Only H1 clears the prespecified BH-q<0.05 primary family.

The technical-mask track reproduces the same primary endpoint statuses:
- H1 effect +0.306173, q=0.003;
- H2 effect +0.017086, q=0.4635;
- H3a effect -0.040934, q=0.81.

Therefore the primary result is not driven by the frozen technical-probe mask.

## 3. Full n=32 450K sensitivity

The mandatory all-pair 450K sensitivity reproduces the primary qualitative result without conflict:

- H1 effect +0.317045, q=0.003;
- H2 effect +0.016723, q=0.426;
- H3a effect -0.007331, q=0.549.

Masked-technical results again preserve endpoint status.

Frozen conflict list: empty.

This supports the stability of the primary 450K conclusion to the two held-out complete participant pairs.

## 4. EPIC n=26 platform sensitivity

The mandatory EPIC lane gives:

- H1 effect +0.358394, q=0.003;
- H2 effect -0.017032, q=0.69;
- H3a effect +0.030769, q=0.5175.

The technical-mask track is concordant within EPIC.

H1 therefore transports across both independent methylation platforms.

However, H2 changes from a small positive effect on 450K to a small negative effect on EPIC, and H3a changes from negative on 450K to positive on EPIC. Neither H2 nor H3a is significant on either platform, but the preregistered sensitivity rule classifies sign reversal as a material conflict.

Frozen sensitivity conflicts:
- `H2:effect_sign`;
- `H3a:effect_sign`.

Therefore the final preregistered external outcome is:

`P1_REPRESENTATION_DEPENDENT`

This classification must not be softened to full external validation.

## 5. Secondary paired tumor-normal RNA corroboration

The prospectively secondary external RNA comparison did not reproduce the strong pan-cancer internal tumor-normal result at q<0.05 in this prostate cohort.

Primary n=30 paired participants:

- pairwise internal coherence: tumor - adjacent = -0.013484, q=0.504;
- PC1 organization: tumor - adjacent = -0.008643, q=0.504;
- external coupling: tumor - adjacent = +0.000990, q=0.504.

The first two quantities move in the internally predicted direction but are unresolved. External coupling is essentially unchanged and slightly positive.

Disposition:

`SECONDARY_TN_NOT_CONFIRMED_IN_EXTERNAL_PROSTATE`

This does not invalidate the internal pan-cancer tumor-normal result. It limits its transport to this single independent prostate cohort.

## 6. What externally transports

The strongest external result is H1.

Across:
- primary 450K n=30;
- masked 450K n=30;
- full 450K n=32;
- masked full 450K n=32;
- EPIC n=26;
- masked EPIC n=26,

H1 is positive and clears BH q=0.003 in every prespecified lane.

Observed spectral concentration is hundreds of times larger than the independently column-permuted construction floor.

Therefore the independent cohort provides strong evidence that **within-methylation patient-resolved organization above a probe-marginal construction null is not specific to TCGA or to one methylation platform**.

## 7. What does not externally transport cleanly

The independent study does not confirm a universal cross-layer methylation-RNA geometry or same-Hallmark patient-coupling effect under the frozen representation.

- H2 is positive but unresolved on 450K and negative but unresolved on EPIC.
- H3a is negative on 450K and positive on EPIC, unresolved in both.
- the external paired RNA tumor-normal contrast does not reach the frozen significance threshold.

These are Limit-Map findings and remain visible.

## 8. Reviewer-facing interpretation

The reviewer request for independent validation is now **executed and answered**, but the scientifically correct answer is partial and representation-dependent rather than uniformly positive.

The revised manuscript can state:

1. an independent prostate cohort strongly reproduces the methylation-organization H1 result under the exact frozen C1 probe carrier and null construction;
2. the H1 result survives a second methylation platform;
3. H2/H3a do not transport consistently and therefore remain TCGA/internal architecture findings rather than externally established universal features;
4. the independent prostate cohort does not confirm the internal pan-cancer tumor-normal RNA shift.

This is stronger than omitting external validation because the independent test was prospectively frozen, allowed to fail, and reports both transported and non-transported layers.

## 9. GOM disposition

Function Map:
- H1 external transport: supported;
- H1 cross-platform robustness: supported.

Limit Map:
- H2 external transport: unresolved / platform-sign dependent;
- H3a external transport: not established / platform-sign dependent;
- secondary tumor-normal RNA transport: not confirmed.

No averaging of these outcomes is allowed.

## Final disposition

```text
primary_450K_n30 = P1_PARTIAL_TRANSPORT
full_450K_n32 = CONCORDANT_WITH_PRIMARY
EPIC_n26 = H1_TRANSPORT_WITH_H2_H3A_SIGN_CONFLICT
final_external_P1 = P1_REPRESENTATION_DEPENDENT
independent_H1_validation = SUPPORTED
independent_H2_validation = NOT_ESTABLISHED
independent_H3a_validation = NOT_ESTABLISHED
external_tumor_normal_RNA_replication = NOT_CONFIRMED
```
