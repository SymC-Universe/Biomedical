# P0-D8 Subspace-DMD Tail-Gap Forensics Plan

Date: 2026-09-11
Status: P0-D RETROSPECTIVE/MECHANISM MAPPING. NOT P0-Q. NOT P1.
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum

## Motivation

Frozen P0Q1 remains unchanged: SSI-COV SURVIVES_P0Q1 and Subspace DMD FAILS_P0Q1. A later unchanged-source/config replay of the real-pole family did not reproduce the frozen per-replicate pattern exactly, even under the same pinned Python/NumPy/SciPy versions and runner image. The historical result must remain frozen.

Inspection of the rank-sweep architecture exposes a plausible mechanism that can be tested without repairing the failed gate: the P0Q1 candidate is the rank with the largest finite adjacent singular-value ratio. A very large ratio can occur after the dominant dynamically supported singular spectrum, inside finite-sample stochastic tail directions. If an over-rank fit is then numerically admissible, those tail directions may generate unstable or false complex poles.

Therefore the P0-D hypothesis is:

**largest singular gap != supported dynamic rank when the largest gap occurs in a weak stochastic/numerical tail.**

## Design

Use synthetic systems with known low-dimensional structure and vary record length while preserving the current Subspace-DMD implementation.

Families:

1. two stable real poles (-0.7, -2.4), no oscillatory truth;
2. one stable oscillatory pair (decay 0.7, frequency 5 Hz).

Record lengths:

- 1300
- 2600
- 5200
- 10400 samples

Replicates: 16 per family/length.

For each record, capture the projected-future singular spectrum and for candidate ranks 1..8:

- singular value s_r;
- normalized support s_r / s_1;
- next support s_(r+1) / s_1;
- adjacent gap s_r / s_(r+1) using the existing diagnostic definition;
- fixed-rank fit status;
- stable/unstable pole counts;
- positive-frequency complex pole counts;
- candidate decision under the already-frozen P0Q1 rule as a **non-independent retrospective overlay only**.

For synthetic diagnosis only, record whether the selected candidate rank exceeds the known continuous-time state dimension.

## Questions

1. Does the largest-gap rank systematically move into weak tail directions?
2. Are false complex poles concentrated in over-rank tail selections?
3. Does increasing record length shrink the normalized support of the offending tail even when its adjacent gap remains large?
4. Is the frozen gate sensitive to tiny tail-spectrum changes that leave the dominant supported spectrum essentially unchanged?
5. Does the same phenomenon occur in a genuinely oscillatory low-rank system, or is it specific to refusal-family structure?

## Nonclaims

- P0Q1 is not rescored or repaired.
- No new support-floor threshold is selected.
- Known truth is used only for P0-D mechanism diagnosis, never as selector input.
- No method superiority claim is made.
- Any revised Subspace-DMD rank rule requires a new version and untouched P0-Q qualification.

## Reproducibility hardening implication

If tail sensitivity is confirmed, future prospective synthetic qualification should archive the decisive generated input arrays or cryptographic hashes in addition to seed/config/code identity. Seeds plus source versions may be insufficient to guarantee bitwise replay of near-singular linear-algebra cases across hardware/backends.