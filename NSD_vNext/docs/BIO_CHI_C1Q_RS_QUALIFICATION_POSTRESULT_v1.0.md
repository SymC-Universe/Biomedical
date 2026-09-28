# Bio Chi C1Q-RS Function / Limit Qualification Postresult v1.0

**Status:** COMPLETE / P0-Q SEARCH-ROUTE REPAIR SUPPORTED  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Qualified plan:** \`NSD_vNext/docs/BIO_CHI_C1Q_RS_QUALIFICATION_PLAN_v0.2.md\`  
**Freeze:** \`NSD_vNext/docs/BIO_CHI_C1Q_RS_QUALIFICATION_FREEZE_v1.1.md\`

## Provenance

Mechanical contracts:
- workflow: \`NSD C1Q-RS Mechanical Contracts\`
- successful run: \`36370664574\`

Function Map repair:
- workflow: \`NSD C1Q-RS Function Map Qualification\`
- run: \`36370858905\`
- complete artifact: \`10948774993\`
- digest: \`sha256:b9d81fc6858fd8727f57d22abf64e71182f74bf8c57b929437fb8f1cacc8eda1\`

Limit requalification:
- workflow: \`NSD C1Q-RS Limit Requalification\`
- run: \`36370858924\`
- complete artifact: \`10949515451\`
- digest: \`sha256:49eeb01f7e04b8d4190416c13a5db721ceddbc6283750748af07f2bfa53fc233\`

The source Function Map remained run \`36368579380\`, artifact \`10948327278\`, digest \`sha256:cb4ceade9271c80a5b002f0b9f6ba791ae3e0ae049b64ede0a3fdb0aee2b5a0c\`.

## Function Map result

C1Q-RS satisfied the strict non-worsening invariant in **96/96** rate-level rows.

The recurrence/covariance seed was admissible in 88/96 rows and supplied the winning basin in 34/96. Material likelihood improvement relative to the archived C1Q fit occurred in 26/96 rows under the frozen numerical comparison tolerance. The overall likelihood-improvement distribution was strongly right-skewed:

- median: approximately \(2.9\times10^{-11}\), effectively unchanged over the ordinary rows;
- maximum improvement: approximately \(124.727\) NLL units;
- minimum numerical difference: approximately \(-3.11\times10^{-4}\) NLL, within the bounded numerical behavior of the comparison and not a scientific degradation.

The repair therefore leaves already-good rows essentially unchanged while correcting a concentrated subset of severe basin failures.

### Local-\(\chi\) recovery

Across all 96 rows:

- archived C1Q median absolute \(\chi\) error: approximately **0.03547**;
- C1Q-RS median absolute \(\chi\) error: approximately **0.03038**;
- archived maximum absolute \(\chi\) error: approximately **0.68271**;
- C1Q-RS maximum absolute \(\chi\) error: approximately **0.68271**.

The unchanged maximum is scientifically important. The repair is substantial but not universal.

Descriptive post-result counts, which are **not thresholds**, show the shape of the improvement:

- rows with \(|\Delta\chi|>0.1\): 30 before, 11 after;
- rows with \(|\Delta\chi|>0.3\): 20 before, 4 after;
- rows with \(|\Delta\chi|>0.5\): 8 before, 1 after.

Fine-rate median absolute \(\chi\) error improved from approximately 0.02210 to 0.01860. Coarse-rate median improved more strongly, from approximately 0.06749 to 0.03722.

### \(g\) recovery

Across all rows:

- archived C1Q median absolute \(g\) error: approximately **0.13441**;
- C1Q-RS median absolute \(g\) error: approximately **0.11996**.

Descriptive, non-threshold counts:

- rows with \(|\Delta g|>0.2\): 37 before, 28 after;
- rows with \(|\Delta g|>0.5\): 27 before, 14 after;
- rows with \(|\Delta g|>1.0\): 20 before, 8 after.

Thus the search repair improves \(g\) recovery but does not eliminate practical \(g\)-identification failures.

### Cell structure

The strongest repairs occur in the cells that drove the original boundary-collapse finding.

Cell 15, previously pathological at both rates and all three seeds, changed from median absolute \(\chi\) error about 0.559 to about 0.051 and median absolute \(g\) error about 1.432 to about 0.200. Median NLL improvement was about 69.93.

Cell 0 improved from median absolute \(\chi\) error about 0.281 to about 0.048 and median \(g\) error about 0.617 to about 0.140.

Cell 5 improved from median \(\chi\) error about 0.206 to about 0.061 and median \(g\) error about 0.911 to about 0.039.

Cell 9 improved from median \(\chi\) error about 0.186 to about 0.025, while \(g\) recovery changed little.

Cell 7 remains an important residual limitation. Its median absolute \(\chi\) error improved from about 0.273 to 0.152, but median absolute \(g\) error remained approximately 1.237. Several cell-7 rows move to a lower-likelihood basin while still landing at \(g\approx+1\), demonstrating that better optimization does not guarantee accurate nuisance-coordinate recovery.

Other residual severe rows include cell 8 seed 104729 coarse and cell 5 seed 417923 coarse, where the recurrence route refused or did not replace the legacy boundary solution.

## Recurrence information versus generic extra compute

The APQ-required compute-matched control optimized the next-ranked legacy start on all 48 previously identified boundary-collapse rows.

It did **not** reproduce the repair:

- the next-ranked extra legacy start materially beat the archived solution in **0/48** rows;
- C1Q-RS was materially better than the best archived-plus-extra-legacy solution in **26/48** rows;
- the remaining 22 rows were effectively ties.

Thus the improvement is attributable to information carried by the recurrence/covariance start, not merely to one additional optimizer call.

## Numerical boundary behavior

C1Q-RS reduces but does not eliminate boundary attraction.

Across the 96 selected C1Q-RS fits:

- three selected raw solutions remain on an exact numerical raw boundary;
- fifteen selected fits remain within \(10^{-6}\) of the C \(g\)-boundary.

These counts are descriptive diagnostics, not admission thresholds.

## Limit Map requalification

The search repair did **not** erase the previously established semantic limits.

### Nested one-mode control

For both isotropic \(g=0\) seeds, A1 remains the extended BIC winner. C1Q-RS does not create a new overfitting preference against the nested simpler family.

### Genuine separated two-mode control

For both genuine separated two-mode seeds, A2 remains the extended BIC winner, with margins of approximately 62.60 and 33.17 over the next candidate. C1Q-RS therefore does not absorb the frozen genuine multimodal control.

### Anisotropic and rank-1 white forcing

The one-mode nuisance-capable C family remains favored over A2 in these forcing-shape controls, consistent with the previous conclusion that A2 false multimodality can arise from omitted forcing geometry.

### Colored-process extra pole

The colored-process control remains a semantic failure. C1Q/C1Q-RS still fit it extremely well, and the extended winner is C1Q-RS for one seed and C1Q for the other. The numerical difference between C1Q and C1Q-RS is negligible.

Therefore:

\[
\mathrm{better\ C1Q\ optimization}
\not\Rightarrow
\mathrm{second\!-\!order\ lineage}.
\]

### D\C and S\D family boundaries

D\C and S\D truths remain out of C by construction even when the constrained C candidate fits them well. C1Q-RS is effectively identical to C1Q on most rows; tiny NLL improvements occur on negative D\C controls while the fitted \(g\) remains at the C boundary.

Therefore:

\[
\mathrm{C1Q\!-\!RS\ fit\ quality}
\not\Rightarrow
\mathrm{truth}\in C.
\]

### Paired-sampling semantics

The paired C, D\C, and S\D sampling results are essentially unchanged by C1Q-RS. Practical cross-rate stability remains informative but is not a C-membership test.

## Post-execution deviation audit

The frozen scientific plan was followed.

- shared-helper and strict-containment contracts were run before scientific interpretation;
- the initial contract workflow failed only because \`pytest\` was absent and was repaired without changing science;
- all 96 Function Map rows were retained;
- all mandatory Limit classes were retained;
- no unfavorable row was excluded;
- the compute-matched extra-start control was executed;
- no scientific threshold was introduced;
- truth-family labels were not changed by fit quality;
- production A0/A1/A2 were not modified.

The only execution-level correction was installation of the missing test dependency in the contract workflow. That failure and repair are recorded separately in \`WORKING_INVESTIGATION.md\`.

## Scientific disposition

**C1Q-RS search repair:** SUPPORTED as a P0-Q search-route improvement.

**C1Q-RS as a fully qualified local-\(\chi\) estimator:** NOT ESTABLISHED.

**C1Q-RS as evidence of C-family membership:** REFUSED.

**Continuous-lineage C mathematics:** NOT FALSIFIED.

**Real-EEG local \(\chi\):** UNLICENSED.

**Scientific threshold:** NONE.

**Biological prevalence:** NOT ESTIMATED.

The correct conclusion is that one important estimator-search defect has been repaired while the independent semantic admission problem remains open.

## Next scientific requirement

Because C1Q-RS was engineered using already-viewed Function/Limit outcomes, its search improvement must next face a prospectively frozen **untouched known-truth qualification envelope** before it becomes the canonical qualification search implementation.

That untouched qualification should use:

- new C-interior coordinates not used to design C1Q-RS;
- new realization seeds;
- the unchanged C1Q and C1Q-RS implementations;
- the strict non-worsening invariant;
- full parameter-recovery distributions;
- no outcome-derived threshold.

The previously established semantic Limit Map does not need to be relabeled or rediscovered by that interior holdout. It remains a separate admission barrier.
