# Meneses 2026 Immediate Context-Transport Closure

**Date:** 25 September 2026  
**Branch:** `bio-chi-meneses-context-transport-p0q-20260925`  
**Status:** CLOSED FOR THIS ITERATION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q literature-open same-source transport

## Status

The transport experiment executed successfully on all 143 frozen motor traces. Every source blob and every frozen per-condition trace count matched. The manuscript-facing constrained collapse/recovery fitter returned for every trace.

The experiment asked whether the immediate four-coordinate motor response organization identified in the sucrose/MB/CCW reference context transports across changes in non-ionic osmolyte, phosphate-buffer cation context, and clockwise-lock/strain context.

## Primary result

Collapse magnitude retained perfect monotonic dose ordering in every context: Spearman rho = 1.0 for sucrose/MB/CCW, sorbitol/MB/CCW, sucrose/SPB/CCW, and sucrose/CW-lock.

That shared amplitude ordering did **not** imply transport of the full multicoordinate geometry.

- Sorbitol versus sucrose: geometry rho = 0.7714, exact p = 1/24 = 0.0417. This missed the frozen strong-transport rho threshold of 0.8 and is retained as `PARTIAL_GEOMETRY_TRANSPORT_P0Q`.
- Sodium-phosphate buffer versus motility buffer under sucrose shock: geometry rho = -0.1429, exact p = 0.5833 despite amplitude rho = 1.0. This is `GEOMETRY_TRANSPORT_REFUSED_P0Q`.
- Clockwise-lock/strain context versus the CCW reference: geometry rho = 0.7714, exact p = 0.0417 with amplitude rho = 1.0. This is `PARTIAL_GEOMETRY_TRANSPORT_P0Q`. Because the source changes strain/plasmid background together with the clockwise lock, this is a context result rather than a pure rotor-direction causal estimate.

The whole-event disposition is therefore `IMMEDIATE_RESPONSE_ORGANIZATION_CONTEXT_DEPENDENT_P0Q`.

## Pooled representation

Across all 16 context-by-dose conditions, the common four-coordinate representation was strongly non-one-dimensional:

- PC1 variance fraction = 0.5198988599;
- maximum absolute standardized one-dimensional reconstruction residual = 2.1521372274;
- frozen one-dimensional adequacy = false;
- `Chi_bio = MULTICOORDINATE_IMMEDIATE_RESPONSE_ARCHITECTURE_REQUIRED_P0Q`.

Scalar `chi_bio` remains `NOT_OPENED_NOT_LICENSED`.

## SPB refusal root cause

The SPB refusal was investigated under a separately frozen post-result diagnostic rather than treated as a terminal blocker or removed as an inconvenient outlier.

It is not explained by a single coordinate. Leave-one-coordinate-out SPB geometry correlations were:

- omit collapse amplitude: -0.1429;
- omit collapse tau: 0.6000;
- omit recovery tau: 0.4286;
- omit recovery endpoint: -0.2571.

None restored the frozen strong-transport threshold.

It is not a median-versus-mean artifact. Mean-based SPB geometry rho was 0.2571 with exact p = 0.4167.

The 2,000-resample trace bootstrap centered close to zero: median rho = 0.0857, 95% interval [-0.7714, 0.8857], with only 18.95% of replicates at rho >= 0.5 and 41.85% at rho <= 0. Under the frozen diagnostic rules, the root-cause disposition is `DISTRIBUTED_CONTEXT_REORGANIZATION`.

This diagnostic does not promote or rewrite the primary refusal.

## Interpretation

The most stable source-level feature is perturbation-depth ordering: stronger shocks produce larger immediate motor collapse in every tested context. The **organization of collapse timing, recovery timing, and recovery endpoint around that depth coordinate is not invariant**. Sorbitol and the clockwise-lock/strain context preserve part of the sucrose geometry, whereas the sodium-phosphate-buffer context reorganizes it.

The result therefore sharpens the biological chi interpretation. A shared whole-system phenotype can coexist with context-dependent internal organization. Preserving only amplitude would conceal that reorganization; preserving the multicoordinate `Chi_bio` representation exposes it.

This does not establish a universal biological chi law, a potassium-specific mechanism, or a scalar boundary.

## Workflow identities

Primary transport run: `36216876191`  
Primary artifact: `10897867200`  
Primary artifact digest: `sha256:2bc6a34636d84954cb84f4c8bf9f841500f12a70a78b56d38e58250fb09ff0e6`  
Primary result JSON digest: `sha256:53debdf0a18cc73168b94c748437576437326b60ff8adb5dce133c7c0c845271`

Root-cause run: `36216972266`  
Root-cause artifact: `10897118026`  
Root-cause artifact digest: `sha256:745555a472c0b8dbc1ce49ddcc19063c26968db3c070661327639f983488ce50`  
Root-cause result JSON digest: `sha256:7781f434be4c198c0b706a607afbe1f08394c052fba2d67a7d7362dc8070db2e`

## What happens next and why

The next informative experiment should leave the Meneses same-source family. This source has now established direct recovery, multicoordinate representation, source-method robustness, partial transport, a context refusal, and the root cause of that refusal. Continuing to mine the same paper would risk source-specific overfitting.

Priority should move to an independent biological perturbation/recovery system with directly retrievable longitudinal data and enough observables to test whether context-dependent multicoordinate organization transports across acquisition lineage.

## What the user needs to do

Nothing is required before the next independent-source freeze.
