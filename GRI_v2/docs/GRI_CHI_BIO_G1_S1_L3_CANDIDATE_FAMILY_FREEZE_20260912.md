# GRI Chi_bio G1/S1/L3 candidate-family scientific freeze

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Scientific authorization:** user explicitly approved the recommended G1 + transcriptomic state + substrate/context + paired local/embedded plan on 2026-09-12.  
**Promotion state:** `NOT_ADMITTED`  
**Freeze class:** SCIENTIFIC CANDIDATE-FAMILY / STATE-SEMANTICS / SCOPE FREEZE  
**This is not yet `CANDIDATE_LOCKED`.**  
**Cancer-specific Chi_bio values inspected:** NO  
**Atlas/unity placement inspected:** NO

## 1. Approved scientific target

The approved primary route is now frozen as:

- **generator family:** G1 normalized regulatory-interaction family;
- **state semantics:** S1 transcriptomic regulatory state;
- **substrate/context role:** methylation is an external substrate/context modifier of the regulatory map, not a coordinate concatenated naively with RNA;
- **system scope:** L3 paired local + embedded analysis;
- **temporal comparator:** G2 discrete transition-operator family;
- **qualitatively different alternative:** G4 attraction/diffusion family.

This freezes what the investigation is trying to identify. It does not yet freeze a TCGA estimator or claim that the required G1 operator is identifiable from current data.

## 2. Frozen system semantics

Let `x` denote a transcriptomic regulatory state. The state may ultimately be represented at gene, predeclared module, or outcome-blind latent resolution, but the empirical reduction rule is **not** frozen here and may not be selected using cancer-specific Chi_bio values, Atlas placement, closeness to unity, or downstream outcome.

Let `s` denote epigenetic/substrate context, including methylation when justified. Let `e` denote embedding variables such as composition, microenvironment, treatment, and other environmental context.

The candidate family asks whether a biologically coherent regulatory map

```text
Phi(x ; s, e)
```

can be identified such that its local derivative with respect to the regulatory state,

```text
K = d Phi / d x
```

and the corresponding restoring/turnover structure define a model-native stability coordinate.

Methylation therefore changes or constrains the regulatory landscape/operator where evidence licenses that relationship. It is not declared dynamically equivalent to RNA merely because both are measured.

## 3. Local-versus-embedded freeze

The L3 scope is mandatory:

### Local object

A local/intrinsic regulatory generator is estimated or constrained for the modeled regulatory state under a declared substrate/context condition.

### Embedded realized behavior

Composition, microenvironment, treatment, and other external feedback are characterized separately as embedding/context. They may alter the realized operator or response.

### Relational question

The project must test whether the local coordinate, modal carrier, or response relationship is preserved, reorganized, or invalidated under embedding. Local and embedded stability may not be silently equated.

## 4. Scalar / modal / conglomerate architecture

The target architecture is frozen conceptually as:

```text
conglomerate/system object: coupled regulatory generator/operator
modal/vector view:          eigenvalues, invariant subspaces, left/right carriers, transient structure
scalar view:                one model-native stability coordinate only if derivation licenses it
```

No arithmetic averaging of H2, H3a, H3b, CKA, principal angles, S_spec, or other existing GRI metrics is permitted to manufacture this scalar.

## 5. Important hardening result discovered immediately after approval

The original G1 source model gives an exact unity boundary because its local Jacobian has the special form

```text
J = beta0 (M - I), beta0 > 0.
```

The approved S1 transfer to a transcriptomic state cannot assume that same structure automatically.

For a more general local transcriptomic linearization

```text
J = K - R
```

with regulatory/production Jacobian `K` and restoring/turnover operator `R`, defining

```text
M = R^-1 K
```

does **not** generally imply

```text
alpha(J) < 0  iff  alpha(M) < 1.
```

This fails for heterogeneous restoration combined with a directed/non-normal regulatory operator. Two exact 2x2 counterexamples are now executable regression tests in `tests/test_chi_bio_g1_hardening.py`.

Therefore the project will not freeze `alpha(R^-1 K)` as Chi_bio merely because it resembles the source-model `M`.

## 6. Exact G1 unity routes still licensed for testing

Two mathematically exact routes survive the hardening pass:

### G1A common-restoration route

If

```text
R = beta I, beta > 0,
```

then

```text
J = beta (M - I), M = K / beta,
```

and

```text
alpha(J) = beta [alpha(M) - 1].
```

Unity is exactly the local linear stability boundary.

### G1B symmetric/generalized route

If `K` is symmetric and `R` is symmetric positive definite, then

