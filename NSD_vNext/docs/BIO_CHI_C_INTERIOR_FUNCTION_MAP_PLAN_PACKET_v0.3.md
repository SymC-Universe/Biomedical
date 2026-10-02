# Bio Chi C-Interior Function Map Plan Packet v0.2

**Status:** APQ-2 REVISED AFTER RUNTIME RECHECK  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0, Section 15.4  
**Purpose tag:** \`FUNCTION_MAPPING\`  
**Parent P0-N:** \`NSD_vNext/docs/BIO_CHI_P0N_PRIOR_ART_CONGLOMERATION_v1.0.md\`  
**Parent A0:** \`NSD_vNext/docs/BIO_CHI_A0_PRIOR_ART_CONGLOMERATION_ATLAS_v1.0.md\`  
**Evidence intake:** \`NSD_vNext/docs/BIO_CHI_EVIDENCE_INTAKE_v1.0.md\`  
**Compliance:** \`NSD_vNext/docs/BIO_CHI_COMPLIANCE_STATUS_v1.0.md\`  
**APQ ledger:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_APQ_LEDGER_v0.1.md\`  
**Plan Delta:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_DELTA_v0.1.md\`

## Scientific target

### Native scientific question

Across the intended one-mode continuous-time C family, where does the current qualification-only C1Q representation recover the true local pole coordinate coherently, where does recovery degrade, and how stable is that recovery under exact fine-to-coarse sampling of the same realized path?

### Residual novelty

P0-N/A0 classifies the residual as \`NEW_INTEGRATION\` with \`NEW_BOUNDARY_TEST\` secondary. The damping ratio, biological oscillation analysis, state-space/OU inference, identifiability, sampling aliasing, model-order methods, and projection memory are prior art.

### Smallest live claim

Continuous-time family C is mathematically coherent as a prospective local-\(\chi\) representation. The finite-sample operating region of C1Q has not yet been mapped across a representative **qualification envelope**. This plan maps correct-specification estimator behavior only. It cannot establish that C is biologically common, validate the C family externally, promote C1Q, or license real EEG.

### Working hypothesis and material alternatives

**Exploratory working hypothesis:** C1Q recovery of local \(\chi\) and \(g\) will be coherent over substantial portions of the frozen interior envelope, with degradations traceable to finite-sample information, conditioning, sampling density, or optimization rather than arbitrary failure throughout the interior.

Alternatives:

1. recovery is broadly unstable across ordinary interior cells;
2. recovery is strongly asymmetric in \(g\), \(\chi\), latent fraction, or frequency;
3. practical fine/coarse estimates drift materially despite exact theoretical lineage invariance;
4. C1Q-specific optimization/parameterization fails where a generic second-order pole diagnostic still recovers the truth;
5. both diagnostics fail in the same regions, indicating weak finite-sample pole information rather than C1Q-specific failure;
6. the qualification envelope is too narrow or artificial to support a useful estimator Function Map.

### Evidence class and claim ceiling

P0-D exploratory known-truth mapping. Same-family recovery is reported as self-consistency / estimator qualification under correct specification, not independent validation.

## Inputs and provenance

- exact continuous-time C simulator already versioned in the NSD qualification code;
- C1Q implementation \`NSD_vNext/engine/nsd_engine/continuous_lineage_candidate.py\`;
- generic positive-lag covariance-recurrence pole diagnostic added only as an attribution comparator;
- earlier A0/A1/A2 qualification results retained as prior Limit/qualification evidence; no new A0/A1/A2 refit is required by this Function Map;
- existing C/D/S, closure, colored-process, alias, and family-boundary results retained as the companion Limit Map;
- real EEG excluded.

Synthetic input status: \`INTAKE_PASS\`. Literature/A0 status: \`INTAKE_PASS_WITH_LIMITS\`. Compliance: \`NOT_APPLICABLE\`.

Earlier reference outcomes at 10 Hz, \(\chi=0.30\), \(A=0.8\), \(g=0,\pm0.75\) are already viewed. The new Sobol coordinates avoid those exact reference cells and remain P0-D, not confirmation.

## Native model and validity regime

The known truth is the underdamped continuous-time linear stochastic C oscillator

\[
K=
\begin{bmatrix}
-\alpha & -1\\
\nu^2 & -\alpha
\end{bmatrix},
\qquad
\chi=\frac{\alpha}{\sqrt{\alpha^2+\nu^2}},
\qquad
g=\frac{G}{A\alpha},
\]

with \(|g|<1\). Exact discretization uses

\[
F=e^{K\Delta t},
\qquad
Q_d=P-FPF^\top.
\]

The plan requires one true C mode, declared scalar observation, white observation noise, alias-safe factor-2 decimation, and numerically valid C1Q execution. Colored/higher-order forcing, D\C or S\D laws, projection memory, alias collision, near-critical singular behavior, genuine multimodality, and biological nonlinear/nonstationary regimes remain Limit Map cases outside this Function Map claim.

## Frozen qualification envelope

The 16 coordinates are generated once from SciPy Sobol dimension 4, \`scramble=True\`, seed \`20260927\`, then frozen explicitly below. The Sobol generation recipe is provenance only; the listed coordinates are the actual design identity.

Ranges:

- \(A\in[0.20,0.90]\);
- natural frequency \(f_n\in[3,25]\) Hz;
- true \(\chi=\zeta\in[0.15,0.85]\);
- \(g\in[-0.80,0.80]\).

| Cell | A | f_n Hz | chi | g |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.371004707 | 9.892272022 | 0.504089061 | -0.034300108 |
| 1 | 0.658443794 | 15.100740636 | 0.482040667 | 0.044371614 |
| 2 | 0.892343308 | 4.476334769 | 0.778687826 | -0.570623136 |
| 3 | 0.473630218 | 20.687577935 | 0.231985860 | 0.557254179 |
| 4 | 0.432551656 | 6.878767651 | 0.364377508 | 0.760427584 |
| 5 | 0.758293355 | 23.785478780 | 0.648926574 | -0.773792034 |
| 6 | 0.612110780 | 12.301666114 | 0.267449703 | 0.247541299 |
| 7 | 0.242637803 | 18.189667420 | 0.726651006 | -0.237471201 |
| 8 | 0.261257801 | 3.293630781 | 0.308216329 | -0.634738243 |
| 9 | 0.591763440 | 22.214669872 | 0.679922958 | 0.649498792 |
| 10 | 0.784792872 | 8.710853929 | 0.405086727 | -0.373406155 |
| 11 | 0.410513189 | 16.623925384 | 0.602130437 | 0.361601254 |
| 12 | 0.544221032 | 13.869666623 | 0.824758969 | 0.158424690 |
| 13 | 0.825529283 | 16.967463199 | 0.190551668 | -0.170228185 |
| 14 | 0.720473163 | 8.447991112 | 0.550089446 | 0.446320035 |
| 15 | 0.307933592 | 22.559304427 | 0.440546398 | -0.431563991 |

Realization seeds: \`104729\`, \`208457\`, \`417923\`.

Sampling:

- fine \(f_s=256\) Hz;
- same-path exact factor-2 decimation to 128 Hz;
- duration 60 s;
- each fine/coarse pair is one metamorphic unit.

The synthetic design is representative only of this frozen **qualification envelope**, not of biological prevalence.

## Planned execution

1. **Mechanical preflight:** cells 0, 5, 10, 15 with seed \`104729\`. The preflight can stop only for implementation/runtime defects, invalid covariance, alias violation, schema failure, or artifact/reproducibility failure. Scientific recovery magnitude cannot retune the design.
2. **Full Function Map:** 16 cells x 3 seeds.
3. Fit C1Q independently at 256 and 128 Hz.
4. Compute a generic second-order covariance-recurrence pole diagnostic independently of C1Q's state-space likelihood/optimizer. Fit the recurrence on positive-lag sample covariance, then derive \(\rho,\theta,\chi\) only when the fitted recurrence represents an underdamped stable pair. Otherwise emit refusal.
5. Do not rerun the expensive legacy A0/A1/A2 comparison in this Function Map. Its prior C1Q/A1/A2 qualification role is already documented in the existing postresults; the present map makes no new comparative-performance claim against A0/A1/A2.
6. Preserve row-level diagnostics:
   - truth coordinates;
   - C1Q fitted coordinates and signed/absolute errors;
   - generic recurrence pole/\(\chi\) estimate or refusal;
   - C1Q/generic disagreement;
   - attempted/converged starts;
   - raw optimized parameters;
   - maximum absolute raw coordinate and distance to the \([-8,8]\) box;
   - \(1-|g|\) and other relevant transformed boundary distances;
   - NLL/BIC;
   - same-path fine/coarse fitted-\(\chi\) and \(g\) drift;
7. Summaries report full row distributions, per-cell ranges, and medians. No best-case representative is substituted.
8. Preserve every finite fit, nonconvergence, refusal, and rescue.
9. Freeze no empirical admission threshold from these data.

## Optimization and numerical failure handling

If no finite valid C1Q solution exists, preserve \`OPTIMIZATION_UNRESOLVED\`. If a solution is finite but the optimizer reports nonconvergence, preserve both the fit and status. A predeclared mechanical rescue may rerun the same cell with \`optimizer_maxiter=160\` and \`max_optimized_starts=24\`; original and rescue outputs both remain.

The generic recurrence diagnostic refuses when the fitted coefficients do not yield a stable underdamped pair or the covariance system is numerically rank-deficient for that estimate.

## Uncertainty and statistical meaning

Three realization seeds provide descriptive finite-sample dispersion only. No confidence interval, failure probability, prevalence estimate, or inferential threshold is derived from \(n=3\). If seed dispersion changes the qualitative interpretation, the correct result is \`NEED_MORE_INFORMATION\` and a later uncertainty-focused qualification plan.

Same-path fine/coarse drift is interpreted as **practical estimator rate sensitivity under fixed duration**, not as the exact mathematical sampling-invariance theorem and not as two independent observations.

## Reproducibility class

- RNG: NumPy default generator with explicit integer seed per realization.
- Design identity: explicit frozen coordinate table above.
- Expected repeatability: numerical/decision-equivalent repeatability within the declared Python/NumPy/SciPy environment; cross-platform bitwise identity is not promised.
- Workflow artifact records Python, NumPy, and SciPy versions and the Git commit.
- The rerun check compares row count, design identity, status labels, and numerical outputs within a declared floating-point tolerance; no scientific threshold is introduced by the reproducibility tolerance.

## Compliance and design adequacy

Section 0.7: \`NOT_APPLICABLE\` for synthetic computation.  
Section 19.2: \`NOT_APPLICABLE\` because this is P0-D known-truth Function Mapping.

## Outcome architecture

**Supports continued C1Q qualification:** C1Q broadly recovers the truth across the qualification envelope and discrepancies are interpretable with the generic diagnostic, finite-sample variation, parameter information, or optimization diagnostics.

**Narrows the operating claim:** coherent recovery is restricted to identifiable subregions or depends materially on parameter direction/sign.

**C1Q-specific failure:** generic recurrence recovery remains coherent where C1Q repeatedly fails or distorts the pole.

**Information-limited region:** C1Q and the generic diagnostic both degrade on the same cells/realizations.

**Falsifies C1Q as broadly useful in the intended interior:** material C1Q failure is widespread across ordinary interior cells and cannot be assigned to explicit information/optimization limitations.

**Refusal:** truth construction/alias assumptions fail, or an estimator cannot provide a scientifically interpretable underdamped mode.

**Need more information:** seed/optimization variability prevents a stable interpretation.

**Null/indeterminate:** no interpretable relation between qualification-envelope location and recovery emerges.

No outcome promotes the C family as biology.

## Dependency structure

Foundational dependencies are exact truth construction, correct C1Q implementation, exact same-path decimation, and valid frozen coordinates. A mechanical failure in those dependencies stops execution for repair. Scientific recovery failure does not authorize retuning.

The biological branch remains independent: a successful synthetic Function Map still requires separate biological carrier/model qualification before any local biological \(\chi\) claim.

## APQ closure state

Two role-isolated first passes were completed. They are not independent cognitions. All MATERIAL objections are resolved by claim limitation, an added generic recurrence diagnostic, explicit numerical diagnostics, and corrected interpretation of same-path rate sensitivity. No BLOCKER remains.

A shared-premise challenge identified the risk that all reviews inherit the one-mode C assumption. The plan explicitly limits itself to correct-specification Function Mapping and cannot establish that biology belongs to C.

This bounded P0-D APQ-2 plan is eligible for freeze after the objection ledger and Plan Delta are committed. No decisive Function Map outcome has been exposed.


## v0.3 runtime revision

The locally executed frozen preflight exposed a mechanical scalability problem before any Function Map scientific result was produced. Truth construction, C1Q, and the generic recurrence diagnostic progressed, while a single descriptive legacy A0/A1/A2 comparison did not complete within a five-minute local timing attempt. Because that comparator is not a foundational dependency of the current Function Map question and its comparative role was already exercised in prior qualification work, v0.3 removes **new A0/A1/A2 refitting** from the preflight and full map.

This revision does not change the 16-cell envelope, seeds, duration, sampling, C1Q implementation, generic recurrence comparator, outputs that bear on the Function Map question, claim ceiling, refusal logic, or no-threshold rule. It changes only the nonessential expensive legacy-comparator execution dependency.

The revision was made before any new Function Map scientific outcome was produced and is therefore not outcome-directed.
