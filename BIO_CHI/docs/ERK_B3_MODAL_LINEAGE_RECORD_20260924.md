# ERK B3 Bio Chi Modal Lineage Record

**Date:** 24 September 2026  
**Authority:** SymC General Operations Manual v0.8.6  
**Current branch:** `bio-chi-erk-modal-v2-p0q-20260924`  
**Status:** CLOSED AFTER V2 REFUSAL WITH BOTH LIMITS PRESERVED

The ERK B3 lineage now contains two distinct modal qualification questions and neither is allowed to overwrite the other.

The starting point was the publication-selected deterministic Blum 2019 B3 ERK model. Its source identity, topology, parameter lanes, state order, sustained-FGF contexts, and deterministic FRET output were frozen before SymC generator analysis. The first native-reproduction attempt failed mechanically on the source time grid before the solver or trajectory result opened. That failure remains in lineage. The mechanically repaired v0.2 reproduction then passed against all 15 source-native latent states within the prospectively frozen error thresholds.

The first generator analysis used a finite-difference derivative route and was refused under its frozen numerical-consistency rule. That refusal also remains. A P0-Q analytic-Jacobian repair was then independently qualified against complex-step differentiation without changing the biological model. The repaired generator passed, the stoichiometric dynamic subspace had dimension 8, every frozen context was fully observable through the deterministic FRET measurement, and at least one observable complex invariant factor existed in both source-defined parameter lanes under common FGF contexts. This established P0-Q transport of the **mode-specific `chi_bio` representation class**, not transport of one preferred numerical value.

The first nonlinear modal qualification, now **v1**, asked a broad question: whether the complete 8D linear generator reproduced local nonlinear dynamics when the system was perturbed along eight prospectively fixed source-stoichiometric directions spanning the dynamic subspace. Every FRET-visible complex-pair lane passed, but the full 8D all-direction gate failed in every context. The failures were structured. Columns 10 and 14 failed in all four lane/context combinations; columns 4, 6, and 12 failed conditionally. That result is frozen as `ERK_B3_LIMIT_MAP_V01.json`.

The v1 result means that complete local linear adequacy is **not uniform across arbitrary spanning reaction directions at the frozen perturbation scales**. It does not mean the analytic generator is wrong, because the derivative and source-model checks passed. It also does not permit dropping the failed directions or calling the result a pass.

After that limit was frozen, a new ERK modal P0-Q lineage was explicitly authorized. The v2 question was scientifically different and was frozen before its result: instead of arbitrary spanning directions, test the **actual invariant modal carriers** of the same qualified 8D generator. Every real mode was tested in both signs. Every complex-conjugate pair was tested across both signs of both frozen real-subspace basis directions. The same primary amplitude-convergence rule used in v1 was retained, and no carrier could be removed after viewing the result.

The v2 gate also failed overall. Across four source-defined lane/context combinations, **52 of 64 frozen directions passed** and **15 of 25 carrier-context records passed**. Real-mode carriers accounted for 10 of the 12 failed directions. Two complex-pair directions also failed, both in the high-FGF context. In the primary parameter lane at FGF 250, the pair with `chi_bio ~= 0.44686` failed only its frozen `PAIR_RE_MINUS` state-convergence rule. In the sensitivity lane at FGF 250, the pair with `chi_bio ~= 0.98384` failed the same frozen negative-real direction under both state and FRET convergence rules.

Several v2 failures occur at very small relative errors and worsen further at the 1e-5 sensitivity amplitude. That pattern is compatible with a numerical-floor, stiffness, or solver-tolerance interaction, but that interpretation does **not** change the frozen adjudication. Under the preregistered rule, those lanes fail. Demonstrating that they are numerical rather than biological would require a separate frozen numerical-resolution investigation and could not retroactively convert either v1 or v2 into a pass.

The lineage therefore closes with the following three-object disposition.

**`chi_bio`** transports at P0-Q as a **mode-specific scalar representation class** from NF-kB into the independent ERK B3 system. ERK does not reproduce one universal numerical value and was never required to. The ERK generator contains context-dependent observable complex factors, and the original v1 pair lanes passed local nonlinear qualification. The stronger v2 test shows that this local scalar family has an explicit directional nonlinear limit: not every direction spanning every complex invariant subspace satisfies the frozen convergence rule.

**`Chi_bio`** remains model-specific and admitted in NF-kB, but ERK does not earn full modal admission. ERK has a qualified generator-level modal precursor, yet the complete modal architecture is refused under both v1 and v2. v1 refuses uniform complete-8D adequacy across arbitrary reaction directions. v2 refuses uniform adequacy even when the test is restricted to all natural invariant modal carriers. These are complementary boundaries, not contradictory results.

**Bio Chi** remains model-specific and admitted in the NF-kB reference system. Cross-system Bio Chi transport into ERK is **not opened**, because the ERK modal layer did not earn admission. The hierarchy therefore behaves exactly as the GOM requires: scalar success does not force modal success, and modal failure is not averaged away by a successful scalar result.

The current scientific lesson is narrower than a universal biological stability law and stronger than a failed replication. In these two signaling systems, the generator-derived scalar construction is more portable than complete nonlinear modal closure. ERK demonstrates that local pole structure can remain meaningful while the higher-dimensional embedding introduces direction- and context-dependent limits. That boundary itself is part of the Bio Chi architecture.

## Immutable lineage spine

- Native source freeze: `BIO_CHI/config/BLUM_B3_TRANSPORT_SOURCE_FREEZE_v0_2.json`
- Native reproduction: `BIO_CHI/config/BLUM_B3_NATIVE_REPRODUCTION_V02_RESULT_PIN.json`
- Preserved generator v1 refusal: `BIO_CHI/config/BLUM_B3_GENERATOR_TRANSPORT_V01_RESULT_PIN.json`
- Qualified analytic generator: `BIO_CHI/config/BLUM_B3_GENERATOR_TRANSPORT_V02_RESULT_PIN.json`
- Modal round-trip v1: `BIO_CHI/config/BLUM_B3_LOCAL_NONLINEAR_ROUNDTRIP_V01_RESULT_PIN.json`
- v1 Limit Map: `BIO_CHI/config/ERK_B3_LIMIT_MAP_V01.json`
- Modal v2 freeze: `BIO_CHI/config/ERK_B3_INVARIANT_MODAL_V2_FREEZE_v0_1.json`
- Modal v2 result: `BIO_CHI/config/ERK_B3_INVARIANT_MODAL_V2_RESULT_PIN.json`
- Machine-readable complete lineage: `BIO_CHI/config/ERK_B3_MODAL_LINEAGE_V01.json`

No third ERK modal representation is opened in this cycle. Any future ERK modal work inherits explicit promotion debt from both v1 and v2 and must be justified independently of the desire to eliminate these failures.