```text
G1B = lambda_max(R^-1/2 K R^-1/2)
```

has the exact boundary

```text
G1B < 1  iff  K - R is negative definite.
```

This follows from the inertia-preserving congruence of the symmetric generalized eigenproblem. It is **not** licensed for a general directed regulatory network.

### General directed heterogeneous case

For a general directed/signed transcriptomic network with heterogeneous restoring rates, the local truth is the spectrum of

```text
J = K - R.
```

A natural unity-valued G1 scalar has not yet been derived for that general class. If no independently justified normalization exists, the correct outcome is to narrow/reject the G1 unity construction rather than force it.

## 7. Biological reason this hardening matters

The Guo-Amir source model is a specific protein-allocation regulatory model. It cannot be transferred to bulk transcriptomic state by renaming variables. Mammalian mRNA stability is gene- and context-dependent, and contemporary GRN inference distinguishes mechanistic regulatory interactions from statistical correlation. Those facts make a common restoring rate or symmetric interaction operator an empirical/model assumption that must be demonstrated rather than assumed.

Primary source retained for the native G1 derivation:

- Guo Y, Amir A. *Exploring the effect of network topology, mRNA and protein dynamics on gene regulatory network stability.* Nature Communications 12, 130 (2021). DOI: 10.1038/s41467-020-20472-x.

Additional literature hardening:

- Agarwal V, Kelley DR. *The genetic and biochemical determinants of mRNA degradation rates in mammals.* Genome Biology 23, 245 (2022). DOI: 10.1186/s13059-022-02811-x.
- Badia-i-Mompel P et al. *Gene regulatory network inference in the era of single-cell multi-omics.* Nature Reviews Genetics 24, 739-754 (2023). DOI: 10.1038/s41576-023-00618-5.
- Maizels RJ, Briscoe J. *Gene regulatory networks: from correlative models to causal explanations.* Nature Reviews Genetics 27, 485-498 (2026). DOI: 10.1038/s41576-026-00939-1.

## 8. Frozen anti-fitting rules

The following may not determine the G1 subvariant, empirical state reduction, restoration model, or substrate coupling:

- cancer-specific candidate Chi values;
- closeness to 1;
- favored cancer ordering;
- Atlas placement;
- treatment response labels used both to define and validate the coordinate;
- downstream survival/clinical outcome;
- suppression of cancers or modes that disagree.

## 9. Promotion consequence

The science decision boundary from `GRI_CHI_BIO_SCIENCE_DECISION_PACKET_20260912.md` is resolved at the family/state/scope level.

However, `CANDIDATE_LOCKED` is **not** yet earned because CB7-CB9 remain to be completed at candidate-specific strength, and the exact unity-bearing G1 subvariant is conditional on restoration/operator structure.

Current gate disposition:

```text
CB1 semantic definition:                 PASS at family/state/scope level
CB2 native generator/derivation:         PASS for G1 source family; transfer remains conditional
CB3 natural normalization:               PASS only for G1A/G1B exact subcases; OPEN for general directed S1
CB4 meaningful native observables:       PARTIAL / measurement mapping open
CB5 scalar-modal-conglomerate relation:  PASS structurally
CB6 outcome/Atlas independence:          PASS by freeze design
CB7 competing-generator identifiability: OPEN
CB8 uncertainty/tolerance:               OPEN
CB9 known-truth recovery/refusal:        ACTIVE, generator-specific harness now authorized
```

## 10. Next execution path

Without inspecting cancer-specific Chi_bio outcomes:

1. freeze and run G1A/G1B/general-directed known-truth and known-failure cases;
2. quantify when the naive normalized G1 construction disagrees with the true local Jacobian;
3. develop uncertainty and near-degeneracy/refusal logic;
4. keep G2 as the temporal comparator and fallback candidate if G1 cannot satisfy its own derivation;
5. preserve G4 as a structurally different stochastic alternative;
6. ingest completed C1/post-C1 archives read-only when available for later estimator identifiability work;
7. do not compute cancer-specific Chi_bio values until a candidate-specific estimator is frozen.

## 11. Current scientific status

**Approved:** G1 family + S1 transcriptomic state + methylation as substrate/context + L3 paired local/embedded analysis.  
**New derivational finding:** the simple `alpha(M)=1` boundary does not automatically survive a generic transcriptomic transfer.  
**Exact scalar subvariant:** CONDITIONAL / not yet frozen.  
**Chi_bio promotion state:** `NOT_ADMITTED`.  
**Biological unity boundary:** NOT_ADMITTED.
