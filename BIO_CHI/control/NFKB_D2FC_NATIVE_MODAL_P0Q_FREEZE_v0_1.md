# NF-kB D2FC² native-modal biological chi freeze v0.1

**Date:** 26 September 2026  
**Branch:** `bio-chi-nfkb-d2fc-native-modal-p0q-20260926`  
**Status:** FROZEN BEFORE SYMC-SPECIFIC MODEL OUTPUT INSPECTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q literature-open source-model/native-modal qualification

## Why this is the next experiment

The Meneses E. coli and Stentor lineages support bounded context/path-sensitive whole-event organization, but neither source provides an independently identified damped modal carrier from which scalar `chi_bio` can be licensed.

The Lee et al. D2FC² NF-kB source is different. It includes experimental nuclear RelA data, experimentally fitted time-varying IKK inputs, a source-preferred mechanistic SimBiology model, alternative source model parameterizations, and an explicit fitting/validation split. It therefore gives scalar `chi_bio` a fair native-model test rather than constructing a scalar from response summaries.

## Source

Associated study: *Time-varying stimuli that prolong IKK activation promote nuclear remodeling and mechanistic switching of NF-κB dynamics*.

Pinned source repository:
- repository: `recleelab/D2FCSquared`
- commit: `4414c1556e3068c9bfe2162d5ba9d2cf770713fc`
- README blob: `b07594fcc55d7c3e38cb771adb6f441409cd65a1`
- D2FC² model blob: `71f91098b49c3621dfe54d156f29d4f8eea75ab9`
- source simulation helper blob: `674d69aadb6c1ccf467af5b907d25c34f1986b49`
- parameter source blob: `dc3cdff9de983d178e86c3a4b9521300b23fe744`
- experimental data blob: `4e4c7ee76e472d6730b0d8cb29eb0516eafdf772`
- mean IKK path blob: `aa7df5999a0d02ee0464caae634465e3dcc7aa11`
- single-cell IKK-fit blob: `7d199a8e410585ef83bd9be5c6e3323ccc263030`
- source average-run script blob: `f0dd64cf468a556d4ad49409c08ca76ba1b79a34`
- source single-cell-run script blob: `b216a0b2642a8a96a4d7683f3a634063ef8854c9`

Execution uses MATLAB R2024b with SimBiology, matching the source README requirement.

The qualitative source conclusion that time-varying IKK inputs alter NF-kB dynamics and can produce mechanistic switching was visible during candidate selection. This lineage is therefore literature-open and not blinded confirmation.

## Source-defined scenario split

Preserve the exact ordering and split used by `RunAverageIKKTrajectory.m`.

Source fitting set:
1. Control
2. 1X6 min
3. 1X30 min
4. 4X1.5 min

Source validation set:
5. 1X30 sec
6. 1X2 min
7. 1X15 min
8. 2X3 min
9. 3X2 min

No scenario is reassigned after outcome inspection.

## Stage A: source execution and trajectory fidelity

Run the source-preferred `D2FC²` model using the pinned `MeanIKKTrajectories.csv`, `ModelParameters.xlsx`, and `ExpData.mat`.

For each of the nine source scenarios:
- reproduce the source simulation with the pinned D2FC² model;
- interpolate model `RelativeNFkB_Nuc` to the experimental 0:4:181 minute grid;
- retrieve the corresponding source mean nuclear RelA trajectory using the pinned source helper;
- record RMSE, Pearson correlation, peak value, time to peak, AUC, and late 120--180 min mean for model and experiment.

Stage A is a source-reproduction gate, not a model-selection contest. It passes if:
- all nine source scenarios execute with finite trajectories;
- all nine experimental trajectories resolve to 46 finite source points;
- model and experiment are aligned on the source 0:4:181 minute grid.

No post-result RMSE threshold is introduced. Quantitative errors are reported and preserved.

If Stage A fails mechanically or source identities cannot be reproduced, modal interpretation does not open.

## Stage B: native post-stimulus recovery states

For each of the eight non-control scenarios, preserve the source-preferred D2FC² parameters and source IKK path.

Run the source simulation for its native 3 h stimulated window and record the complete 17-species state at the final simulated time.

For modal analysis:
- use that scenario-specific final state as the local state;
- set the source stimulation switch `TR=0`;
- retain all other source parameters unchanged;
- evaluate the autonomous local recovery dynamics with the IKK input disabled.

This asks about local recovery from the realized source-native state; it does not reinterpret the time-varying forced system itself as autonomous.

## Stage C: numerical Jacobian

For each non-control final state, estimate the 17x17 local Jacobian of the autonomous recovery system by central finite differences.

Baseline numerical scheme:
- local derivative horizon `dt=0.01 s`;
- species perturbation `delta_j=max(1e-10,1e-5*max(abs(x_j),1e-4))`;
- use a one-sided difference only if the negative perturbation would create a negative species amount;
- SimBiology absolute and relative tolerances `1e-10`;
- all source species are logged in source order;
- stimulation `TR=0` throughout each local derivative evaluation.

