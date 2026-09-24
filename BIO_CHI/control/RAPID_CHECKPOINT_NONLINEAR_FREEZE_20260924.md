# Bio Chi rapid checkpoint - nonlinear round-trip frozen

**Branch:** bio-chi-closure-p0q-20260924

## Current durable state
- chi_bio model-specific P0-Q scalar: SUPPORTED and pinned.
- local observability through free nuclear NF-kB: PASS and pinned.
- source-native pulse regime audit: mixed TR=1/TR=0 pulse protocols excluded as clean tests of the TR=1 equilibrium pole.
- nonlinear round-trip gate frozen and source hash mechanically corrected before execution.

Freeze:
BIO_CHI/config/JARUS_LOCAL_NONLINEAR_ROUNDTRIP_FREEZE_v0_1.json

Correct local-stability source artifact:
- artifact 10748186325
- SHA-256 7b17c4b2ec5c3cfd280eac48155903f329a57a1a62e4918ef4fcac4ed3aea7a9

## Next single gate
Execute:
1. complex-pair local nonlinear convergence;
2. complete six-state linear-vs-nonlinear convergence;
3. pair analytic vs full-linear implementation self-check;
4. single-real-pole refusal control.

No downstream Chi_bio or Bio Chi promotion is opened until this gate is pinned.

No user intervention required.
