# Meneses 2026 context-transport root-cause diagnostic freeze

**Date:** 25 September 2026  
**Branch:** `bio-chi-meneses-context-transport-p0q-20260925`  
**Status:** FROZEN AFTER PRIMARY RESULT / BEFORE DIAGNOSTIC OUTPUT EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** POST-RESULT ROOT-CAUSE / STABILITY DIAGNOSTIC  
**Primary result:** `MENESES2026_IMMEDIATE_CONTEXT_TRANSPORT_P0Q_V01`

## Trigger

The frozen primary transport gate returned:

- sorbitol: `PARTIAL_GEOMETRY_TRANSPORT_P0Q`;
- sodium-phosphate-buffer context: `GEOMETRY_TRANSPORT_REFUSED_P0Q`;
- clockwise-lock/strain context: `PARTIAL_GEOMETRY_TRANSPORT_P0Q`;
- pooled one-dimensional compression: refused.

The sodium-phosphate-buffer lane preserved monotonic collapse amplitude ((ho=1)) while refusing the four-coordinate distance geometry. That mismatch is treated as an outlier/root-cause target rather than a reason to alter the primary threshold.

## Frozen diagnostics

All diagnostics are applied symmetrically to sorbitol, sodium-phosphate buffer, and clockwise-lock contexts relative to the sucrose/MB/CCW reference.

### D1. Leave-one-coordinate-out leverage

Recompute the distance-geometry Spearman correlation after omitting each one of the four frozen coordinates in turn:

- `A_dec`;
- `tau_dec`;
- `tau_inc`;
- `speed_increase_max`.

No leave-one-out result may replace the primary four-coordinate transport classification.

### D2. Central-tendency sensitivity

Recompute the same four-coordinate transport geometry using condition **means** rather than the frozen primary medians. This is motivated by the source manuscript's reporting of population means but is post-result here.

Classification strings are not reassigned from this sensitivity. Report only the mean-based rho and exact 24-permutation p.

### D3. Trace-bootstrap stability

Using the already fitted, unfiltered source traces, independently resample traces with replacement within every context-by-dose cell.

- bootstrap replicates: `B=2000`;
- deterministic seed: `20260925`;
- condition summary inside each bootstrap: median of the four fitted coordinates;
- standardization and geometry computation: identical to the primary frozen transport test.

For each target context report:

- median bootstrap geometry rho;
- 2.5th and 97.5th percentiles;
- fraction of replicates with rho >= 0.5;
- fraction with rho >= 0.8;
- fraction with rho <= 0.

## Interpretation rules

- Classify `SINGLE_COORDINATE_LEVERAGE` if exactly one leave-one-coordinate-out SPB rho is >=0.8 and all other leave-one-out SPB rhos are <0.5.\n- Otherwise classify `CENTRAL_TENDENCY_SENSITIVE` if the mean-based SPB rho is >=0.8 while the frozen median-based primary rho is <0.5 and the bootstrap 95% interval spans both rho <= 0 and rho >= 0.8.\n- Otherwise classify `DISTRIBUTED_CONTEXT_REORGANIZATION` if the SPB bootstrap median rho is <0.5, at least 25% of bootstrap replicates have rho <= 0, and the maximum leave-one-coordinate-out SPB rho is <0.8.\n- Otherwise classify `MULTIFACTOR_OR_UNRESOLVED_CONTEXT_REORGANIZATION`.

These labels explain the primary failure only. They cannot promote a refused transport result.

## Scalar rule

Scalar `chi_bio` remains unopened regardless of diagnostic outcome.

## Claim ceiling

Post-result same-source stability diagnostic. No new confirmatory evidence and no isolated causal claim about potassium, buffer ions, or rotor state.
