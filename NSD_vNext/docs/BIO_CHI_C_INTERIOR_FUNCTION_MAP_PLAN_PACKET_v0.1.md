# Bio Chi C-Interior Function Map Plan Packet v0.1

**Status:** APQ-2 DRAFT  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0, Section 15.4  
**Purpose tag:** `FUNCTION_MAPPING`  
**Parent P0-N:** `NSD_vNext/docs/BIO_CHI_P0N_PRIOR_ART_CONGLOMERATION_v1.0.md`  
**Parent A0:** `NSD_vNext/docs/BIO_CHI_A0_PRIOR_ART_CONGLOMERATION_ATLAS_v1.0.md`  
**Evidence intake:** `NSD_vNext/docs/BIO_CHI_EVIDENCE_INTAKE_v1.0.md`  
**Compliance:** `NSD_vNext/docs/BIO_CHI_COMPLIANCE_STATUS_v1.0.md`

## Scientific target

### Native scientific question

Across the intended one-mode continuous-time C family, where does the current qualification-only C1Q representation recover the true local pole coordinate coherently, where does recovery degrade, and how stable is that recovery under exact fine-to-coarse sampling of the same realized path?

### Residual novelty after P0-N/A0

The damping ratio, biological oscillator analysis, OU/state-space inference, model-order methods, identifiability, sampling aliasing, and projection memory are established prior art. The residual is a `NEW_INTEGRATION` / `NEW_BOUNDARY_TEST`: an explicit admission/refusal architecture that maps both the supported interior and the limits before a biological local (chi) is reported.

### Smallest live claim

Continuous-time family C is mathematically coherent as a prospective local-(chi) representation, but the finite-sample operating region of the current C1Q qualification candidate has not been mapped representatively. The next experiment may characterize estimator/function behavior inside C. It cannot establish biological prevalence or license real EEG.

### Hypothesis and alternatives

**Exploratory working hypothesis:** across a broad interior C qualification envelope, C1Q recovery of local (chi) and (g) will be stable enough that failures concentrate in identifiable conditioning/sampling regions rather than appearing arbitrarily throughout the interior.

Material alternatives:

1. recovery is broadly unstable across the interior, making C1Q unsuitable even as a qualification candidate;
2. recovery is asymmetric in (g), (chi), latent fraction, or frequency;
3. paired fine/coarse estimates drift materially even where exact lineage invariance holds;
4. optimization rather than statistical identifiability dominates apparent failures;
5. the selected synthetic envelope is too narrow or artificial to support even an estimator Function Map.

### Evidence class and claim ceiling

P0-D exploratory known-truth Function Map. The map is a qualification-envelope description and self-consistency/estimator-recovery study under correct family specification. It is not external biological validation and cannot promote C1Q or license real-EEG (chi).

## Inputs and provenance

### Material inputs

- exact continuous-time C-family simulator already versioned in the NSD qualification code;
- qualification-only C1Q implementation at `NSD_vNext/engine/nsd_engine/continuous_lineage_candidate.py`;
- current production A0/A1/A2 machinery only as a limited legacy comparator on frozen sentinel cells;
- existing C/D/S and closure Limit Map results as contextual companion evidence, not rerun as the primary map.

### Intake status

- synthetic known truths: `INTAKE_PASS`;
- literature/A0 evidence: `INTAKE_PASS_WITH_LIMITS`;
- real EEG: excluded from this plan.

### Already-viewed outcome information

Earlier C1Q results at the 10 Hz, (chi=0.30), (A=0.8), (g=0,pm0.75) reference cells are already viewed. Those exact cells are not used as the new space-filling map. Existing limit/adversarial outcomes remain qualification evidence and are not counted as new confirmation.

### Unavailable / blocked evidence

No real biological prevalence distribution exists for the synthetic coordinates in this plan. No claim will treat the synthetic design density as a biological frequency distribution.

## Native model and validity regime

The known-truth family is the underdamped continuous-time linear stochastic oscillator

[
K=
egin{bmatrix}
-alpha & -1 \\

u^2 & -alpha
end{bmatrix},
qquad
chi=rac{alpha}{sqrt{alpha^2+
u^2}},
qquad
g=rac{G}{Aalpha},
]

with stationary covariance constructed so (|g|<1) lies in continuous-lineage family C. Exact discretization uses (F=e^{KDelta t}) and (Q_d=P-FPF^	op).

Required assumptions:

- the truth is actually one underdamped continuous-time C mode;
- the scalar observation is the declared first state plus white observation noise;
- the fine sampling branch and exact factor-2 decimation remain alias-safe;
- C1Q's likelihood and optimizer are numerically valid over the frozen envelope.

Known failure modes outside the claim:

- colored or higher-order forcing;
- D\C or S\D laws;
- projection memory / inadequate closure;
- alias collision;
- near-critical or boundary singularity;
- genuine multiple modes;
- real biological nonstationarity or nonlinear regime switching.

These remain Limit Map concerns and are not redefined by the Function Map.

## Planned execution

### Frozen synthetic qualification envelope

The map uses 16 deterministic Sobol cells generated with SciPy Sobol dimension 4, `scramble=True`, seed `20260927`, mapped to:

