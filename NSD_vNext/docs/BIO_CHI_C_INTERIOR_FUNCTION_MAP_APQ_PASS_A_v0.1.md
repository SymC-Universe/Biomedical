# Bio Chi Function Map APQ First Pass A v0.1

**APQ level:** APQ-2 SUBSTANTIAL  
**Review lens:** domain validity, novelty, interpretation, alternative biological explanations  
**Plan reviewed:** `BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_PACKET_v0.1.md` at commit `673bbd477d87819165a0740426ee5619f0b30575`  
**Isolation statement:** this pass was produced from the frozen Plan Packet without access to another APQ review conclusion. It is role-isolated but not independently cognized.

## 1. Strongest justified feature

The plan correctly separates a synthetic estimator Function Map from biological validation. It does not use successful recovery inside the generating family as evidence that real neural or other biological dynamics belong to C, and it keeps previously mapped Limit cases visible rather than treating the Function Map as a success-only narrative.

## 2. Strongest scientific assumption

The strongest assumption is that mapping the underdamped C interior is the right next residual question after P0-N. The literature establishes many biological regimes that are not reducible to one damped second-order mode. The plan is valid only if it remains an estimator/representation qualification map and does not silently become a claim that C is biologically typical.

## 3. Most likely failure mode

The map may look strong because the simulator and C1Q fit the same model family. A successful map can therefore become an elaborate self-consistency result rather than evidence that the estimator is robustly recovering information from finite observations.

## 4. Most dangerous hidden dependency

Simulator and estimator share the same continuous-time C parameterization and mathematical identities. A coding or structural assumption shared by both could make recovery look better than it would under a differently parameterized but observationally equivalent estimator.

## 5. Plausible competing explanation

If C1Q recovery varies across the envelope, the pattern may reflect optimizer geometry, finite-sample covariance conditioning, or observation-noise information rather than a scientifically meaningful boundary in biological modal stability.

## 6. Circularity / leakage / provenance concern

The parameter envelope is informed by the existing qualification history, and earlier C1Q outcomes are known. The new Sobol cells avoid exact prior reference cells, which is appropriate for exploratory mapping, but the plan must not describe them as untouched confirmation.

## 7. Missing control / comparator

A cheap independent pole-recovery diagnostic is missing. The map should include a generic second-order covariance-recurrence pole estimate or other non-C1Q parameterization on the same signals. It need not be promoted as an estimator; its purpose is to distinguish "information about the pole is absent" from "C1Q optimization/parameterization failed."

## 8. Cheaper / cleaner discriminating test

Before the full 16-cell map, run the four-cell mechanical pilot and calculate the generic positive-lag second-order recurrence pole estimate alongside C1Q. If the generic diagnostic fails on the same low-information cells, that supports an information/conditioning explanation. If it recovers the pole while C1Q fails, the problem is estimator-specific and the full map should preserve that distinction.

## 9. Refusal condition

Refuse any interpretation that a cell demonstrates biological applicability. Refuse a C1Q-specific scientific interpretation when the generic pole diagnostic and C1Q disagree materially and the discrepancy cannot be assigned to known finite-sample conditioning without further qualification.

## 10. Objection classification

- **A1 MATERIAL:** shared-family self-consistency can masquerade as estimator validation.
- **A2 MATERIAL:** absence of an independent pole-recovery diagnostic prevents clean attribution of recovery failures.
- **A3 MINOR:** the synthetic envelope is not biologically representative and must retain that label everywhere.
