# GRI Chi_bio G2 reduced-order system-identification literature collision

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D methodology / prior-art collision before empirical state freeze  
**Candidate role:** G2 temporal comparator  
**Chi_bio outcomes inspected:** NO

## 1. Question posed before empirical fitting

The G2 route asks whether an ordered low-dimensional transcriptomic state can support a discrete transition operator whose spectral radius is a meaningful system-level stability coordinate.

Before selecting a state reduction, the relevant prior-art questions are:

1. is low-rank projection before operator identification a native method rather than an ad hoc GRI construction?
2. how is exogenous treatment represented in an established operator framework?
3. what are the known failure modes when rank is chosen poorly or the system varies in time?
4. does existing literature remove the need for a prospective rank/state freeze?

## 2. Dynamic mode decomposition is native prior art for reduced sequential operators

Schmid introduced dynamic mode decomposition (DMD) as a way to extract dynamic information and coherent modes from high-dimensional sequential measurements, including experimentally observed systems, and to represent the dynamics in a lower-dimensional modal system.

Reference:

- Schmid PJ. *Dynamic mode decomposition of numerical and experimental data.* Journal of Fluid Mechanics 656, 5-28 (2010). DOI: `10.1017/S0022112010001217`.

This establishes that the broad G2 concept

```text
high-dimensional sequential measurements
-> low-dimensional state/subspace
-> fitted linear transition operator
-> eigenvalue/mode analysis
```

is established system-identification/model-reduction territory.

**Novelty consequence:** the mere use of a low-rank transition spectrum is not a novel SymC result.

## 3. Rank truncation is a model choice, not a free preprocessing step

Standard/exact DMD computes the operator through a pseudoinverse commonly obtained from an SVD, with a truncated rank `r` used to reduce the state space. Reviews and practical analyses emphasize that this truncation changes the representation and resulting modes.

References:

- Schmid PJ. *Dynamic Mode Decomposition and Its Variants.* Annual Review of Fluid Mechanics 54, 225-254 (2022). DOI: `10.1146/annurev-fluid-030121-015835`.
- *Challenges in dynamic mode decomposition*, Journal of the Royal Society Interface / open-access methodological analysis (2022-era literature; retained here as methodological context rather than candidate-defining authority).

For GRI, this means:

```text
rank r is part of the scientific representation
not a mechanical knob to tune after Chi values are seen.
```

The existing state-reduction firewall is therefore necessary, not excessive.

## 4. Exogenous treatment has established operator-system prior art

Dynamic Mode Decomposition with Control (DMDc) extends the operator relation to include control/input terms, conceptually matching

```text
x_(k+1) = T x_k + B u_k.
```

Reference:

- Proctor JL, Brunton SL, Kutz JN. *Dynamic Mode Decomposition with Control.* SIAM Journal on Applied Dynamical Systems 15 (2016). DOI: `10.1137/15M1013857`.

This is directly relevant to cetuximab/PBS temporal sources because treatment can be represented as an explicit exogenous input rather than being hidden inside a condition-specific scalar.

**Novelty consequence:** the `T + B u` architecture is prior art. Any residual GRI contribution must lie in the biological state definition, independent substrate/context relation, admission/refusal logic, cross-timescale/cross-system predictions, and evidence that the resulting coordinate has additional biological utility beyond standard system identification.

## 5. Short high-dimensional time series have a recognized overfitting problem

Reduced-rank linear dynamical-system literature explicitly treats short, high-dimensional time series as vulnerable to overfitting and develops reduced-rank/regularized models to control the effective latent dimension.

Reference:

- She Q, Gao Y, Xu K, Chan R. *Reduced-Rank Linear Dynamical Systems.* AAAI 32 (2018). DOI: `10.1609/aaai.v32i1.11666`.

A related high-dimensional system-identification line uses explicit low-rank and regularized estimators.

Reference:

- Chen S et al. *An M-estimator for reduced-rank system identification.* Pattern Recognition Letters 86, 76-81 (2017). DOI: `10.1016/j.patrec.2016.12.012`.

For SCC25, this reinforces the already derived algebraic result that `d<=18` or `d<=9` is only a formal ceiling, not a sensible target dimension.

The practical representation should be materially lower-dimensional or more strongly structured.

## 6. A constant operator is itself a falsifiable assumption

Time-varying DMD methods exist specifically because one fixed operator need not describe nonstationary systems.

Reference:

- Zhang H, Rowley CW, Deem EA, Cattafesta LN. *Online Dynamic Mode Decomposition for Time-Varying Systems.* SIAM Journal on Applied Dynamical Systems 18 (2019). DOI: `10.1137/18M1192329`.

This literature collision supports the GRI refusal branch already frozen:

```text
if one T is rejected by the ordered transitions,
report time variation / regime dependence / model refusal;
do not average the trajectory into a convenient fixed operator.
```

The existence of time-varying operator methods also means that failure of a constant G2 model is not evidence that the biological series is incoherent. It may simply require a different native temporal model.

## 7. What prior art does and does not resolve

### Prior art resolves

- low-rank operator fitting is established;
- SVD/PCA-like reduction before DMD is established;
- treatment/control inputs can be represented explicitly;
- transition spectra and modes are standard system-identification objects;
- time-varying operators are established alternatives when stationarity fails;
- short high-dimensional time series require rank/regularization discipline.

### Prior art does not resolve for GRI

- what the biologically correct transcriptomic state is;
- which reduction is independent enough for the SCC25 falsification test;
- whether a candidate state transports from daily to weekly SCC25 experiments;
- whether it transports from SCC25 to SCC1;
- whether ATAC substrate/context organization preserves or reorganizes the same relation;
- whether a scalar spectral radius provides useful compression after modal/non-normal information is retained;
- whether a GRI-specific biological unity interpretation survives independent evidence;
- whether any residual GRI novelty remains after comparison with DMD/DMDc/state-space prior art.

## 8. Candidate reduction consequence

This collision strengthens **R1 control-only unsupervised basis** as a legitimate G2 feasibility architecture because fitting a reduced basis then identifying a transition operator is methodologically native.

It does **not** authorize choosing the rank after looking at treated dynamics.

A defensible first G2 freeze should therefore specify in advance:

```text
basis fit role = PBS control only
candidate ranks = prospectively bounded small set or one fixed rank
rank-selection rule = control-only / outcome-blind
transition form = shared T + treatment input B or separately frozen alternative
intercept handling = fixed
conditioning/refusal rule = fixed
residual/model-adequacy rule = fixed
```

The exact rank-selection rule remains a scientific choice and is not frozen by this literature pass.

## 9. Attribution / residual novelty ledger entry

The following must not be described as uniquely SymC:

- DMD/eigenanalysis of a reduced transition operator;
- SVD rank truncation;
- DMD with explicit control;
- time-varying DMD;
- generic low-rank state-space identification.

Potential residual novelty, if later supported, would instead require evidence for the specific GRI relational architecture:

```text
transcriptomic state + independently represented substrate/context
+ scalar/modal/conglomerate reporting
+ pre-Atlas admission/refusal discipline
+ cross-timescale and cross-system transport predictions
+ independently supported biological boundary interpretation
```

No novelty claim is made here. This is an attribution-preserving collision pass.