- latent fraction (Ain[0.20,0.90]);
- natural frequency (f_nin[3,25]) Hz;
- true (chi=zetain[0.15,0.85]);
- (gin[-0.80,0.80]).

Exact frozen coordinates:

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

Realization seeds: `104729`, `208457`, `417923`.

Sampling:

- fine (f_s=256) Hz;
- same-path exact decimation factor (m=2) to 128 Hz;
- 60 s fine realization per cell/seed;
- fine/coarse pair is one metamorphic unit, not two independent observations.

### Ordered steps

1. Run a mechanical preflight on cells 0, 5, 10, and 15 with seed `104729`. The grid, estimator, and outcome fields are already frozen; preflight may expose only runtime/implementation defects.
2. If the preflight is mechanically valid, run all 16 cells x 3 seeds.
3. Fit C1Q independently at fine and coarse rates with the current committed implementation.
4. On sentinel cells 0, 5, 10, and 15 only, run current A0/A1/A2 comparison at fine and coarse rates as a descriptive legacy comparator. Sentinel selection is frozen before outcomes.
5. Record per fit:
   - optimizer success;
   - attempted and converged start counts;
   - fitted (A), (f_n), (chi), (g);
   - signed and absolute (chi) error;
   - signed and absolute (g) error;
   - natural-frequency error;
   - fine/coarse fitted-(chi) drift;
   - fine/coarse fitted-(g) drift;
   - distance of fitted (|g|) from the C boundary;
   - C1Q NLL/BIC;
   - sentinel A0/A1/A2 BIC winner and margin.
6. Summarize the full qualification envelope with per-cell and pooled range, median, and seed distribution. Do not select a best representative.
7. Preserve every finite fit, nonconvergence, refusal, and rescue attempt.
8. Do not set an empirical admission threshold from these rows.

### Optimization failure handling

A fit is marked `OPTIMIZATION_UNRESOLVED` if no finite solution exists, the selected solution is invalid, or the optimizer diagnostic shows insufficient convergence for interpretation. A predeclared mechanical rescue may rerun the same cell with `optimizer_maxiter=160` and `max_optimized_starts=24` without changing the scientific grid. Both original and rescue results remain in the artifact. Rescue does not convert a scientific miss into a pass.

### Compliance and design-adequacy state

- Section 0.7: `NOT_APPLICABLE` for synthetic computation.
- Section 19.2: `NOT_APPLICABLE` because this is P0-D known-truth Function Mapping, not P1 empirical confirmation.

### Uncertainty and summary

The three realization seeds characterize finite-sample variation descriptively. They are not treated as biological replicates or as a powered inferential sample. No confidence interval or pass threshold is inferred from (n=3) seeds. If dispersion is large enough to change interpretation, a later qualification plan must address uncertainty explicitly.

### Checkpoints / artifacts

Expected artifacts:

- frozen design manifest;
- row-level JSON/CSV;
- summary JSON/Markdown;
- workflow/run identity;
- reproducibility-guide verification section;
- updated `WORKING_INVESTIGATION.md`.

## Outcome architecture

**Supports continued C1Q qualification:** recovery is broadly coherent across the frozen C interior, with errors/paired drift interpretable as finite-sample or conditioning effects and no widespread optimization failure.

**Narrows the claim:** coherent recovery is restricted to identifiable subregions, signs of (g), frequencies, latent fractions, or damping regimes.

**Falsifies C1Q as a broadly useful qualification candidate:** material recovery failure occurs throughout ordinary interior cells rather than concentrating near identifiable conditioning regions.

**Refusal condition:** a cell cannot support a local estimator interpretation because the fit is numerically unresolved or the known-truth lineage itself violates the frozen alias-safe C assumptions.

**Need-more-information:** seed dispersion or optimizer ambiguity is too large to tell whether apparent regional structure is scientific or numerical.

**Null/indeterminate:** no interpretable relationship between location in the C envelope and estimator recovery emerges.

**Alternative-model success:** the legacy A1/A2 family outperforms C1Q on frozen sentinel C truths in a pattern that cannot be explained by the known (g=0) nesting or finite-sample fluctuation. This triggers qualification review rather than automatic family promotion.

## Dependency structure

Foundational dependencies:

1. exact C simulator is mathematically correct;
2. C1Q implementation matches its declared parameterization;
3. fine-to-coarse path construction is exact decimation of the same realization;
4. the frozen envelope remains inside the intended alias-safe underdamped C family.

If 1-3 fail mechanically, downstream results are invalid and execution stops for repair. If 4 fails for a cell, that cell is refused and the design must be reviewed rather than silently altered.

The biological interpretation can remain closed even if the estimator Function Map succeeds. No downstream real-EEG claim depends automatically on this map.

## APQ target

**Requested level:** `APQ-2 SUBSTANTIAL`

The plan must receive at least two role-isolated adversarial first passes, an objection ledger, evidence-mediated resolution, Plan Delta, shared-premise challenge, and frozen qualified version before the full map executes. The same cognition may perform role-isolated passes only with an explicit non-independence limitation.
