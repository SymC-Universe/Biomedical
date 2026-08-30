# Stage C1 methylation architecture preregistration

**STATUS: FROZEN — EXPLICITLY APPROVED BEFORE C1 BETA-VALUE BIOLOGICAL ANALYSIS**

Approval date: 2026-08-30

## Canonical approved contract

The scientific contract frozen by this preregistration is the exact pre-result Stage C1 v2 draft that was presented for approval and then explicitly approved by the user.

- Approved source document: `docs/STAGE_C1_ANALYSIS_CONTRACT_DRAFT_V2_20260830.md`
- Approved source blob SHA-1: `a39414c5990c234dc513569bd405b0237117d434`
- Draft-hardening commit: `425e39d040162ae55852e5fc51fc1867243399f3`
- Approval occurred after Stage C1A exact-probe inventory PASS and before any Stage C1 methylation beta-value biological result was calculated or inspected.

The draft filename is retained as a historical provenance object. Its `DRAFT` header records its state at the moment it was presented. This preregistration freezes that exact blob by hash; the scientific content may not be silently edited after C1 outcomes are known.

## Frozen analysis package

The approved v2 freezes all of the following together:

1. shared sample eligibility derived once from the `PRIMARY_PUBLICATION` 22,601-probe track and inherited unchanged by the 22,022-probe `MASKED_TECHNICAL` track;
2. publication-era beta scale, with no M-value or alternate-transform discovery branch;
3. 95% sample completeness, 95% probe completeness, and within-cancer probe-median imputation after eligibility;
4. fixed `n=30`, 100 deterministic without-replacement resamples, with cancer rather than resample as the inferential unit;
5. seed namespace `GRI_V2_C1_20260830` and SHA-256-derived 32-bit seeds from the exact approved token order;
6. all-probe sample-space modal Gram matrix `G = X X^T / p`, with complete 29-position normalized eigenspectrum and top-five mode contributions;
7. scalar compression `S_spec = 1 - H_norm` as primary and `S_PR = 1 - r_PR/29` as secondary, neither of which is chi;
8. exact within-probe permutation construction null preserving each probe's sampled marginal distribution while destroying cross-probe alignment;
9. full-modal methylation/RNA CKA bridge on identical patients plus patient-alignment null and top-five principal-angle diagnostics;
10. `PROMOTER_CORE = TSS200` as the primary conglomeration stratum;
11. unique-probe median gene methylation aggregation, annotation-supported multi-gene mapping, and no nearest-gene invention;
12. Hallmark methylation PC1 eigengenes with deterministic orientation, minimum 10 mapped genes, minimum 10 probes, and minimum 25 eligible Hallmarks per primary conglomeration resample;
13. absolute Spearman same-Hallmark methylation/RNA coupling with both patient-alignment and Hallmark-label nulls;
14. mandatory joint B1 ABSOLUTE-purity plus methylation-derived-leukocyte residualization for the strongest cross-layer promotion tier;
15. raw four-test family `H1`, `H2`, `H3a`, `H3b` with BH FDR at `q<0.05` separately by probe track;
16. composition-adjusted three-test family `H2_adj`, `H3a_adj`, `H3b_adj` with BH FDR at `q<0.05` separately by probe track;
17. minimum 24 eligible cancers for a promoted pan-cancer claim;
18. mandatory direction and significance agreement between publication-faithful and technical-mask tracks;
19. secondary regulatory strata and topology as non-rescuing context decomposition only;
20. failure retention with no post-result retuning of primary stratum, scalar, scaling, missingness, mask, nulls, direction, multiplicity family, `n`, or resample count.

## Frozen upstream identities

- methylation source SHA-256: `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`
- Stage A profile cache SHA-256: `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`
- Hallmark membership SHA-256: `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`
- B1 ABSOLUTE purity SHA-256: `f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd`
- B1 leukocyte-fraction SHA-256: `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`
- C1A probe-gene-region map SHA-256: `78f38d420a486427d67d88f67f5da83d1811003bf578b3c673f1dcbee5912296`
- C1A probe-flags SHA-256: `5777ff7331c4bae750ed1c87bb6eb93136c56ade6dbf8522829db1f5659ac455`
- primary probe count: `22601`
- masked technical probe count before C1 missingness eligibility: `22022`
- frozen technical-mask union: `579`

## Promotion ladder

### C1-1

Requires `H1` to pass on both probe tracks. This licenses only organized **static methylation geometry beyond exact probe marginals**.

### C1-2

Requires C1-1 plus raw `H2`, `H3a`, and `H3b` on both tracks. This licenses only **specific patient-aligned and Hallmark-identity-aligned static methylation/RNA architecture**.

### C1-3

Requires C1-2 plus `H2_adj`, `H3a_adj`, and `H3b_adj` on both tracks with at least 24 jointly eligible cancers. This licenses only **composition-robust specific static methylation/RNA architecture** relative to the frozen B1 purity/leukocyte covariates.

## Claim ceiling

Even C1-3 does **not** establish causality, substrate inheritance, temporal progression, memory, irreversibility, damping, recovery, critical slowing, an exceptional point, a phase transition, a cancer optimum, treatment response, a master stability score, biological chi, or `chi=1` as a cancer boundary.

Ordered/temporal or perturbational evidence remains mandatory for inheritance. A same-coordinate dynamic Gamma/Omega admission gate remains mandatory for biological chi.

## Execution rule

Implementation may now proceed mechanically. Before any real C1 beta-value biological result is inspected, the machine-readable config, mathematical kernel, source/loaders, null machinery, inference logic, and regression tests must agree with this frozen contract and pass CI. Mechanical failures may be repaired without changing frozen science. Any change to the scientific contract requires an explicit new version and cannot retroactively replace this preregistration.