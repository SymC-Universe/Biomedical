# NSD v0.2 N-B2/N-B3 Switched Certification Implementation Spec v0.1

**Status:** POST-FREEZE MECHANICAL IMPLEMENTATION SPEC  
**Scientific baseline:** `NSD-V02-B01-FROZEN`  
**Execution authority:** false

This record translates already-frozen N-B2/N-B3 packet requirements into an implementation task. It does not change the scientific packet, target, tolerance, operator, switching law, or claim ceiling.

## Frozen target

For the switched truth, report

\[
D(t)=\left\|\Phi(t,0)-e^{\bar A t}\right\|_2,
\]

where \(\Phi(t,0)\) is the chronological right-continuous propagator under the frozen switching law and \(\bar A\) is the frozen period-time-weighted mean operator.

The implementation must retain both the declared evaluation-schedule curve and a certified enclosure of

\[
\max_{0\le t\le 32}D(t).
\]

## Production certificate

The production route must partition \([0,32]\) at every frozen switch boundary. Within a switch-free interval \([a,b]\), with active generator \(A_i\), use a conservative interval upper bound derived from

\[
\Phi'(t)=A_i\Phi(t),\qquad
\frac{d}{dt}e^{\bar A t}=\bar A e^{\bar A t}.
\]

A valid implementation may use the matrix logarithmic-norm bound

\[
\|\Phi(t)\|_2\le
\exp(\max(0,\mu_2(A_i))(t-a))\|\Phi(a)\|_2
\]

and the analogous bound for \(e^{\bar A t}\). This yields a uniform interval Lipschitz bound for \(D(t)\). Endpoint cones may then upper-bound the interval maximum. Subdivide until

\[
U-L\le 10^{-9}\max(1,|L|),
\]

matching the frozen peak-enclosure tolerance. Retain all non-pruned argmax intervals whose upper bound overlaps the frozen tie criterion.

No scientific PASS/REFUSE verdict is produced by this routine.

## Independent reference route

A separate verifier must use an independently implemented dense/high-precision route on non-confirmatory fixtures, with analytic anchors where available. The reference path must not call the production optimization/certification routine. It must verify that dense/reference maxima lie inside the production enclosure and that zero-discrepancy anchors return zero within numerical tolerance.

This verifier is mechanical qualification only and must not inspect the frozen confirmatory suite outcomes.

## Required test coverage

- identical switched generators give zero discrepancy;
- switch boundaries are explicit partition boundaries;
- nontrivial fixture dense/reference maximum is enclosed by the production certificate;
- interval budget exhaustion fails closed;
- returned evidence namespace is numerical only;
- no representation-sufficiency or recoverability verdict is encoded.

## Current transport status

Two repository code-mutation attempts for the switched-discrepancy implementation were rejected by the connector safety layer during the current controller cycle. The scientific specification is unchanged. Retry the code mutation later; do not weaken or replace the frozen certificate to bypass the infrastructure block.
