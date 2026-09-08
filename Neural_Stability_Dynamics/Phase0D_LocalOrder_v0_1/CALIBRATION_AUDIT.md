# Phase 0D Development Calibration Audit

This is development evidence only. It does not rescore Phase 0C and is not the Phase 0D holdout.

## Phase 0C failure mechanism reproduced

Using the frozen Phase 0C generator, seed, noise realizations, and singular-gap order rule:

- global-timescale challenge: q_full=8 in 9/9; q_first=q_second=4 in 9/9
- observation-map challenge: q_full=8 in 9/9; q_first=q_second=4 in 9/9
- structural challenge: q_full=6 in 9/9; q_first=q_second=4 in 9/9

This confirmed that Phase 0C's full-order-on-halves evaluator overfit local segments.

## Local-order diagnostic

With local q=4 in the same already-seen Phase 0C challenge data:

- global timescale: scalar pole distance ~0.198-0.200; median carrier MAC >=0.99994; whole-subspace similarity >=0.99994; relational geometry <=0.00437
- observation switch: scalar pole distance <=0.00180; median carrier MAC ~0.116-0.362; whole-subspace similarity ~0.156-0.415
- structural switch: scalar pole distance ~0.0789-0.0819; median carrier MAC >=0.99990; whole-subspace similarity >=0.99994; relational geometry ~0.210-0.222

## Phase 0D selector calibration on already-seen Phase 0C systems

After implementing independent local order, MAC/subspace carrier matching, crowding-aware system geometry, and unresolved single-cluster geometry:

- global timescale expected behavior: 9/9 scalar, 9/9 modal, 9/9 system
- observation switch expected behavior: 9/9 scalar, 9/9 modal, 9/9 system
- structural switch expected behavior: 9/9 scalar, 9/9 modal, 9/9 system
- 1/f null expected behavior: 27/27 scalar, 27/27 modal, 27/27 system
- stationary scalar admission: 213/216 = 0.986111
- stationary modal admission: 213/216 = 0.986111
- stationary system admission among Phase 0C system-scored trials: 175/189 = 0.925926

These numbers are calibration only because Phase 0C has already been observed. They justify freezing the new architecture but cannot admit it.

The actual admission test is the new untouched Phase 0D configuration with seed `202609081703` and new synthetic system parameters.
