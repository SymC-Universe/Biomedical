# BioSystems tumor-normal protocol-lineage audit - 22 September 2026

**Status:** CLOSED / PROVENANCE CLARIFIED  
**Scope:** protocol chronology only; no biological outcome interpretation and no scientific retuning.

## Question resolved

The revision branch contains an earlier paired-n=20 tumor-normal authorization/config as well as the later TN-A1/TN-C1/TN-P20 execution architecture. This audit establishes which design is active and whether the later design was frozen before tumor-normal molecular outcomes were available.

## Chronology

1. An earlier paired-n=20 authorization was committed at `d5bfe478557275f6831329fce2a5c5aeee1e34b8` on 22 September 2026 at 19:51:11 UTC. It referenced `biosystems_tumor_normal_control_v1_0.json`.
2. GitHub Actions run `35776448724` attempted that design. Source acquisition and identity checks completed, but the biological execution command failed immediately with `ModuleNotFoundError: No module named 'src'`.
3. The failed run produced no `TUMOR_NORMAL_RUN_SUMMARY.json`, no global inference table, and no cancer biological summary. The failure occurred at module import before the biological runner could parse or calculate tumor-normal molecular effects.
4. A revised tumor-normal freeze was committed at `0717ce47914f069b98a2b919e9e4e1e799b15b0d` on 22 September 2026 at 20:46:03 UTC. It prospectively restored the already-calibrated n=30 Stage A/C1 design as the primary RNA and multiomic comparison and retained paired n>=20 RNA as sensitivity.
5. TN-C0 then ran as a metadata-only gate. Final TN-C0 closure was recorded at run `35784202933` / commit `52599f2521df4819bd5cbaa21372a8f45713f04a`, with molecular values explicitly sealed.
6. The TN-A1/TN-C1 execution contract was first committed at `0a8013b258fd908767199ded9a3af2536066a819` at 22:13:34 UTC, before the first TN RNA molecular execution attempt at 22:16:19 UTC.
7. Subsequent pre-outcome-binding commits fixed source-row identity and symmetric common-probe construction. Later execution repairs have been mechanical only: writable-array handling, paired-only KICH routing, worker-count parallelization, and restoration of frozen participant order after pandas column selection.

## Active evidence contract

For manuscript and reviewer purposes, the active tumor-normal design is:

- **TN-A1 RNA primary:** 12 cancers, n=30 tumor and n=30 normal, 100 deterministic draws.
- **TN-C1 multiomic primary:** 5 cancers, n=30 RNA+methylation overlap per state, 100 deterministic draws.
- **TN-P20 paired RNA sensitivity:** 13 cancers with >=20 paired participants, fixed paired n=20 sensitivity.
- Cancer is the inferential unit.
- No tumor-normal direction is prespecified.
- Frozen outcome classes remain TN-SPECIFIC, TN-SHARED_WITH_SHIFT, TN-SHARED_NO_RESOLVED_SHIFT, TN-HETEROGENEOUS, and TN-NOT_EVALUABLE.

The earlier paired-n=20 authorization/config is retained as historical provenance and must not be treated as the active publication contract.

## GOM disposition

This lineage does **not** constitute post-result retuning because the earlier biological execution failed before molecular outcome computation, and the active TN-A1/TN-C1/TN-P20 architecture was frozen before the first molecular execution attempt.

The historical files are retained rather than deleted. Any reviewer-facing or manuscript-facing provenance map must point to the later tumor-normal freeze, TN-C0 eligibility closure, and TN-A1/TN-C1 execution contract as the active source of truth.

## Claim ceiling

This audit establishes only prospective protocol lineage. It does not establish tumor specificity, shared architecture, biological chi, capital-Chi dynamics, external validation, causality, or clinical utility.
