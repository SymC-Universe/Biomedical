# GRI <-> Bio Chi B1 calibration re-entry checkpoint

**Date:** 25 September 2026
**Branch:** `gri-biochi-bridge-p0q-20260925`
**Status:** ACTIVE P0-Q / B1 TARGETED SOURCE SEARCH
**Authority:** SymC GOM v0.8.6 + GRI project guardrails + existing GRI <-> Bio Chi bridge freeze.

## TASK_ID
`GRI_BIOCHI_B1_STATIC_TO_NATIVE_DYNAMICS_20260925`

## AUTHORITATIVE_INPUTS
- `BIO_CHI/config/GRI_BIOCHI_BRIDGE_FREEZE_v0_1.json`
- `BIO_CHI/config/GRI_BIOCHI_BRIDGE_FEASIBILITY_V01_RESULT_PIN.json`
- `BIO_CHI/control/GRI_BIOCHI_BRIDGE_CHECKPOINT_20260925.md`
- `BIO_CHI/control/HARMANGE_DIRECT_BRIDGE_SOURCE_REFUSAL_20260925.md`
- `BIO_CHI/control/SHAFFER2017_BRIDGE_DESIGN_CHECKPOINT_20260925.md`
- `BIO_CHI/control/SHAFFER2017_PREANALYSIS_METHOD_DECISION_PACKET_20260925.md`
- BioSystems submission main/SI are frozen as manuscript targets and are not edited by this source-search checkpoint.

## COMPLETED_VERIFIED_STATE
1. The historical cross-sectional RNA quantity `chi_GRI = sigma/(2 mu) = CV/2` remains an operational fluctuation-to-signal/stability proxy. Static TCGA does not uniquely identify `omega` or `gamma`.
2. The original direct proportional identifications `mu -> omega` and `sigma -> gamma` are not licensed by static TCGA alone. This is an identifiability ceiling, not a universal falsification of every calibrated static-to-dynamic relationship.
3. Su M397 provides source-native dynamical eigenstructure but is dependent-only for bridge qualification. Scalar `chi_bio` is refused under frozen eigenvalue-class uncertainty; modal `Chi_bio` remains model-specific.
4. The outcome-blind bridge feasibility audit found no external B1 scalar candidate among then-qualified systems.
5. Harmange is refused for direct same-carrier bridge at the current reproducibility level because the required lineage carrier cannot be materialized from the released lightweight objects.
6. Shaffer passed source qualification for B2/B3 development/internal validation, but no B1 scalar has been licensed there and B2/B3 molecular outcomes remain unopened.

## OPEN_ISSUES
- Find a cancer/oncology system with both:
  1. same-carrier transcriptomic measurements sufficient to compute a frozen GRI-compatible static proxy before or independently of the dynamical target; and
  2. a source-native, independently identified dynamical scalar or generator with a robust complex carrier and explicit uncertainty.
- Determine whether a direct scalar calibration is scientifically identifiable at all, or whether only modal/relational calibration is defensible.
- Preserve a null outcome: no qualifying B1 source is an admissible scientific result and must not trigger proxy redefinition.

## B1 QUESTION
Does frozen pre-outcome GRI-compatible static organization, including but not limited to historical `chi_GRI`, predict or calibrate an independently licensed dynamical coordinate on the same biological carrier beyond simple/native descriptors and relevant RNA mean-variance/composition controls?

## NONNEGOTIABLE FIREWALL
- Do not define `omega` from mean RNA abundance.
- Do not define `gamma` from across-sample RNA SD.
- Do not use the dynamic outcome to select genes, thresholds, representations, or carriers.
- Do not use `chi=1` as a rescue target.
- Do not promote same-publication development/internal validation to external confirmation.
- Refusal remains valid if no robust scalar carrier exists.

## CHECKPOINT CONTRACT
`CHECKPOINT_UNIT | candidate-source adjudication`
`CHECKPOINT_CADENCE | after every source qualification/refusal and before any target outcome is opened`
`RESUME_KEY | GRI_BIOCHI_B1_STATIC_TO_NATIVE_DYNAMICS_20260925`
`ATOMIC_OUTPUT | source identity + carrier map + eligibility/refusal + next action`
`DUPLICATE_GUARD | DOI/accession/source-lineage identity`
`MAX_RECOVERY_LOSS | one candidate-source adjudication`

## NEXT_EXACT_ACTION
Run a targeted literature/source search for cancer systems exposing same-carrier transcriptomic state plus independently identifiable relaxation/oscillation/generator dynamics. Rank candidates by source materializability and B1 identifiability only; do not inspect target effect direction before a candidate-specific freeze.

## SAFE_RESUME_POINT
This checkpoint.

## SCIENTIFIC_STATE_CHANGED
No. This checkpoint narrows the unresolved B1 question and records the source-search gate; it creates no supporting result.
