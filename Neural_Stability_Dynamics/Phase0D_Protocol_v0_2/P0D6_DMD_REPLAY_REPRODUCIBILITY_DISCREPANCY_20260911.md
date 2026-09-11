# P0-D6 Subspace-DMD Frozen-Replay Reproducibility Discrepancy

Date: 2026-09-11
Status: **FORENSIC P0-D REPRODUCIBILITY DEBT. P0Q1 FROZEN RESULT UNCHANGED. SYSTEM MODEL LOCK UNAFFECTED.**

## Frozen source-of-record result

The original prospective P0Q1 artifact remains the authoritative result for that frozen qualification execution:

- SSI-COV: `SURVIVES_P0Q1`;
- Subspace DMD: `FAILS_P0Q1`;
- real-pole-only family: `2/5` false admissions in the frozen result;
- zero mechanical exceptions reported in the original P0Q1 execution.

Artifact SHA-256: `1bfdb57ce0a9aceec1df8aa7a4968a1ae18bfa7297b557c2a2b0cad8444a00b7`.

The frozen result is not rescored from a later replay.

## P0-D6 replay result

A later retrospective diagnosis regenerated the same declared real-pole family using the current branch code and frozen seed/configuration source. It did **not** reproduce the original per-replicate decision pattern exactly.

Replay outcomes at selected rank 4:

- replicate 0: false complex structure + unstable pole -> `REFUSE_UNSTABLE_SELECTED_POLE`;
- replicate 1: stable false complex structure -> `ADMIT_RANK_SIGNAL`;
- replicate 2: `METHOD_EXCEPTION_PRESERVED` -> `REFUSE_METHOD_EXCEPTION`;
- replicate 3: false complex structure + unstable pole -> `REFUSE_UNSTABLE_SELECTED_POLE`;
- replicate 4: false complex structure + unstable pole -> `REFUSE_UNSTABLE_SELECTED_POLE`.

Thus the replay produced one false admission plus one method exception rather than the frozen run's two false admissions and zero exceptions.

Replay run: `34566576823`
Replay artifact SHA-256: `5db1ca67ff27662a20907484397e1315d83ebc7f806a66a69b6892ec49853d6c`.

## Interpretation

This discrepancy does **not** rescue Subspace DMD. Both executions independently show that the method/rank construction is not qualified on the real-pole-only family. The failure mechanism remains centered on over-rank numerical behavior that can create false complex structure, instability, or an exception in a system whose truth contains only stable real poles.

However, the discrepancy means the present implementation is not yet sufficiently reproducible at the exact per-replicate numerical-outcome level to support a stronger mechanistic statement about the frequency of each failure subtype.

## Required forensic work

Before any revised Subspace-DMD qualification or final comparator freeze:

1. compare the exact original and replay dependency/environment identities;
2. verify NumPy/SciPy/LAPACK/BLAS and Python versions for the frozen P0Q1 run versus replay;
3. compare generated input matrices/data hashes per replicate if recoverable;
4. distinguish deterministic-data mismatch from eigensolver/SVD numerical sensitivity;
5. preserve the original artifact as source of record;
6. do not tune a repair against these five records;
7. if Subspace DMD remains a comparator candidate, qualify the final implementation/version on new untouched evidence.

## System Model consequence

None. The discrepancy is already representable by the locked open-channel objects:

- estimator disagreement;
- method exception;
- failed/unstable fit;
- reproducibility status;
- unresolved method-specific mechanism.

No System Model v1.0 object or logical relation needs revision.

## Atlas consequence

The Atlas may record method identity and method-specific reliability/uncertainty context, but these replay records are not Atlas population coordinates and must not be used to define biological reference zones.
