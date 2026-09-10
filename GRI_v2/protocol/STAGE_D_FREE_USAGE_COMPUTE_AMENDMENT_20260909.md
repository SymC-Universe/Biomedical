# Stage D free-usage compute amendment

Date: 2026-09-09
Status: MECHANICAL EXECUTION AMENDMENT ONLY

## Reason
GitHub Actions jobs were initially blocked by account billing state. After billing access was restored, the Stage-D preflight was re-run on a standard GitHub-hosted Ubuntu runner and began executing normally. The first executable failure was then traced to a Python boolean typo (`false` instead of `False`) in the metadata audit object, not to the scientific design.

The same re-run also revealed that the original metadata inventory stored full GEO family SOFT files inside the Actions artifact directory, producing an approximately 748 MB artifact. Although the parser did not analyze numeric assay values, this was unnecessarily large, potentially consumed artifact-storage allowance, and was stricter than needed for a metadata-only gate.

## Mechanical changes
1. Stage-D GitHub jobs are constrained to standard public-repository GitHub-hosted Linux labels (`ubuntu-latest` or `ubuntu-24.04`). Larger runners, GPU runners, paid runner groups, and custom-image runners are forbidden.
2. Stage-D heavy numerical work remains routed to Kaggle or PowerCell rather than GitHub Actions.
3. The D0 metadata inventory now uses GEO `view=brief` metadata endpoints only and does not download family SOFT, series matrices, supplementary numeric files, or raw assay data.
4. The Python boolean typo is corrected.
5. Stage-D preflight artifacts are compact metadata/validation outputs only and are retained for one day.
6. Concurrency cancellation is enabled so superseded preflight jobs do not run simultaneously.

## Scientific effect
None. No dataset role, hypothesis, endpoint, threshold, null, promotion rule, biological interpretation, or Stage C1/P0 result was changed. This amendment only constrains compute cost, tightens the metadata-only firewall, and repairs execution mechanics.

## Supersession
`GRI_v2/config/stage_d_compute_routing_v0.2.json` supersedes v0.1 for execution routing only. The Stage-D scientific freeze remains authoritative and unchanged.
