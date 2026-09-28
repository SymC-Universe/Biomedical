# Bio Chi C-Interior Function Map Postresult v1.0

**Status:** COMPLETE / P0-D FUNCTION MAP  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Plan:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_PACKET_v0.3.md\`  
**Freeze:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_FREEZE_v1.1.md\`

## Provenance

- Workflow: \`NSD Bio Chi C-Interior Function Map\`
- Run: \`36368579380\`
- Source head: \`45f74d8e3e8d027ab8b4bbb8572b81af0f00f55b\`
- Complete artifact: \`nsd-bio-chi-c-function-map-complete\`
- Artifact ID: \`10948327278\`
- Digest: \`sha256:cb4ceade9271c80a5b002f0b9f6ba791ae3e0ae049b64ede0a3fdb0aee2b5a0c\`

All four frozen mechanical preflight jobs passed. All 16 full-map cell jobs passed. Merge completed successfully.

The merged artifact contains exactly 96 rate-level rows and 48 paired same-path fine/coarse units.

## Full-envelope result

C1Q returned a fit for all 96/96 rate-level rows. This is a computational-completion result, not an admission result.

Across the complete frozen envelope:

- absolute C1Q \(\chi\) error: median \`0.0354734941\`, range \`0.0001918070\` to \`0.6827091730\`;
- absolute C1Q \(g\) error: median \`0.1344078717\`, range \`0.0004202380\` to \`1.7737918089\`;
- absolute natural-frequency error: median \`0.4255409757 Hz\`, range \`0.0132711972\` to \`106.2407031204 Hz\`;
- same-path practical C1Q \(\chi\) rate drift: median \`0.0126180976\`, maximum \`0.7182935518\`;
- same-path practical C1Q \(g\) rate drift: median \`0.1099697762\`, maximum \`1.8215100364\`.

Fine-rate rows were materially better than coarse-rate rows in the descriptive full-envelope summaries:

- fine median absolute \(\chi\) error: \`0.0221043159\`;
- coarse median absolute \(\chi\) error: \`0.0674911141\`;
- fine median absolute \(g\) error: \`0.0653805788\`;
- coarse median absolute \(g\) error: \`0.2731104666\`;
- fine median natural-frequency error: \`0.3862907608 Hz\`;
- coarse median natural-frequency error: \`0.7210328654 Hz\`.

These rate differences are practical finite-data estimator effects under fixed duration, not a violation of the exact continuous-lineage sampling invariance theorem.

## Function Map structure

The result is strongly heterogeneous rather than uniformly poor.

Cells 1, 2, 3, 4, 6, 10, 13, and 14 showed comparatively coherent recovery across seeds/rates. Several other cells showed a repeatable pathological solution in which C1Q approached the optimizer boundary, with fitted \(g\) effectively \(+1\), fitted \(\chi\) near 1, and natural frequency strongly distorted.

The boundary-collapse cells were:

\[
\{0,5,7,8,9,11,12,15\}.
\]

Twenty-one of 96 rows landed exactly on at least one raw optimizer box boundary. Twenty-six rows fitted \(g\) at the numerical saturation corresponding to the raw \(g\) bound. Those rows were concentrated in the eight cells above.

The most persistent case was cell 15, for which all six fine/coarse x seed rows converged to the pathological boundary branch. Cells 0 and 5 collapsed only at the coarse rate. Cell 7 collapsed at both rates for most seeds. Cells 8, 9, 11, and 12 were primarily coarse-rate failures.

This is evidence of a Function-Map boundary/conditioning problem for the current C1Q implementation. It is not evidence that those truth cells are outside family C; they were generated from exact C truths.

## Independent recurrence diagnostic

The generic covariance-recurrence diagnostic returned an underdamped pole estimate in 89/96 rows and explicitly refused seven rows. The refusals occurred in cells 8 and 12 and were preserved as \`REFUSE_NOT_UNDERDAMPED\` or \`REFUSE_NONSTABLE_B\`.

Across its 89 estimable rows:

- recurrence absolute \(\chi\) error median: \`0.0365213271\`;
- recurrence absolute \(\chi\) error maximum: \`0.3988880794\`;
- C1Q-versus-recurrence \(\chi\) disagreement median: \`0.0314148062\`;
- C1Q-versus-recurrence disagreement maximum: \`0.7130951123\`.

Post-hoc descriptive decomposition, **not a frozen threshold or admission rule**, shows that among rows with C1Q absolute \(\chi\) error greater than 0.1 and an available recurrence estimate, recurrence was closer to truth in 25/27 rows. For rows with C1Q error greater than 0.3 and an available recurrence estimate, recurrence was closer in 19/19 rows.

This does not promote the recurrence estimator. It indicates that many large C1Q misses cannot be attributed simply to absence of all second-order pole information in the realized signal.

## Current interpretation

The P0-D Function Map supports neither universal C1Q adequacy nor wholesale rejection of C1Q.

The supported interpretation is:

1. substantial regions of the frozen C interior are recoverable with useful finite-sample accuracy;
2. the current C1Q implementation also contains a reproducible pathological branch in which the likelihood/optimization solution moves toward \(g\approx+1\), \(\chi\approx1\), and distorted natural frequency;
3. coarse sampling increases the prevalence and magnitude of this pathology in the frozen map;
4. some cells exhibit the pathology even at 256 Hz, so it cannot be reduced to decimation alone;
5. the independent recurrence diagnostic often retains substantially better pole information in the same pathological rows, making a C1Q-specific likelihood/parameterization/optimization mechanism a live explanation;
6. no scientific admission threshold can be frozen from this exploratory map.

## Claim consequences

- **C1Q promotion:** no.
- **Real-EEG local \(\chi\) admission:** no.
- **Biological prevalence statement:** no.
- **Scientific threshold:** none.
- **Continuous-lineage C mathematics:** not falsified by this estimator map.
- **Current C1Q broad operating claim:** narrowed. C1Q is not presently qualified as a broadly reliable estimator across the full tested C interior.
- **Function Map / Limit Map balance:** restored. The map now contains both coherent interior regions and explicit estimator-failure regions.

## Root-cause requirement

Before expanding the biological search or defining an empirical admission rule, determine why the pathological C1Q branch wins.

The cheapest discriminating diagnostic is to use the already-frozen known-truth realizations and compare, for pathological rows:

1. C1Q negative log-likelihood at the generating truth coordinates;
2. negative log-likelihood at the selected pathological fit;
3. a truth-seeded local optimization basin;
4. the existing multi-start selected solution;
5. raw-bound and transformed-bound diagnostics.

Interpretation:

- if the truth-seeded basin reaches the selected boundary solution and the boundary has materially lower realized NLL, the problem is finite-sample likelihood geometry / weak information under the current parameterization;
- if a truth-seeded basin remains near truth with better NLL than the selected solution, the multi-start search is failing;
- if both basins are nearly tied, the region is practically weakly identified and should become a refusal/uncertainty target rather than an estimator-selection problem.

This diagnostic is P0-Q root-cause work and does not alter the frozen Function Map result.
