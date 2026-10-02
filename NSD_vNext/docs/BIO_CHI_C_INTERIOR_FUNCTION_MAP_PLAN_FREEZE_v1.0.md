# Bio Chi C-Interior Function Map Qualified Plan Freeze v1.0

**Freeze status:** QUALIFIED_FROZEN  
**Date:** 27 September 2026  
**APQ level:** APQ-2 SUBSTANTIAL  
**Qualified Plan Packet:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_PACKET_v0.2.md\`  
**Qualified Plan commit:** \`45d81671bc862437c92d12e79b6eef3d8faf18d2\`  
**Objection ledger:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_APQ_LEDGER_v0.1.md\`  
**Plan Delta:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_DELTA_v0.1.md\`  
**First-pass records:** \`BIO_CHI_C_INTERIOR_FUNCTION_MAP_APQ_PASS_A_v0.1.md\`, \`BIO_CHI_C_INTERIOR_FUNCTION_MAP_APQ_PASS_B_v0.1.md\`

## Frozen scientific scope

P0-D known-truth Function Mapping of the qualification-only C1Q candidate over the exact 16-cell qualification envelope and three fixed realization seeds in Plan Packet v0.2.

The plan maps:

- C1Q recovery of truth \(A,f_n,\chi,g\);
- generic second-order covariance-recurrence pole recovery as an attribution diagnostic;
- same-path practical fine/coarse rate sensitivity;
- optimizer and parameter-bound diagnostics;
- A0/A1/A2 comparison on four preselected sentinel cells only.

## Frozen design identity

- 16 explicit coordinates exactly as listed in Plan Packet v0.2;
- seeds \`104729\`, \`208457\`, \`417923\`;
- fine rate 256 Hz;
- exact factor-2 decimation to 128 Hz;
- 60 s fine duration;
- mechanical preflight cells 0, 5, 10, 15 at seed \`104729\`;
- sentinel comparator cells 0, 5, 10, 15;
- current committed C1Q implementation unless a mechanical defect forces a new plan version.

## Frozen claim ceiling

The result is an exploratory correct-specification estimator Function Map. It cannot:

- establish that biology belongs to C;
- estimate biological prevalence;
- promote C1Q;
- define a biological or empirical admission threshold;
- license real-EEG local \(\chi\);
- replace the existing Limit Map;
- convert already-viewed outcomes into untouched confirmation.

## Failure / refusal paths

Execution stops mechanically if truth construction, covariance validity, exact-decimation identity, frozen-design identity, artifact serialization, or required environment recording fails.

Poor scientific recovery does not stop or retune the map. It is preserved as the result.

The generic recurrence diagnostic may refuse when a stable underdamped pair is not estimable. C1Q may remain \`OPTIMIZATION_UNRESOLVED\` after the predeclared rescue. Both are valid outcome classes.

## Thresholds / tolerances

No scientific admission threshold is frozen.

Only numerical implementation tolerances needed for exact-contract verification and serialization are permitted. They may not be used to classify scientific success/failure.

## Reproducibility class

Numerical/decision-equivalent repeatability in the declared software environment is promised. Cross-platform bitwise identity is not promised. The workflow records Python, NumPy, SciPy, branch commit, coordinate manifest, and seeds.

## APQ qualification statement

The APQ reviews were role-isolated but produced by one cognition and are not represented as independent reviewers. Their MATERIAL objections were resolved by:

- explicit self-consistency/correct-specification claim limitation;
- independent-parameterization recurrence diagnostic;
- optimizer and bound diagnostics;
- corrected interpretation of same-path rate sensitivity;
- explicit prohibition on prevalence/failure-rate inference from three seeds;
- stochastic repeatability declaration.

No unresolved BLOCKER or MATERIAL objection remains for this bounded P0-D plan.

## Next gate

Execute the frozen mechanical preflight. If it passes mechanically, execute the full frozen Function Map without scientific retuning. If it reveals a mechanical defect, record \`PLAN_HOLD\` or \`PLAN_VERSION_SUPERSEDED\` before dependent execution.
