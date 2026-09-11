# P0 Assignment-Margin Correction

Date: 2026-09-10/11
Status: **P0 DIAGNOSTIC CORRECTION. NO SCIENTIFIC RESULT RESCORED.**

The first order/rank sweep exposed negative values in the field named `assignment_margin`. Investigation showed that the implementation compared a globally chosen Hungarian pair against row/column-local alternatives. A globally optimal assignment can contain a pair that is not individually row- or column-optimal because the remaining assignments are coupled, so that quantity was not a valid nonnegative ambiguity margin.

The corrected definition is:

> For each selected pair, forbid that pair, re-solve the complete Hungarian assignment, and report the increase in total globally optimized assignment cost.

Consequences:

- exact alternative global assignments yield margin `0`;
- uniquely supported assignments yield positive margins;
- infeasible alternatives yield infinite margin;
- a materially negative margin is treated as an implementation error because it would imply the original assignment was not globally optimal.

This is a diagnostic-definition correction only. No threshold is introduced, no pair is promoted to `shared`, `lost`, or `added`, and no P1 result exists to rescue or reinterpret. The original run remains preserved in GitHub Actions provenance; the sweep is rerun after this correction before any stability interpretation is recorded.
