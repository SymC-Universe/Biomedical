# ds003775 D3 Metadata/Join Closure Status v0.1

Date opened: 16 September 2026
Status: CLOSED / SUPERSEDED BY VERIFIED PROMOTION
Dataset: OpenNeuro `ds003775`

## 1. Closure decision

The D3 metadata/join gate is now closed for the frozen T0 healthy-qualification scope.

Authoritative promotion record:

`docs/D3_DS003775_PROMOTION_v0.1.md`

Decision:

`ds003775 -> D3_METADATA_JOIN_VERIFIED (T0 scope)`

This file is retained only as the historical closure controller so that the previously open blockers remain traceable.

## 2. Previously open blockers and disposition

1. participant-table to BIDS-subject join cardinality -> **CLOSED**
2. unmatched/ambiguous record artifact -> **CLOSED**
3. metadata missingness summary -> **CLOSED**
4. canonical role-manifest hash -> **CLOSED**
5. Engine-visible recording-state/acquisition field enumeration -> **CLOSED FOR T0 SCOPE**
6. unreviewed-column non-admission regression control -> **CLOSED**

The versioned machine-readable role manifest and the D3 audit tooling preserve the label-blind Engine firewall.

## 3. Current D3 invariants

```text
participant_to_bids_join_cardinality == one_to_one
unmatched_participants == 0
unmatched_bids_subjects == 0
ambiguous_joins == 0
all_task_columns_have_reviewed_roles == true
engine_visible_participant_columns == [participant_id]
manifest_hash_recorded == true
```

Age, sex, and cognitive outcomes remain downstream-only for the frozen T0 structural-qualification task.

## 4. Current downstream gate

D3 no longer blocks T0.

The current dataset gate is D4/D5:

- D4 pilot payload identity/readability: verified previously;
- D4 real repeat-pair identity/readability: scientifically verified previously, with current CI workflow regression under mechanical repair after an import/dependency-surface change;
- D4 dataset-wide expansion: open;
- D5 analysis-ready promotion: open.

A later workflow regression does not revoke the underlying pinned payload evidence unless the re-run exposes a scientific mismatch. Mechanical workflow failures are tracked and repaired separately.

## 5. Why this matters

The future decision-support tool must preserve proof that structural features were built without cognition, diagnosis, symptom scores, or demographic outcome leakage.

D3 is therefore part of the tool evidence chain and is now closed for the declared T0 scope.
