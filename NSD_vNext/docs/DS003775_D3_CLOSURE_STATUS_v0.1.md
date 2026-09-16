# ds003775 D3 Metadata/Join Closure Status v0.1

Date: 16 September 2026
Status: ACTIVE CLOSURE CONTROLLER
Dataset: OpenNeuro `ds003775`

## 1. Goal

Promote `ds003775` from `D2_HIERARCHY_VERIFIED` to `D3_METADATA_JOIN_VERIFIED` without allowing cognitive outcomes or demographic covariates to influence Structural Engine construction.

## 2. Completed

- D2 subject/session hierarchy reconciled: 111 subjects, 153 sessions, 42 repeat-session subjects.
- `participants.tsv` column roles reviewed.
- Machine-readable role manifest frozen at:
  - `docs/manifests/ds003775_metadata_roles_v0.1.json`
- Structural Engine participant-table visibility restricted to `participant_id`.
- `age` and `sex` classified downstream as demographic covariates.
- RAVLT, digit-span, trail-making, color-word, and verbal-fluency variables classified downstream as cognitive/clinical outcomes.
- CI regression test added to reject accidental cognitive-outcome leakage into the Structural Engine.

## 3. Remaining D3 blockers

D3 is **not yet promoted**. Closure still requires:

1. machine-audited one-to-one participant-table to BIDS-subject join cardinality on the pinned release;
2. explicit unmatched/ambiguous-record count artifact;
3. metadata missingness summary for every reviewed participant-table column;
4. canonical hash of the reviewed role manifest in the D3 closure artifact;
5. confirmation that BIDS recording-state/acquisition fields used by the Engine are explicitly enumerated and role-licensed;
6. regression test that any unreviewed metadata column remains non-admitted until assigned a reviewed role.

## 4. D3 promotion condition

Promote only if all of the following are true:

```text
participant_to_bids_join_cardinality == one_to_one
unmatched_participants == 0
unmatched_bids_subjects == 0
ambiguous_joins == 0
all_task_columns_have_reviewed_roles == true
engine_visible_participant_columns == [participant_id]
manifest_hash_recorded == true
```

If any condition fails, retain D3 as blocked/quarantined and record the failure rather than repairing it silently.

## 5. D4 interaction

D4 signal-payload verification may proceed mechanically in parallel where identity is independently pinned, but D5 analysis-ready status cannot be granted until both D3 and D4 close.

The existing D4 pilot/repeat workflows therefore remain useful while this D3 closure is completed.

## 6. Why this matters for the eventual tool

The future assessment/diagnostic tool must be able to prove that structural features were built without seeing cognition, diagnosis, symptom scores, or demographics that could leak target information into the representation layer.

D3 is therefore part of the clinical-tool evidence chain, not mere dataset housekeeping.