The derivative at state `x` is estimated from a source-model simulation over `dt` as
[
f(x)approx[x(dt)-x]/dt.
]

Every Jacobian, eigenspectrum, residual diagnostic, and numerical failure is preserved.

## Stage D: modal and scalar eligibility

A local eigenmode is a stable complex carrier when its eigenvalue is part of a conjugate pair
[
lambda=apm ib,qquad a<0,quad |b|>10^{-8} {m s}^{-1}.
]

Numerical conjugate matching tolerance is `1e-7` relative to eigenvalue magnitude.

For each stable complex pair, the established biological scalar candidate is the normalized native 2D pole invariant
[
chi_{mathrm{bio}}
=-rac{operatorname{tr}(J_{mathrm{pair}})}
       {2sqrt{det(J_{mathrm{pair}})}}
=-rac{Relambda}{|lambda|}.
]

This is the same trace/determinant invariant used in the closed Su oncology generator lineage. It is not a new scalar definition.

### Local scalar status

- zero stable complex pairs: `LOCAL_SCALAR_REFUSED_REAL_ONLY_OR_NONSTABLE`;
- exactly one stable complex pair: one local candidate may be reported;
- more than one stable complex pair: `LOCAL_SCALAR_REFUSED_NONUNIQUE_COMPLEX_CARRIER`.

### Family scalar admission

A D2FC² family-level `chi_bio` is admitted at P0-Q only if all eight non-control source scenarios contain exactly one stable complex pair under the baseline Jacobian scheme.

If any non-control scenario has zero or multiple stable complex pairs, the family scalar is refused without selecting a preferred pair post hoc.

## Stage E: numerical robustness if and only if the family scalar gate remains open

If Stage D finds exactly one stable complex pair in all eight non-control scenarios, rerun the Jacobian under the frozen sensitivity grid:

- `dt = 0.005, 0.02 s`;
- perturbation relative factor = `5e-6, 2e-5`.

The scalar family is robust only if every scenario remains exactly-one-complex-pair and every scenario's candidate `chi_bio` varies by less than 5% relative to its baseline value across all four sensitivity combinations.

Failure returns `SCALAR_REFUSED_NUMERICAL_CLASS_OR_VALUE_SENSITIVITY`.

No sensitivity grid is needed if the family gate is already refused at Stage D.

## Stage F: modal representation and whole-event relation

Regardless of scalar admission, report for every source scenario:
- full local eigenvalue spectrum;
- spectral abscissa;
- stable/unstable/near-zero mode counts;
- number of stable complex pairs;
- source trajectory feature vector;
- pairwise relative change of scenario-local Jacobians from the 1X6 min fitting reference.

`Chi_bio` is the source-native uncertainty-free D2FC² local modal family only if Stage A passes and all Jacobians are finite. No claim of superiority over the source ODE is permitted.

Biological chi at this gate is the bounded relation among source IKK path, realized NF-kB trajectory, and scenario-specific local recovery organization. It may be described only if Stage A passes and scenario-local modal organization is reproducibly computed.

## Source-model sensitivity

The source also provides D2FC optimized and original D2FC parameterizations. They are not used to choose the primary result.

After the D2FC² primary gate closes, repeat only the Stage-D complex-pair count at the same source scenarios under those two source variants as a model-form sensitivity.

This post-primary source-native sensitivity may narrow modal/scalar interpretation but cannot rescue a failed D2FC² gate or promote a scalar refused in the primary model.

## Biological chi hierarchy

- **biological chi:** bounded IKK-path -> NF-kB response -> local recovery-organization relation;
- **Chi_bio:** complete source-native local modal family if finite and source-reproduced;
- **chi_bio:** only the established trace/determinant invariant of a unique stable complex pair, and only if the frozen family and numerical-robustness gates pass.

No `chi_bio=1` criterion is used to rescue or select carriers.

## Failure/outlier rules

- MATLAB/SimBiology setup failure is infrastructure, not science.
- Source simulation failure is preserved by scenario and stage.
- A nonfinite state or Jacobian is a scientific/implementation refusal for that scenario.
- Zero, one, or multiple stable complex pairs are all valid outcomes.
- No eigenmode may be selected because its scalar value is near 1 or resembles another project.
- Near-zero eigenvalues are reported and never silently discarded.
- Alternative source model variants cannot retroactively redefine the primary D2FC² result.

## Claim ceiling

This lineage can establish only a P0-Q source/model qualification of native NF-kB modal organization and scalar eligibility in the pinned D2FC² system. It cannot establish a universal NF-kB scalar, biological `chi=1` boundary, common mechanism across E. coli/Stentor/NF-kB, cancer causality, or cross-system numerical universality.
