# Bio Chi P0-D testbed eligibility contract v0.1

**Frozen:** 22 September 2026  
**Status:** P0-D SOURCE/DESIGN QUALIFICATION  
**Purpose:** classify candidate datasets before any newly designed Bio Chi analysis uses their target outcomes.

## General rule

Eligibility is determined from experimental design, source accessibility, native biological measurement, and the question to be tested.

A dataset is not promoted because its published result agrees with SymC.

Different testbed classes have different gates. Failure in one class does not make the dataset scientifically worthless; it changes the question that the dataset may answer.

## Class R — recovery / reorganization

### Hard gates

R0. Exact source identity can be frozen and reproduced.  
R1. A defensible pre-perturbation reference state exists.  
R2. Perturbation identity and ordering are defined.  
R3. Perturbation is removed, terminated, or followed by a scientifically equivalent recovery interval.  
R4. At least one post-perturbation state is measured after removal/termination.  
R5. A native return/reorganization endpoint can be defined without SymC.  
R6. Time ordering is not reconstructed solely from cross-sectional similarity.

### Depth flags

- **R-DENSE:** repeated post-removal measurements allow path/timescale/hysteresis analysis.
- **R-SPARSE:** recovery is directly measured but with insufficient temporal density for detailed path inference.
- **R-RECHALLENGE:** repeated perturbation/rechallenge exists.
- **R-REFUSE:** no removal/recovery phase; recovery claims are prohibited.

## Class M — modal/vector Χ_bio

### Hard gates

M0. State vector or native multivariate representation is defined.  
M1. Mode/subspace/carrier construction can be frozen independently of the downstream claim.  
M2. Enough temporal, perturbational, or repeated-state information exists to identify or test the modal representation.  
M3. Degeneracy/conditioning/representation dependence can be assessed.  
M4. A native/simple comparator is available.

A static multiomic geometry may inform architecture discovery but does not automatically qualify as a dynamical modal test.

## Class S — scalar χ_bio

### Hard gates

S0. A native biological generator/reduction is specified.  
S1. The scalar is derived from the generator rather than named by analogy.  
S2. Required rate/frequency/state quantities refer to the same coordinate/mode.  
S3. Parameters or local poles are identifiable with uncertainty.  
S4. The interpretation survives justified representation/state choices or is explicitly scoped.  
S5. Strong native/simple alternatives are compared.  
S6. Any proposed boundary is derived/frozen before decisive outcome testing.  
S7. Independent transport is required before broad admission.

A complex eigenpair may be retained as pole geometry without satisfying S1 for a mechanical damping ratio.

## Class I — Stability Inheritance

### Hard gates

I0. Parent/substrate is characterized before target reveal in the new test.  
I1. Carrier correspondence is explicit.  
I2. Parent-to-child mapping is frozen.  
I3. Child/recovery target is independently generated.  
I4. Intervention/counterfactual tests the proposed carrier.  
I5. Scrambled/generic/expression-only or other appropriate specificity controls are included.  
I6. Nonidentifiability/refusal is allowed.

Static cross-layer association cannot satisfy Class I by itself.

## Class C — Bio Chi conglomerate/system

### Hard gates

C0. At least two independently defined representation layers are available.  
C1. Cross-level relation is tested, not assumed.  
C2. Coupling/context/history/substrate contributions are separated where identifiable.  
C3. Held-out or prospective behavior tests whether the conglomerate adds information beyond simpler representations.  
C4. Disagreement among scalar/modal/conglomerate views is retained.  
C5. Failure to add value is a valid result.

## Current opening classifications

| Testbed | R | M | S | I | C |
|---|---|---|---|---|---|
| Rehman 2021 CRC DTP | PASS R-RECHALLENGE | candidate | no current scalar | candidate | candidate |
| Su 2026 melanoma hysteresis | PASS R-DENSE/R-RECHALLENGE | strong candidate | exploratory only | candidate | strong candidate |
| Marsolier 2022 TNBC H3K27me3 | PARTIAL recovery | candidate | no current scalar | strong candidate | candidate |
| Harmange 2023 scMemorySeq | PARTIAL recovery/rechallenge | strong state/lineage candidate | no current scalar | strong candidate | candidate |
| Sharma 2010 PC9 | PASS R-SPARSE | limited | no current scalar | candidate | candidate |
| Shaffer 2017 melanoma | PASS boundary/reversion | candidate | no current scalar | candidate | strong boundary case |
| Lee 2014 paclitaxel | PASS R-SPARSE | limited | no current scalar | weak | secondary |
| Jiang 2020 yeast memory | PASS design, source pending | candidate | generator-dependent | mechanistic qualification | candidate |
| McFarland MIX-Seq | **R-REFUSE** | response modes only | no admission | no recovery inheritance | response-only |
| sci-Plex | **R-REFUSE** | response manifold only | no admission | no recovery inheritance | response-only |
| Identifiable NF-kB reduced model | model-based recovery protocol | strong | **strongest S candidate** | not inheritance test | candidate |
| Son 2021 NF-kB | partial recovery/refractory | strong | candidate with access risk | no | candidate |
| Geva-Zatorsky 2006 p53 | no finite recovery design | strong oscillator limit case | adversarial S case | no | limited |
| Blum 2019 ERK | PASS washout/rebound | strong | candidate | no | candidate |

## Promotion rule

No testbed is promoted beyond P0-D from this table.

P0-Q requires a separate frozen analysis contract and reproducible source manifest. P1 requires untouched decisive evidence and full MFR controls.
