# Bio Chi Working Scientific State

**Status:** ACTIVE LIVING SCIENTIFIC RECORD  
**Date established:** 27 September 2026  
**Program authority:** SymC General Operations Manual v0.8.6  
**Working repository:** \`SymC-Universe/Biomedical\`  
**Working branch:** \`nsd-rebuild-gom-v0.8.0\`  
**Last science head reconciled before creation of this file:** \`c849f4e9dd80866a98afcc7a6ac526918a249961\`  
**Primary investigation:** Bio Chi  
**Current proving ground:** NSD / neural dynamics  
**Real-EEG local chi:** UNLICENSED  

This is the canonical human-readable working state for the Bio Chi investigation. It does not replace individual freezes, preflights, postresults, artifacts, or the reproducibility guide. It connects them into one continuously updated scientific narrative so that a reader can determine where the investigation came from, where it stands, what changed, why it changed, what is currently licensed, what is refused, and what experiment comes next.

This file is to be updated whenever there is a meaningful scientific update, a new exact mathematical boundary, an empirical threshold freeze or revision, a model-family decision, a promotion or refusal, a new failure/root-cause result, or a change in the next scientific experiment. Mechanical-only commits do not require narrative expansion unless they alter reproducibility or the interpretation of evidence.

## 0. Reader's Guide

The current investigation is **Bio Chi**, not a return to disorder-first NSD. NSD is being used because it provides a difficult biological dynamical system in which a local scalar can fail for many legitimate reasons. A rule that only works for EEG remains an NSD-specific rule. A rule that survives native-model, identifiability, sampling, closure, refusal, and cross-domain checks becomes a candidate Bio Chi rule.

The current hierarchy is:

1. **N-B1, local scalar:** when a native biological mode can legitimately carry local \`chi\`.
2. **N-B2, modal/vector architecture:** how qualified modes, subspaces, participation, coupling, spatial structure, and uncertainty organize. This is the neural instance of capital \`Chi\`.
3. **N-B3, conglomerate/system behavior:** how coupling, topology, non-normality, perturbation, transient amplification, recovery, context, and history determine the realized system response.

N-B1 is the current bottleneck. N-B2 and N-B3 remain scientifically active but must not be collapsed into the local scalar.

## 1. Where the Investigation Came From

### 1.1 Historical NSD correction

The recovered 2025 NSD manuscript is treated as an architecture-first P0-D document, not as empirical validation. Historical disorder coordinates, thresholds, trajectories, and whole-system displays do not enter the forward program unless their data lineage, estimator, independence structure, uncertainty, and current GOM classification are rebuilt.

This correction matters because Bio Chi is not being constructed by defending historical NSD scalar values. The investigation restarted from native neurophysiology, known truth, and refusal.

Canonical source:
\`NSD_vNext/docs/CONTINUITY_STATE_v0.1.md\`

### 1.2 Transfer of Bio Chi into NSD

On 25 September 2026 the active Bio Chi investigation was transferred from the GRI/cancer extension lane into NSD.

What transferred:
- architecture;
- native-model-first rules;
- scalar refusal discipline;
- the distinction between local scalar, modal/vector architecture, and conglomerate behavior;
- cross-project methodological lessons.

What did not transfer as NSD evidence:
- TCGA/GRI results;
- Shaffer melanoma results;
- cancer scalar or modal values;
- tumor-normal results;
- prostate external validation.

Completed GRI/BioSystems remains closed for this phase. Cancer/Shaffer remains parked.

Canonical source:
\`NSD_vNext/docs/BIO_CHI_TRANSFER_TO_NSD_20260925.md\`

### 1.3 First central correction

A biological scalar is optional.

A local scalar may be called \`chi\` only where a native dynamical model licenses it. A descriptive peak, spectral width, covariance summary, session similarity, state ordering, or aperiodic exponent is not promoted into chi by analogy.

For the classical second-order oscillator

\[
q''+2\zeta\omega_n q'+\omega_n^2q=0,
\]

the SymC local coordinate equals the damping ratio only when the denominator uses the **natural angular frequency**:

\[
\chi=\frac{\gamma}{2\omega_n}=\zeta.
\]

Using the damped frequency instead gives a different quantity and is not the licensed local chi.

There is no assumed universal neural \`chi=1\` empirical boundary. \`chi=1\` is the exact critical-damping boundary of the licensed second-order pole-pair model, not a universal healthy/pathological neural cutoff.

## 2. Current Mathematical Architecture

### 2.1 Regular all-regime recurrence

The positive-lag second-order covariance recurrence is

\[
\gamma_{k+2}=a\gamma_{k+1}-b\gamma_k,
\]

with

\[
\rho=\sqrt b,
\qquad
\xi=\frac{a}{2\rho},
\qquad
L=-\ln\rho.
\]

The regular covariance form is

\[
\gamma_k
=
\rho^k
\left[
A T_k(\xi)+H U_{k-1}(\xi)
\right].
\]

The regular transition is

\[
F_{\rm reg}
=
\rho
\begin{bmatrix}
\xi&-1\\
1-\xi^2&\xi
\end{bmatrix}.
\]

Regimes:
- \(|\xi|<1\): underdamped;
- \(\xi=1\): critical;
- stable positive-real overdamped: \(1<\xi<\cosh L\).

### 2.2 Structural rank boundary

The positive-lag Hankel determinant is

\[
\Delta_H
=
\rho^4
\left[
A^2(\xi^2-1)-H^2
\right].
\]

The parameter Jacobian determinant is

\[
\det J=-4\rho^5\Delta_H.
\]

Therefore generic finite-\(H\) critical points are structurally identifiable. The true local rank-drop surface is

\[
\Delta_H=0,
\]

not the entire critical surface.

### 2.3 C, D, and S family hierarchy

Three one-mode scopes are kept distinct.

**C, continuous-time embeddable lineage.** This is the prospective biological N-B1 target.

With continuous nuisance amplitude \(G\), decay rate \(\alpha=L/T_s\), and

\[
g=\frac{G}{A\alpha},
\]

same-branch continuous embeddability is

\[
|g|\le1.
\]

**D, discrete exact white-Q image.** This is a sample-rate-specific state-space control layer.

\[
0\le A\le1,
\qquad
|H|\le A\sinh L.
\]

Define

\[
h=\frac{H}{A\sinh L}.
\]

Then D is \(|h|\le1\).

**S, scalar-positive observable family.** This is the broad covariance-validity layer defined by exact nonnegative residual spectral density.

At finite sampling interval,

\[
C\subsetneq D\subseteq S,
\]

with \(D\subsetneq S\) for \(A<1\), while \(D=S\) at \(A=1\).

These are **semantic/model-scope layers**. They are not ordinary same-dimensional alternatives that BIC can choose scientifically.

### 2.4 Local chi across all regimes

On a licensed continuous branch:

Underdamped, with \(\theta=\arccos\xi\),

\[
\chi
=
\frac{L}{\sqrt{L^2+\theta^2}}.
\]

Critical:

\[
\chi=1.
\]

Stable overdamped, with \(\psi=\operatorname{acosh}\xi<L\),

\[
\chi
=
\frac{L}{\sqrt{L^2-\psi^2}}.
\]

Near criticality,

\[
\chi-1
\sim
\frac{\xi-1}{L^2}.
\]

Therefore near-critical conditioning must be treated relative to \(L^2\), not by a raw \(\xi-1\) distance alone.

## 3. Sampling and Lineage Results

Exact integer decimation by factor \(m\) obeys

\[
A_m=A,
\qquad
\rho_m=\rho^m,
\qquad
\xi_m=T_m(\xi),
\qquad
H_m=H U_{m-1}(\xi).
\]

On an alias-safe continuous branch, both local chi and the continuous nuisance coordinate \(g\) are exact lineage invariants:

\[
\chi_m=\chi,
\qquad
g_m=g.
\]

The discrete coordinate \(h\) is not invariant:

\[
h_m
=
h
U_{m-1}(\xi)
\frac{\sinh L}{\sinh(mL)}.
\]

For nontrivial canonical coarsening, \(|h_m|<|h|\) when \(h\ne0\). Thus D compatibility systematically moves toward the interior under coarsening.

The Hankel determinant transports as

\[
\Delta_{H,m}
=
\rho^{4(m-1)}
U_{m-1}(\xi)^2
\Delta_H.
\]

For underdamped modes, \(U_{m-1}=0\) exactly when \(\sin(m\theta)=0\). A structurally identifiable fine oscillator can therefore collapse to rank one at coarse DC/Nyquist alias collision. Raw Hankel magnitude must not be used as a sample-rate-independent threshold.

A constructive result further showed that a fine-rate law may lie in \(S\setminus D\), decimate into D, and still remain outside C. Therefore:

\[
\text{coarse D membership}
\not\Rightarrow
\text{fine D membership}.
\]

Current paired C1Q fitting also showed that finite-sample parameter stability is not a sufficient C-membership test. Valid C truths can show fitted drift, while out-of-C truths can look stable across rates.

Canonical source:
\`NSD_vNext/docs/C1Q_PAIRED_SAMPLING_SEMANTICS_POSTRESULT_v0.1.md\`

## 4. Substrate Inheritance Contribution

Substrate Inheritance changed the admission question from "is a pole pair identifiable?" to "is the reduced local dynamical object sufficiently closed for the claim being made?"

For a \(P/Q\) split of a full generator,

\[
L=
\begin{bmatrix}
L_{PP}&L_{PQ}\\
L_{QP}&L_{QQ}
\end{bmatrix},
\]

the mechanisms are kept separate:

- \(L_{QP}\): P-to-Q leakage;
- \(L_{PQ}\): Q-to-P hidden-state input;
- return-memory/self-energy:

\[
\Sigma(z)
=
L_{PQ}
(zI-L_{QQ})^{-1}
L_{QP}.
\]

Eliminating Q gives

\[
p'(t)
=
L_{PP}p(t)
+
L_{PQ}e^{L_{QQ}t}q_0
+
\int_0^t
L_{PQ}e^{L_{QQ}(t-s)}L_{QP}p(s)\,ds.
\]

This yields a key Bio Chi correction:

**Raw leakage is not itself a universal refusal criterion.**

P may leak into Q while the resolved P trajectory remains exact if there is no return path. Hidden-state input and endogenous return memory are also different mechanisms and must not be collapsed into one closure score.

The same isolated local oscillator block, and therefore the same nominal local chi, can occupy different closure classes depending on its embedding.

Canonical sources:
- \`NSD_vNext/docs/SUBSTRATE_CLOSURE_QUALIFICATION_PREFLIGHT_v0.1.md\`
- \`NSD_vNext/docs/PREDICTIVE_APPROXIMATE_CLOSURE_POLICY_v0.1.md\`

## 5. Approved Closure Policy

The user approved **predictive approximate closure** rather than exact or near-exact Markovian isolation.

The N-B1 question is therefore claim-relative:

> Are unresolved substrate/interface dynamics small enough, under prospectively calibrated known-truth and held-out tests, that they do not materially alter the claimed local pole lineage, local chi, or held-out reduced-model prediction?

Measurable memory does not automatically refuse the mode. It becomes disqualifying when it materially changes the claimed local dynamics or breaks prospective predictive adequacy.

The exploratory closure map, workflow run \`36354816856\`, supports this policy.

At the frozen exploratory 10 Hz local mode with local chi \(=0.30\):

- closed controls had numerical-zero prediction, memory, pole displacement, and chi displacement;
- P-to-Q leakage-only controls retained effectively exact resolved prediction and unchanged chi despite nonzero leakage;
- Q-to-P hidden-input-only controls retained zero endogenous memory but hidden-state sensitivity increased with coupling;
- bidirectional return-memory produced increasing prediction error, memory, pole displacement, and chi displacement.

At coupling fractions 0.05, 0.10, and 0.20, bidirectional prediction RMS was approximately 0.198, 0.808, and 4.928, while chi displacement was approximately 0.00037, 0.00148, and 0.00592.

These coordinates are **map points, not thresholds**.

Canonical source:
\`NSD_vNext/docs/PREDICTIVE_CLOSURE_CALIBRATION_POSTRESULT_v0.1.md\`

## 6. Why Current A1 Is Insufficient

Current production A1 fixes the covariance-phase degree to \(H=0\), equivalent to the \(g=0\) subcase of the prospective continuous lineage.

Analytic spectral qualification showed that valid one-mode C truths with nonzero \(g\) can make A2 outperform A1 even though only one physical oscillator exists.

At 10 Hz, truth chi \(=0.30\), \(A=0.8\), \(n_{\rm eff}=7552\):

- \(g=-0.75\): expected BIC(A2)-BIC(A1) approximately -18.19;
- \(g=+0.75\): expected BIC(A2)-BIC(A1) approximately -15.24;
- \(g=0\): A1 contains the truth.

Finite 30 s paired-realization tests confirmed this pressure. Negative-\(g\) one-mode truths were repeatedly selected as A2 at both 256 and 128 Hz. Positive-\(g\) behavior was more realization-dependent.

Therefore:

\[
A2\text{ preference}
\not\Rightarrow
\text{two physical modes}.
\]

This result justified a qualification-only one-mode nuisance-capable candidate. It did **not** authorize a production estimator change.

Canonical sources:
- \`NSD_vNext/docs/CONTINUOUS_LINEAGE_SPECTRAL_ADEQUACY_POSTRESULT_v0.1.md\`
- \`NSD_vNext/docs/CONTINUOUS_LINEAGE_FINITE_PROBE_POSTRESULT_v0.1.md\`

## 7. C1Q Qualification State

C1Q is a qualification-only k=4 one-mode continuous-lineage candidate with coordinates:

- \(A\);
- \(\rho\);
- damped frequency \(f_d\);
- continuous nuisance \(g\), constrained to C.

At \(g=0\), C1Q nests current A1 observationally.

### 7.1 What C1Q passed

Run \`36354967663\`:

- every \(g=\pm0.75\) valid one-mode C cell preferred C1Q;
- every \(g=0\) cell retained simpler A1;
- fitted chi remained near the truth but showed finite-sample variation;
- one coarse positive-\(g\) fit reached practical \(g\)-boundary proximity.

Run \`36355157685\`:

- isotropic one-mode controls retained A1;
- genuine separated two-mode controls retained A2;
- anisotropic/rank-1 one-mode white-forcing controls moved from false A2 pressure to C1Q.

### 7.2 What C1Q failed

The same adversarial run showed C1Q winning both colored-process controls by about 44 to 45 BIC. The colored truth contains an additional real process pole.

Therefore:

\[
\mathrm{C1Q\ wins}
\not\Rightarrow
\mathrm{second\ order\ continuous\ lineage}.
\]

Family-boundary run \`36355282570\` then showed C1Q winning all eight \(D\setminus C\) and \(S\setminus D\) cells.

In positive \(D\setminus C\) controls, the true implied continuous \(g\approx1.0206\) was approximated with fitted C1Q \(g\approx0.87\) to \(0.91\).

Therefore:

\[
|\hat g|<1
\not\Rightarrow
\mathrm{truth\in C}.
\]

C1Q remains qualification-only.

Canonical sources:
- \`NSD_vNext/docs/CONTINUOUS_LINEAGE_C1Q_PREFLIGHT_v0.1.md\`
- \`NSD_vNext/docs/CONTINUOUS_LINEAGE_C1Q_POSTRESULT_v0.1.md\`
- \`NSD_vNext/docs/C1Q_ADVERSARIAL_CONTROLS_POSTRESULT_v0.1.md\`
- \`NSD_vNext/docs/C1Q_FAMILY_BOUNDARY_CONTROLS_POSTRESULT_v0.1.md\`

## 8. D1Q Scope-Control State

D1Q is a qualification-only k=4 one-mode control spanning discrete exact-image family D. It uses \(h\) rather than constraining the solution to continuous family C.

Successful workflow:
- workflow: \`NSD D1Q Scope Controls\`;
- run: \`36355795300\`;
- source head: \`c849f4e9dd80866a98afcc7a6ac526918a249961\`;
- artifact: \`nsd-d1q-scope-controls\`;
- artifact ID: \`10943632903\`;
- digest: \`sha256:281ebddad3fc8ed3f907c71cefbc81a78b4d77eb79c854f577e357bb46079247\`.

Contracts passed: 9/9.

Current finite-sample result:

- C-interior cells gave essentially identical C1Q and D1Q likelihoods, with D1Q implied \(g\) remaining inside C.
- Negative \(D\setminus C\) cells were correctly pushed outside C by D1Q, with implied \(g\approx-1.020\) and \(-1.032\), and small likelihood improvements over constrained C1Q.
- Positive \(D\setminus C\) cells were **not** reliably exposed. D1Q converged to implied \(g\approx0.87\) to \(0.91\), inside C, with effectively identical likelihood to C1Q.
- \(S\setminus D\) cells drove D1Q to the D boundary \(h\approx\pm1\). Implied continuous \(g\) was approximately \(-1.045\) for negative controls and \(+1.032\) to \(+1.033\) for positive controls. D1Q improved over C1Q, but cannot represent the true S-only law because D1Q itself is restricted to D.

Interpretation:

D1Q is useful as a scope/control model, especially for boundary pressure and some \(D\setminus C\) cases, but finite-sample D1Q point estimates are **not a complete C-membership test**. Positive \(D\setminus C\) remains a constructive false-inside example.

No C-vs-D empirical threshold is frozen.

Canonical design source:
\`NSD_vNext/docs/D1Q_DISCRETE_CONTROL_PREFLIGHT_v0.1.md\`

## 9. Structural-Order Refusal State

Exact mathematics separates genuine second-order covariance from a generic added third pole.

Second order obeys exactly:

\[
r_k
=
\gamma_{k+2}
-a\gamma_{k+1}
+b\gamma_k
=0,
\]

and a consecutive positive-lag \(3\times3\) Hankel matrix has rank at most two.

For an added distinct pole \(\phi\),

\[
\gamma_k
=
\gamma_k^{(2)}
+
C\phi^k,
\]

the second-order recurrence residual is generically nonzero:

\[
r_k
=
C\phi^k
(\phi^2-a\phi+b).
\]

The exact colored-process control is therefore structurally rank three even though C1Q can win BIC.

Canonical source:
\`NSD_vNext/docs/STRUCTURAL_ORDER_REFUSAL_PREFLIGHT_v0.1.md\`

### 9.1 Finite-sample calibration result

Successful workflow:
- workflow: \`NSD Structural-Order Calibration\`;
- run: \`36355795307\`;
- source head: \`c849f4e9dd80866a98afcc7a6ac526918a249961\`;
- artifact: \`nsd-structural-order-finite-sample\`;
- artifact ID: \`10944171633\`;
- digest: \`sha256:76091c306371c507f588c4fecda47f7d46c9e20ce15a3d144b3619c4bfad3a54\`.

Exact structural-order contracts passed: 9/9.

The finite-sample map used 20 seeds at 30 s, 120 s, and 300 s at fine 256 Hz and deterministic coarse 128 Hz.

Key finding:

**The current recurrence-residual and small Hankel singular-value diagnostics do not cleanly separate the colored-process truth from valid C/D/S one-mode truths at these durations.**

For example, at 300 s fine rate, median normalized recurrence residuals were approximately:

- C \(g=0\): 0.0241;
- C \(g=-0.75\): 0.0155;
- C \(g=+0.75\): 0.0191;
- \(D\setminus C\): 0.0183;
- \(S\setminus D\): 0.0115;
- colored \(\phi=0.7\): 0.0254.

These ranges overlap strongly.

Genuine separated two-mode truth shows a large recurrence failure after coarse decimation, with coarse median approximately 0.233 at 120 to 300 s, but at the fine rate its median is approximately 0.043 to 0.047 and overlaps the upper tail of one-mode controls.

Interpretation:

The exact structural-order theorem is valid, but a simple universal finite-sample recurrence or raw Hankel cutoff is not yet justified. Finite-sample structural refusal needs stronger uncertainty-aware or model-based machinery, likely combining recurrence order, innovation/residual behavior, explicit extra-pole alternatives, held-out prediction, and sampling semantics.

No structural-order threshold is frozen.

## 10. Current Decision and Boundary Ledger

| Item | Current status | Scientific meaning |
| --- | --- | --- |
| Bio Chi vs NSD focus | **Bio Chi primary** | NSD is the proving ground, not the final scope |
| N-B1 family target | **C selected prospectively** | Continuous-time modal lineage is the intended biological local-scalar family |
| Closure policy | **Predictive approximate closure approved** | Refusal depends on material effect on the local claim, not raw coupling alone |
| Real-EEG local chi | **REFUSED / UNLICENSED** | No current neural data result may be reported as licensed local chi |
| A1 | Production qualification baseline unchanged | Valid only for its narrower \(H=0/g=0\) family |
| A2 | Production qualification baseline unchanged | A2 preference is not proof of two physical modes |
| C1Q | Qualification-only | Corrects valid nonzero-\(g\) one-mode pressure but fails colored/family-scope refusals |
| D1Q | Qualification-only control | Helps expose D scope but cannot alone establish C membership |
| C boundary | Exact mathematical boundary \(|g|=1\) | Not an empirical fitted-value threshold |
| D boundary | Exact mathematical boundary \(|h|=1\) | Not a biological boundary |
| Structural rank | Exact \(\Delta_H=0\) | Exact order-loss boundary, not a finite-data cutoff |
| Critical chi | Exact \(\chi=1\) | Model critical damping, not universal neural pathology boundary |
| Alias collapse | Exact \(\sin(m\theta)=0\) | Sampling/refusal boundary |
| Predictive-closure tolerance | **NOT FROZEN** | Must be calibrated before real EEG |
| Structural-order finite-data threshold | **NOT FROZEN** | Current finite-sample diagnostics overlap |
| C-vs-D finite-data threshold | **NOT FROZEN** | C1Q/D1Q point estimates can misclassify scope |
| Paired-sampling drift cutoff | **NOT FROZEN** | Valid C can drift and out-of-C can appear stable |
| BIC promotion cutoff | **NONE** | BIC is model-comparison evidence, not family-semantic admission |
| Near-critical uncertainty cutoff | **NOT FROZEN** | Must account for \(1/L^2\) sensitivity |
| A2 collision threshold | **NOT FROZEN** | Exact collision is singular; finite separation needs qualification |

Any future numerical threshold must be added to this table on the commit that freezes it, including rationale, calibration source, direction of inequality, population/regime, and whether it is discovery, qualification, or confirmatory.

## 11. Current Empirical NSD Context

The descriptive healthy/reference lane remains separate from N-B1.

Eyes-open MFR-14 v0.2.1:
- COMPLETE;
- 14/14 mechanical pass;
- result: \`NOT_CONFIRMED_UNDER_FROZEN_MFR14_THRESHOLD\`;
- session1-3 minus session1-2 median \(+0.064685\), raw \(p=0.092285\), Holm \(p=0.184570\);
- session2-3 minus session1-2 median \(+0.028322\), raw \(p=0.179565\), Holm \(p=0.184570\).

This remains descriptive Function/Limit evidence. It does not license damping, local chi, capital Chi, or recovery.

The prior eyes-closed topology-audit failure remains an infrastructure/provenance issue and not a scientific outcome.

Historical ASD/disorder outcomes remain downstream and must not be opened as Bio Chi confirmation until the local/modal representation earns admission prospectively.

## 12. What Has Been Ruled Out

The investigation has now ruled out several shortcuts:

- descriptive spectral peak \(\rightarrow\) local chi;
- spectral width \(\rightarrow\) damping without broadening separation;
- covariance summary \(\rightarrow\) chi;
- A2 wins \(\rightarrow\) two physical modes;
- C1Q wins \(\rightarrow\) truth belongs to C;
- fitted \(|g|<1\) \(\rightarrow\) truth belongs to C;
- paired C1Q parameter stability \(\rightarrow\) truth belongs to C;
- finite fitted drift \(\rightarrow\) truth lies outside C;
- coarse D compatibility \(\rightarrow\) fine-rate D compatibility;
- raw leakage \(\rightarrow\) closure failure;
- exact structural-order theorem \(\rightarrow\) immediate finite-data structural threshold;
- local chi vector \(\rightarrow\) embedded system stability;
- eigenspectrum alone \(\rightarrow\) perturbation/recovery architecture.

These failures are retained as scientific progress, not hidden as dead ends.

## 13. What Currently Looks Strong

The strongest current Bio Chi architecture is:

\[
\text{native generator}
\rightarrow
\text{projection/interface/closure}
\rightarrow
\text{effective modal lineage}
\rightarrow
\Chi_{\rm bio}
\rightarrow
\text{licensed local }\chi
\rightarrow
\text{coupling/context/history}
\rightarrow
\text{realized system response}.
\]

The local scalar is not the inherited object. The dynamical lineage is the inherited object, and local chi is a coordinate of that lineage where licensed.

This is consistent with the mature Substrate Inheritance result that scalar agreement does not prove lineage and scalar disagreement does not destroy lineage.

## 14. Current Open Scientific Problems

### 14.1 Structural-order refusal in finite data

Exact order is understood. Finite-sample colored-process separation is not.

Needed:
- uncertainty-aware recurrence/order assessment;
- comparison with explicit extra-pole or colored alternatives;
- innovation/residual whiteness;
- held-out predictive consequences;
- alias-aware treatment;
- evaluation across duration and signal strength.

### 14.2 C versus D family membership

C1Q and D1Q point estimates are not sufficient.

Needed:
- uncertainty on \(g\), \(h\), and family-boundary distance;
- broader unconstrained one-mode diagnostics;
- paired sampling interpreted jointly with uncertainty;
- likelihood or predictive evidence that is not circularly conditioned on C.

### 14.3 Predictive approximate closure calibration

The policy is chosen, but the empirical tolerance is not.

Before real EEG, the program must freeze:
- prediction horizon or horizons;
- prediction error functional;
- hidden-state uncertainty representation;
- acceptable pole/chi displacement or uncertainty-relative criterion;
- held-out degradation rule;
- coverage/multiplicity policy;
- refusal behavior for nonidentifiability.

### 14.4 Near-critical uncertainty

Because \(d\chi/d\xi|_{\xi=1}=1/L^2\), the same \(\xi\) error has very different chi consequences depending on decay scale. Uncertainty must be propagated to chi before any critical-boundary claim.

### 14.5 A2 collision singularity

At coincident A2 pole pairs the scalar law collapses to a one-mode law and the latent split is unidentifiable. Ordinary BIC is nonregular in this region. A2 model count must not be interpreted naively near collision.

### 14.6 Holdout semantics

The current holdout is frozen-parameter **cold-start generalization after burn-in**, not the exact conditional likelihood of a contiguous second half given the terminal training filter state.

Future qualification must keep separate:
- contiguous predictive holdout with terminal-state carry-forward;
- fresh-segment generalization with prospectively qualified initialization/burn.

## 15. Immediate Forward Plan

The next work remains pre-real-EEG and qualification-only.

### Stage A: close finite-sample structural refusal

1. Preserve the exact second-order and added-pole theorems.
2. Use the completed duration map as calibration evidence, not as a threshold source.
3. Add explicit colored/extra-pole candidate or equivalent prediction test.
4. Compare recurrence/order evidence with held-out innovation whiteness and predictive degradation.
5. Determine whether a non-threshold refusal combination can be defined before considering numerical cutoffs.

**Why:** C1Q currently absorbs colored memory structure. Until this is controlled, a winning one-mode fit does not establish local lineage.

### Stage B: close C-versus-D scope

1. Continue D1Q as a control, not biological target.
2. Quantify uncertainty around implied \(g\) and \(h\).
3. Test boundary-near positive and negative \(D\setminus C\) truths across duration/signal strength.
4. Combine unconstrained D fit with paired-rate and predictive evidence.
5. Refuse family attribution when C versus D remains unresolved.

**Why:** finite-sample constrained C fits and unconstrained D fits can both return apparently inside-C point estimates for true out-of-C laws.

### Stage C: freeze predictive closure calibration

Only after the mechanism map and uncertainty behavior are sufficiently understood:

1. choose prediction horizon(s);
2. choose error functional(s);
3. define uncertainty-aware pole/chi preservation rule;
4. define held-out predictive degradation rule;
5. freeze coverage/multiplicity;
6. validate on untouched known truths;
7. record failure behavior.

**Why:** the user approved predictive approximate closure specifically to keep the biological investigation open without pretending biology is exactly isolated.

### Stage D: reconsider estimator promotion

Only after Stages A-C:

- assess whether C1Q, another observable-equivalence implementation, or refusal-only is scientifically justified for N-B1;
- do not promote merely because C1Q repaired false A2 selection;
- do not promote D1Q as the biological family.

This is the next user-level estimator/model-family decision point unless earlier qualification falsifies the route.

### Stage E: real EEG

Real EEG is opened for local chi only after:
- one-mode family scope is qualified;
- structural-order refusal is qualified;
- predictive closure is frozen;
- sampling/alias rules are frozen;
- uncertainty and near-critical rules are frozen;
- holdout semantics are prospectively specified.

Until then, real-EEG local chi remains refused.

## 16. N-B2 and N-B3 Forward Position

N-B2 does not wait for scalar success in principle. Modal/subspace structure can remain scientifically useful even where N-B1 refuses a scalar. Any empirical N-B2 work must retain mode identity, multiplicity, conditioning, spatial participation, and representation dependence.

N-B3 remains a separate system layer. Existing exact coupled-second-order fixtures already show:
- same local damping plus same eigenspectrum can have different transient gain and return behavior;
- same local damping can produce different embedded spectra under coupling;
- locally stable modes can become globally unstable.

Therefore N-B1 success will not collapse N-B3 into local chi.

## 17. Reproducibility Spine

The reviewer-facing reproduction path is maintained in:

\`NSD_vNext/docs/REPRODUCIBILITY_GUIDE_v0.1.md\`

Current relevant verification sections include:
- V12: white-process pole-identifiability predecision;
- V13: lineage, sampling, and substrate-closure contracts;
- V14: exploratory nonzero-g continuous-lineage probe;
- V15: predictive approximate-closure map;
- V16: nonzero-g spectral model-order pressure.

New scientific experiments must add or extend a V-numbered executable verification path before the package is called complete.

## 18. Canonical Source Map

Core continuity:
- \`BIO_CHI_TRANSFER_TO_NSD_20260925.md\`
- \`CONTINUITY_STATE_v0.1.md\`
- \`FUNCTION_LIMIT_MAP_v0.1.md\`
- \`REPRODUCIBILITY_GUIDE_v0.1.md\`

Core modal geometry:
- \`STATE_SPACE_WHITE_PROCESS_POLE_IDENTIFIABILITY_PREFLIGHT_v0.1.md\`
- \`STATE_SPACE_LINEAGE_SAMPLING_QUALIFICATION_SUITE_v0.1.md\`

Substrate/closure:
- \`SUBSTRATE_CLOSURE_QUALIFICATION_PREFLIGHT_v0.1.md\`
- \`PREDICTIVE_APPROXIMATE_CLOSURE_POLICY_v0.1.md\`
- \`PREDICTIVE_CLOSURE_CALIBRATION_PREFLIGHT_v0.1.md\`
- \`PREDICTIVE_CLOSURE_CALIBRATION_POSTRESULT_v0.1.md\`

Continuous lineage:
- \`CONTINUOUS_LINEAGE_SPECTRAL_ADEQUACY_POSTRESULT_v0.1.md\`
- \`CONTINUOUS_LINEAGE_FINITE_PROBE_POSTRESULT_v0.1.md\`
- \`CONTINUOUS_LINEAGE_C1Q_PREFLIGHT_v0.1.md\`
- \`CONTINUOUS_LINEAGE_C1Q_POSTRESULT_v0.1.md\`
- \`C1Q_ADVERSARIAL_CONTROLS_POSTRESULT_v0.1.md\`
- \`C1Q_FAMILY_BOUNDARY_CONTROLS_POSTRESULT_v0.1.md\`
- \`C1Q_PAIRED_SAMPLING_SEMANTICS_POSTRESULT_v0.1.md\`

Scope and structural refusal:
- \`D1Q_DISCRETE_CONTROL_PREFLIGHT_v0.1.md\`
- \`STRUCTURAL_ORDER_REFUSAL_PREFLIGHT_v0.1.md\`

This working file is the first document to read for state, but source-specific claims must remain traceable to these records and their workflow artifacts.

## 19. Living Update Protocol

Every meaningful scientific update must update this file in the same checkpoint cycle.

A scientific update includes:
- a new theorem or exact boundary;
- a new known-truth result;
- a new empirical result;
- a threshold freeze, revision, or retirement;
- a family/estimator promotion or demotion;
- a new refusal rule;
- a root-cause result that changes interpretation;
- a failure that materially changes the next experiment;
- a change to N-B1/N-B2/N-B3 architecture;
- a change to the current next experiment.

Each update must record:

1. **What changed.**
2. **Evidence/provenance**, including run, artifact, commit, or source document where available.
3. **Why it matters.**
4. **What it does not license.**
5. **Threshold impact**, explicitly stating frozen, revised, retired, or still unfrozen.
6. **What comes next and why.**

Threshold entries must additionally state:
- exact mathematical or empirical definition;
- value and units;
- direction of pass/refusal inequality;
- applicable regime/population;
- calibration dataset or known-truth family;
- whether discovery, qualification, or confirmatory;
- version/date;
- effect on prior results.

No threshold may be silently changed by editing an old number. Changes must preserve the superseded value and reason.

## 20. Current One-Sentence State

**Bio Chi is currently testing whether a native continuous-time biological mode can carry a sampling-invariant local chi under identifiable second-order structure and predictive approximate closure; the continuous-lineage target is mathematically coherent, but finite-data family scope, colored/memory refusal, uncertainty, and closure tolerances remain unresolved, so real-EEG local chi is still refused.**


## 20.1 Active Qualification Experiment: Combined Structural-Predictive Refusal

**Status:** LAUNCHED / RESULT PENDING  
**Preflight:** \`NSD_vNext/docs/COMBINED_STRUCTURAL_PREDICTIVE_REFUSAL_PREFLIGHT_v0.1.md\`  
**Probe:** \`NSD_vNext/engine/tools/probe_combined_structural_predictive_refusal.py\`  
**Workflow:** \`.github/workflows/nsd-combined-structural-predictive-refusal.yml\`

### What changed

The investigation is no longer waiting at the structural-order overlap finding. A qualification-only experiment has been launched to test whether colored/extra-pole truth can be distinguished by a **combined refusal pattern** rather than by any single structural statistic.

The experiment jointly records:
- frozen-parameter held-out NLL;
- held-out innovation autocorrelation;
- held-out innovation RMS;
- positive-lag recurrence residual;
- Hankel singular-value ratios;
- C1Q versus D1Q scope behavior;
- A0/A1/A2 training and holdout comparison as descriptive control.

### Why

C1Q can absorb colored-process truth, while finite-sample recurrence/Hankel diagnostics overlap materially with valid second-order controls. Neither model selection nor one raw order statistic is sufficient alone.

The combined map asks whether independent consequences of misspecification move together strongly enough to support a later prospectively frozen refusal design.

### What this does not license

- no real-EEG local chi;
- no new production estimator;
- no structural-order threshold;
- no predictive-closure threshold;
- no promotion of C1Q or D1Q;
- no disorder opening.

### Threshold impact

**No threshold is frozen or revised.** The output is distributional and threshold-free. If diagnostic distributions still overlap materially, the next move will be a stronger explicit higher-order/memory comparator or a more conservative refusal architecture rather than post hoc cutoff tuning.

### What comes next and why

1. Observe the workflow result and preserve artifact provenance.
2. Audit whether colored and genuine multimode truths separate from C interiors across multiple independent diagnostic channels.
3. If they do, design a prospective calibration packet without selecting a cutoff from these same rows.
4. If they do not, advance to an explicit higher-order/memory comparator before any N-B1 promotion decision.


## 20.2 Combined Structural-Predictive Refusal Result

**Status:** COMPLETE / NO CLEAN REFUSAL SEPARATOR  
**Canonical postresult:** \`NSD_vNext/docs/COMBINED_STRUCTURAL_PREDICTIVE_REFUSAL_POSTRESULT_v0.1.md\`

### What changed

The combined diagnostic strategy was tested on untouched holdout data and **did not produce a clean finite-sample refusal signature for the colored-process extra-pole truth**.

Against pooled C-interior controls, threshold-free rank AUC for the colored truth was approximately:
- C1Q held-out NLL per sample: 0.037;
- C1Q innovation max absolute autocorrelation: 0.444;
- D1Q held-out NLL per sample: 0.037;
- D1Q innovation max absolute autocorrelation: 0.444;
- D1Q-minus-C1Q holdout NLL: 0.444;
- Hankel s3/s2: 0.407;
- normalized order-two recurrence hold-lag RMS: 0.482.

The colored truth therefore did not move monotonically away from valid C interiors across these diagnostics.

The population root cause is now clearer: the extra real pole is structurally genuine but weak in the covariance-Hankel spectrum. For the frozen analytic colored law, a 6x6 population Hankel matrix has approximately:
- s1 = 2.0123;
- s2 = 0.7020;
- s3 = 0.001692;
- s3/s2 = 0.002410;
- s3/s1 = 0.000841.

Finite-sample noise can therefore obscure the third structural component even though exact rank theory remains correct.

### Why it matters

The shortcut

\[
\text{several weak diagnostics}
\Rightarrow
\text{reliable structural-order gate}
\]

is now rejected.

The correct next question is explicit **nested recurrence-order comparison** on untouched holdout data, followed by an explicit likelihood-based higher-order/memory comparator if recurrence order still overlaps.

### What this does not license

- no real-EEG local chi;
- no C1Q or D1Q promotion;
- no structural-order threshold;
- no biological memory cutoff;
- no A2 physical-mode interpretation;
- no disorder opening.

### Threshold impact

No threshold was frozen, revised, or retired.

## 20.3 Active Qualification Experiment: Nested Recurrence Order

**Status:** LAUNCHED / RESULT PENDING  
**Preflight:** \`NSD_vNext/docs/NESTED_RECURRENCE_ORDER_COMPARATOR_PREFLIGHT_v0.1.md\`  
**Probe:** \`NSD_vNext/engine/tools/probe_nested_recurrence_order.py\`  
**Workflow:** \`.github/workflows/nsd-nested-recurrence-order.yml\`

The experiment fits order-2, order-3, and order-4 covariance recurrences on training covariance and scores their frozen predictions on untouched holdout covariance. The target pattern is order-3 improvement for colored extra-pole truth without comparable improvement for true order-2 controls, and order-4 improvement for genuine two-mode truth.

No cutoff is selected from this experiment. If improvement distributions still overlap materially, the next safe move is an explicit likelihood-based higher-order/memory comparator rather than threshold tuning.
