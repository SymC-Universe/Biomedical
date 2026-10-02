# Bio Chi C-Interior Function Map APQ Objection Ledger v0.1

**Plan under review:** \`BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_PACKET_v0.1.md\` at commit \`673bbd477d87819165a0740426ee5619f0b30575\`  
**APQ level:** APQ-2 SUBSTANTIAL  
**Review limitation:** both first passes are role-isolated passes from one cognition, not independent reviewers. Evidence routes differ: Pass A is anchored in P0-N/domain literature and scientific meaning; Pass B is anchored in repository code, computation, and reproducibility.

| ID | Source | Severity | Affected premise | Failure mechanism | Disposition | Resulting change |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Pass A | MATERIAL | Successful C-map recovery is informative | Same-family simulation and fitting can look like validation by construction | DEFERRED_CLAIM_LIMITED | Explicitly classify the map as correct-specification estimator recovery/self-consistency only; no biological or external validation language |
| A2 | Pass A | MATERIAL | C1Q failure can be interpreted from C1Q alone | Shared parameterization may hide whether information is absent or C1Q specifically failed | ACCEPTED_TEST_ADDED | Add a generic positive-lag second-order recurrence pole diagnostic using a distinct parameterization |
| A3 | Pass A | MINOR | Synthetic envelope is "representative" | Synthetic design density can be confused with biological prevalence | ACCEPTED_MODIFIED | Rename to representative **qualification-envelope** coverage; prohibit biological prevalence language |
| B1 | Pass B | MATERIAL | Recovery error is scientific rather than optimizer-bound behavior | Raw parameter-box proximity can mimic identifiability failure | ACCEPTED_MODIFIED | Record raw-parameter bound distance, converged-start count, and transformed boundary distances for every C1Q fit |
| B2 | Pass B | MATERIAL | Fine/coarse drift measures pure sampling invariance | Same-duration decimation changes sample count/information density | ACCEPTED_MODIFIED | Reclassify as practical same-path rate sensitivity; exact mathematical invariance remains a separate known-truth contract |
| B3 | Pass B | MATERIAL | Three seeds can characterize failure frequency | n=3 only supports descriptive finite-sample dispersion | ACCEPTED_MODIFIED | Report row-level results, range and median only; forbid prevalence, stable failure-rate, or inferential-probability language |
| B4 | Pass B | MINOR | Seeded simulation implies exact reproducibility | Runtime/library/platform can change floating-point or optimization details | ACCEPTED_MODIFIED | Declare numerical repeatability class and record Python/NumPy/SciPy versions plus RNG/seed rule |

## Evidence-mediated resolution

### A1

Known-truth recovery within the same mathematical family is inherently a qualification/self-consistency question. The plan is useful because the current unresolved issue is *where the candidate works and fails under its intended truth family*, not whether biology follows C. The claim ceiling is narrowed accordingly. No new experiment is needed to resolve this objection.

### A2

The positive-lag covariance of a valid second-order C truth obeys the generic recurrence
\[
\gamma_{k+2}=a\gamma_{k+1}-b\gamma_k.
\]
A generic least-squares recurrence fit provides a non-C1Q route to the pole pair. Where \(b>0\) and \(|a/(2\sqrt b)|<1\),
\[
\rho=\sqrt b,\qquad
\theta=\arccos\!\left(\frac{a}{2\rho}\right),
\]
and the continuous pole coordinate follows from
\[
L=-\ln\rho,\qquad
\chi=\frac{L}{\sqrt{L^2+\theta^2}}.
\]
This diagnostic shares the underlying second-order truth assumption but not C1Q's state-space likelihood, nuisance parameterization, or optimizer. It is therefore suitable as an attribution diagnostic, not an independent biological validation.

### B1

The C1Q production candidate already exposes raw optimized parameters, attempted starts, converged starts, and transformed parameters. The revised map records those quantities directly. No arbitrary "near bound" threshold is introduced.

### B2

The fine/coarse pair remains valuable because it is the same realized path under exact decimation. The interpretation is narrowed to *practical rate sensitivity of the estimator under same-duration data*, while exact \(\chi/g\) invariance remains established analytically in the lineage contracts.

### B3

The seed count is retained for bounded resource use. The map is descriptive P0-D coverage, not an estimate of biological prevalence or a stable failure probability. Any later threshold or probabilistic claim requires a separate qualification design.

### B4

The revised plan promises numerically equivalent / decision-stable reproducibility within the declared software environment, not universal bitwise identity. The workflow records package/runtime versions and exact seeds.

## Unresolved objections

**BLOCKER:** none.  
**MATERIAL:** none after claim limitation and plan revision.  
**MINOR:** no minor objection blocks execution.

## Shared-premise challenge

Both reviews share the premise that continuous-time C is worth mapping. That premise comes from the already-completed P0-N/A0 residual, not from reviewer agreement. A common failure would be that the project mistakes successful correct-specification recovery for evidence that C is biologically common. The revised plan prevents that inference explicitly.

Both reviews also share the current one-mode second-order theory. The added generic recurrence diagnostic does not escape the second-order assumption, so the map still cannot test whether biology belongs to the family. That limitation remains explicit and is intentionally deferred to later biological candidate testing.

## APQ closure recommendation

APQ may close for this P0-D plan after the complete revised Plan Packet v0.2 and Plan Delta are preserved. A second adversarial pass is not required because this is a bounded known-truth P0-D map, not a P1 or high-risk APQ-2 plan, and all MATERIAL objections are resolved by narrowing or pre-execution controls.
