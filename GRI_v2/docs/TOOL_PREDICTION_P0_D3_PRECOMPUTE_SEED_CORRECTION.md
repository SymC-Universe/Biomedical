# P0 D3 pre-compute seed-lineage correction

**STATUS: FROZEN BEFORE ANY D3 CROSS-LAYER DISCOVERY RESULT IS COMPUTED**

Date: 2026-08-30

This note corrects one implementation-lineage detail in `TOOL_PREDICTION_P0_D3_DISCOVERY_AUDIT_MODEL_FREEZE.md` before D3 real cross-layer results exist.

The D3 freeze correctly requires 39 deterministic null permutations and reuses the F2-calibrated audit primitives, but its first draft described a new little-endian seed conversion. That is unnecessarily different from the already-established F2 kernel and is therefore superseded here before execution.

D3 nulls MUST use the existing F2 `stable_seed` algorithm exactly:

1. construct the payload by joining `[namespace, *parts]` with literal `|`;
2. SHA-256 the UTF-8 payload;
3. interpret the first 8 digest bytes as an unsigned **big-endian** integer;
4. reduce modulo `2**32`.

D3 namespace:

`GRI_V2_PREDICTION_P0_20260830|D3`

Parts are the stable analysis tag, cancer, technical/layer tag, and zero-based permutation index as applicable.

The P1 CV-fold rule remains separately frozen as the first 8 SHA-256 bytes of `GRI_V2_PREDICTION_P0_20260830|CV|<cancer>|<participant_root>`, unsigned big-endian, modulo 5.

This correction is provenance-preserving and result-independent. It changes no null count, threshold, endpoint, state rule, feature, participant, or interpretation. No D3 real-data cross-layer statistic had been computed when this correction was made.
