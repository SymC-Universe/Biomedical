# Bio Chi rapid checkpoint - Blum B3 native reproduction repair

**Branch:** bio-chi-closure-p0q-20260924

## Preserved v0.1 failure
Workflow run: 36058688918
Disposition: MECHANICAL_PRE_RESULT_TIME_GRID_ASSERTION_FAILURE

Exact source hashes passed. The ODE solver did not execute and no source trajectory values were compared. The failure arose because the frozen source contract expected 0 to 180 min / 91 points, while the exact NaClO3 sim_times.txt source is 0 to 178 min / 90 points.

## Frozen repair
BIO_CHI/config/BLUM_B3_TRANSPORT_SOURCE_FREEZE_v0_2.json

Only repaired:
- endpoint 180 -> 178 min
- count 91 -> 90 points

Unchanged:
- B3 topology
- source commit/tree/blob identities
- primary and sensitivity parameter roles
- ODE equations
- initial-state rule
- sustained FGF2 = 2.5
- BDF solver and tolerances
- max-absolute and RMS pass thresholds
- future stoichiometric-subspace generator rule

## Active rerun
Workflow: Bio Chi Blum B3 native reproduction P0-Q v0.2
Run: 36058880837
Status at checkpoint: in progress

No ERK spectrum or chi-like quantity has been opened.
