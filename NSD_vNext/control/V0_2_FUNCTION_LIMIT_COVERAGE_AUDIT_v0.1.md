# NSD v0.2 Function/Limit Coverage Audit v0.1

**Status:** PREFREEZE COVERAGE AUDIT / NO OUTCOMES OPENED  
**Governance:** SymC GOM v1.0 + Continuity Hardening Addendum  
**Source:** `FRESH_UNTOUCHED_V0_2_DRAFT.json`

## N-B1 balance

The draft contains 9 Function truth classes and 9 Limit truth classes. This is a designed qualification balance, not prevalence.

### Function coverage

| ID | Role | Primary channels stressed |
| --- | --- | --- |
| U2F0 | ordinary interior C | F, N, I, U |
| U2F1 | ordinary nonzero-g C | F, N, I, U |
| U2F2 | weak observation valid C | I, U, S |
| U2F3 | near-critical valid C | I, N, U |
| U2F4 | high-frequency valid C | S, I, U |
| U2F5 | low-damping valid C | I, N, U |
| U2F6 | positive-g valid C | F, N, I |
| U2F7 | negative-g valid C | F, N, I |
| U2F8 | benign observation-gain control | R plus ordinary C channels |

This preserves ordinary success regions and includes difficult-but-valid C truth so refusal behavior cannot be assessed only on easy cases.

### Limit coverage

| ID | Role | Primary refusal question |
| --- | --- | --- |
| U2L0 | D not C positive branch | semantic family |
| U2L1 | D not C negative branch | semantic family |
| U2L2 | scalar-positive not D positive | semantic family |
| U2L3 | scalar-positive not D negative | semantic family |
| U2L4 | colored memory | memory/closure |
| U2L5 | genuine two mode | order/multiplicity |
| U2L6 | piecewise C reorganization | stationarity/time variation |
| U2L7 | AR(1) nonoscillatory | zero-oscillator/nonoscillatory refusal |
| U2L8 | two-mode reference mixture | observation/reference plus multiplicity |

No single Limit class is allowed to stand in for all refusal mechanisms.

## N-B2/N-B3 coverage

The fresh draft retains distinct target families for autonomous initial-condition response, B-driven input response, C-observed response, and time-varying dynamics.

Required Function/Limit pairings remain:

- low-order sufficiency for asymptotic/modal targets;
- same local modes with altered embedded spectrum;
- same eigenvalues with altered non-normal finite-time response;
- same A with different B for input-dependent targets;
- same A/B with different C for observation-dependent targets;
- similarity-related realizations with transformed physical metric;
- time-varying operator truth versus declared stationary comparator;
- partial-observation/sampling and misspecification challenges.

## Coverage disposition

No prefreeze imbalance requiring a scientific redesign is identified. The draft is suitable for Round-2 APQ review, but this audit does not freeze the packet or authorize execution. Any Round-2 objection may require prospective revision.
