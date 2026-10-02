# Bio Chi C1Q Likelihood-Basin Root-Cause Postresult v1.0

**Status:** COMPLETE / P0-Q ROOT-CAUSE RESULT  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Plan:** \`NSD_vNext/docs/BIO_CHI_C1Q_LIKELIHOOD_BASIN_PLAN_v0.1.md\`  
**Freeze:** \`NSD_vNext/docs/BIO_CHI_C1Q_LIKELIHOOD_BASIN_FREEZE_v1.0.md\`

## Provenance

- Workflow: \`NSD C1Q Likelihood Basin Root Cause\`
- Run: \`36369682759\`
- Source head: \`d68c50c4398417beec1bd65158ee56bcc64b1598\`
- Complete artifact: \`nsd-c1q-likelihood-basin-complete\`
- Artifact ID: \`10948127976\`
- Artifact digest: \`sha256:f8d5c1eae3a38d8b8751190767e78e264c91c44a1edacaf85619a781e9e1a105\`
- Parent Function Map artifact: \`10948327278\`, digest \`sha256:cb4ceade9271c80a5b002f0b9f6ba791ae3e0ae049b64ede0a3fdb0aee2b5a0c\`

All eight frozen cell jobs and the merge completed successfully. All 48 source rows reproduced the stored selected-fit NLL within the frozen mechanical tolerance.

## Result

The dominant mechanism is a failure of the current global multistart search to reach a better C1Q likelihood basin, especially after decimation.

Across the 48 frozen rows:

- source NLL reproduced: **48/48**;
- truth-seeded local optimization beat the stored selected solution: **29/48**;
- by rate, truth-seeded local optimization beat the stored solution in **23/24 coarse** rows and **6/24 fine** rows;
- a local polish started from the stored selected solution beat the stored solution in only **8/48** rows;
- the stored selected fit had lower NLL than the population generating coordinates in only **20/48** rows.

The continuous NLL differences are highly asymmetric by sampling rate. For selected-fit NLL minus population-truth NLL:

- fine-rate median: approximately **-1.216**;
- coarse-rate median: approximately **+25.330**;
- overall median: approximately **+3.032**;
- overall range: approximately **-5.812 to +122.879**.

For truth-seeded-local NLL minus stored-selected NLL:

- fine-rate median: approximately **0** at numerical scale, with six material lower-basin recoveries;
- coarse-rate median: approximately **-27.040**;
- overall median: approximately **-5.626**;
- overall minimum: approximately **-124.727**.

Thus many coarse boundary-collapse fits were not merely different finite-sample optima. Their likelihood was substantially worse than both the generating reference and a truth-seeded local basin.

## Local convergence versus basin-selection failure

Only eight rows improved materially when the stored selected coordinates were locally polished. This shows that incomplete local convergence explains a minority of the failures.

In most boundary-collapse rows, polishing from the selected solution stays in the pathological basin, while a truth-seeded start reaches a distinct, substantially lower-NLL basin. Examples include:

- cell 5 coarse rows: truth-seeded basin improves NLL by roughly 99 to 125 relative to the stored boundary branch;
- cell 15, all six rows: truth-seeded basin improves NLL by roughly 36 to 115;
- cell 0 coarse rows: improvement roughly 22 to 36;
- cell 8 coarse failures: improvement roughly 63 and 83;
- cell 7, all six rows: improvement roughly 4 to 12.

Cell 15 is especially informative because the failure occurs at both rates and all seeds. The better truth-seeded solutions recover \(\chi\) and \(g\) in ordinary interior regions rather than at the \(g\approx+1,\chi\approx1\) boundary attractor.

## Scientific interpretation

The current evidence supports the following root-cause hierarchy:

1. **Current C1Q multistart initialization/search is inadequate over a material part of the tested C interior.**
2. The dominant bad branch is a separate local likelihood basin near the numerical/physical boundary.
3. Coarse sampling strongly increases the probability that the current search enters or selects that basin, but the same mechanism can occur at the fine rate.
4. Weak finite-sample identification may still contribute to some rows, but it cannot explain the large-NLL boundary selections as optimal finite-sample solutions.
5. The C-family mathematics is not falsified by this result.
6. The C1Q likelihood formulation is not independently validated by this diagnostic; the result only shows that the current search route fails to optimize that formulation reliably.

## Claim consequences

- **C1Q as currently searched:** not qualified across the intended C interior.
- **C1Q likelihood family:** remains a live qualification candidate, pending a data-derived search-route test.
- **Continuous-lineage C:** not falsified.
- **Real-EEG local \(\chi\):** remains unlicensed.
- **Scientific threshold:** none.
- **Biological prevalence:** none.
- **Production code:** unchanged.

## Post-execution deviation audit

Execution matched the frozen APQ-1 plan:

- all 48 frozen rows were included;
- the immutable parent artifact was used;
- source NLL reproduction passed 48/48;
- generating-coordinate, truth-seeded-local, stored-selected, and selected-polish comparisons were executed;
- no row was excluded for an unfavorable result;
- no scientific threshold was introduced;
- C1Q was not modified during the diagnostic.

The local container attempt timed out before completing the full row set but independently reproduced the same mechanism in partial rows. It is infrastructure corroboration only; the GitHub workflow artifact is the source of record.

## Next discriminating test

Before changing C1Q, test whether a **truth-blind, data-derived recurrence/covariance initialization** can reach the lower likelihood basin on the same 48 rows.

The seed should be constructed from positive-lag sample covariance:

1. fit the generic second-order recurrence to obtain \(\rho\) and \(\theta\);
2. conditionally fit the linear covariance amplitudes \(A\) and \(H\);
3. convert \(H\) to continuous-lineage \(g\) where the C mapping is admissible;
4. start one local C1Q optimization from that data-derived point;
5. compare its NLL continuously with the stored selected basin and the already-computed truth-seeded basin.

If this truth-blind seed recovers the lower basin broadly, the next engineering step is a versioned C1Q search-route candidate using that seed, followed by full Function/Limit requalification. If it does not, broader likelihood/profile geometry must be characterized before estimator redesign.
