# Bio Chi C1Q Recurrence-Seed Rescue Postresult v1.0

**Status:** COMPLETE / P0-Q DISCRIMINATING RESULT  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Plan:** \`BIO_CHI_C1Q_RECURRENCE_SEED_PLAN_v0.1.md\`  
**Freeze:** \`BIO_CHI_C1Q_RECURRENCE_SEED_FREEZE_v1.0.md\`

## Provenance

- Workflow: \`NSD C1Q Recurrence Seed Rescue\`
- Run: \`36370056281\`
- Source head: \`b662ff5f23f1ecdfd72ee5e169af4f4b0f5888d2\`
- Complete artifact: \`nsd-c1q-recurrence-seed-complete\`
- Artifact ID: \`10948891782\`
- Digest: \`sha256:95a74a7d757e2f9afd0e37040414e66137a2825dbfa3780b8105a40be06da248\`

All eight frozen cell jobs completed successfully and the 48-row merge passed.

## Result

The truth-blind recurrence/covariance seed is a viable search-rescue mechanism for a substantial fraction of the observed C1Q failures, but it is not universally admissible or sufficient.

Across 48 rows:

- recurrence seed constructed successfully: **40/48**;
- explicit seed refusal: **8/48**;
- recurrence-seeded local fit beat the immutable source-selected C1Q solution: **26/48**;
- recurrence-seeded local fit matched or beat the previously frozen truth-seeded basin within numerical comparison tolerance: **32/40** admissible rows;
- \(A\) projection was required in **0/40** admissible seeds;
- \(g\) projection to the numerical C domain was required in **18/40** admissible seeds.

By rate:

- fine: seed ready 19/24, beat old selected 6/24, matched/beat truth-seeded basin 15/19;
- coarse: seed ready 21/24, beat old selected 20/24, matched/beat truth-seeded basin 17/21.

For admissible seeds, recurrence-seeded NLL minus old selected NLL had median approximately **-5.763**, with range approximately **-124.727 to +16.914**.

Recurrence-seeded NLL minus truth-seeded NLL had median effectively zero at numerical scale. Its range was approximately **-0.000059 to +22.932**. Thus most admissible recurrence seeds reach the same local basin found by truth-seeding, but a minority do not.

## Refusals and partial failures

Eight rows did not yield an admissible seed:

- cell 12, seed 104729: fine and coarse, recurrence not underdamped;
- cell 12, seed 208457: fine, recurrence not underdamped;
- cell 5, seed 417923: coarse, derived raw seed outside the current C1Q box;
- cell 8, seed 104729: fine and coarse, recurrence not underdamped;
- cell 8, seed 208457: fine, recurrence nonstable;
- cell 8, seed 417923: fine, recurrence not underdamped.

Among admissible rows, the largest failure to match the truth-seeded basin occurred at cell 8, seed 208457, coarse: the recurrence-seeded fit improved the old selected solution by about 60.35 NLL but remained about 22.93 NLL above the truth-seeded basin.

These outcomes prevent the recurrence seed from becoming a standalone replacement search route.

## Scientific interpretation

The result supports a narrower engineering conclusion:

1. observable positive-lag covariance contains enough information to recover the missed C1Q basin in many of the rows where the current multistart search fails;
2. the recurrence/covariance construction is especially useful at the coarse rate, where the old search failure was most prevalent;
3. recurrence refusal and \(g\)-projection are common enough that the seed must remain optional and diagnostic rather than replacing existing starts;
4. because the old start family remains useful in rows where the recurrence route refuses or is inferior, the natural next candidate is an **augmented multistart search** that preserves all existing C1Q starts and forces the recurrence/covariance seed into the optimized set when admissible;
5. the recurrence seed does not solve C1Q's semantic family-scope failures on colored, D\C, S\D, or multimode truths. Those remain mandatory Limit Map controls.

## Claim consequences

- **Current C1Q search route:** confirmed inadequate over a material part of the tested C interior.
- **Recurrence seed as standalone estimator/search:** not promoted.
- **Augmented C1Q search candidate:** justified for P0-Q qualification.
- **C1Q likelihood family:** remains live but unpromoted.
- **Real-EEG local \(\chi\):** unlicensed.
- **Scientific threshold:** none.
- **Biological prevalence:** none.

## Next action

Create a versioned qualification-only candidate, provisionally C1Q-RS, that retains the complete existing start family and forcibly includes the recurrence/covariance start when admissible. The likelihood, parameterization, parameter count, and biological claim ceiling remain unchanged.

Before any promotion, C1Q-RS must be adversarially qualified across:

- the full 16-cell C-interior Function Map;
- recurrence-refusal rows;
- existing nonzero-\(g\) C controls;
- isotropic/anisotropic/rank-1 forcing controls;
- colored extra-pole controls;
- genuine separated two-mode controls;
- D\C and S\D family-boundary controls;
- paired-sampling semantics.

The candidate may improve optimization. It must not erase or relabel model-family refusal failures.
