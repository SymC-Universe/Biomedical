# Bio Chi Profile Function/Limit Calibration APQ Pass B v0.1

**Plan reviewed:** `BIO_CHI_PROFILE_FUNCTION_LIMIT_CALIBRATION_PLAN_v0.1.md` at commit `571d684a3ad5af0cb0a82c311a962f9477966a68`  
**Lens:** computation, profile morphology, reproducibility, frozen design  
**Independence:** role-isolated review from one cognition; not an independent reviewer.

## Findings

1. **Strongest feature:** the full 12-class x 3-seed x 2-rate case identity is frozen before execution and all unfavorable rows are retained.
2. **Strongest assumption:** 72 profile jobs are computationally feasible with the already-qualified profile implementation.
3. **Most likely mechanical failure:** profile cases near chi or frequency bounds can require more nuisance optimization effort and may hit workflow timeouts even when scientifically valid.
4. **Hidden dependency:** morphology labels such as “open” or “closed” can silently become thresholded if not defined purely from recorded geometry.
5. **Competing explanation:** local-minimum counts on a finite 61-point grid can change under grid resolution and must not be treated as topological invariants.
6. **Missing control:** record the exact profile grid and all points; derived morphology should be secondary. Any edge/open label must be traceable directly to edge delta NLL and minimum location rather than a hidden cutoff.
7. **Missing numerical diagnostic:** preserve fitted raw-boundary distance and profile nuisance-boundary contact count to distinguish target-coordinate openness from nuisance optimizer saturation.
8. **Material objection B1:** add per-profile counts of nuisance solutions touching the raw optimization box.
9. **Material objection B2:** the execution should shard by case and use the same timeout budget as the already successful single-series profile jobs, with no runtime-driven scientific simplification.
10. **Minor B3:** the preflight should include one valid regular C case and one semantic Limit case exactly as planned, but their scientific outcomes must remain non-gating.

## Disposition recommendation

Proceed after adding explicit nuisance-boundary diagnostics, preserving the full profile as source of truth, and stating that all morphology labels are descriptive summaries with no hidden numerical admission rule.
