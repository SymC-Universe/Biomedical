# NSD v0.2 Generator and Provenance Validation Plan v0.1

**Status:** PREFREEZE / OUTCOME-BLIND / NO EXECUTION AUTHORITY  
**Governance:** SymC GOM v1.0 + Continuity Hardening Addendum

This stage runs before any scientific outcome adjudication and may inspect only frozen generator/config identities and analytically expected relationships.

## N-B1 checks

- truth ID, generator name, parameter tuple, seed, duration, rate, and observation-transform identity match the final packet;
- every C-member truth uses only the final frozen C generator or a prospectively proven preserving observation transform;
- D-not-C, S-not-D, colored-memory, multimode, nonoscillatory, time-reorganized, and non-preserving observation/reference truths are labeled exactly as frozen;
- same-path paired-rate construction and alias-safety conditions match the packet;
- no v0.1 result payload is referenced.

## N-B2/N-B3 checks

- each A/B/C/x0/G object matches the frozen packet;
- every declared held-fixed relationship is verified before target computation;
- same-spectrum controls have the prospectively required eigenvalue identity;
- same-A/different-B and same-A,B/different-C controls change only the declared operator;
- similarity cases satisfy the frozen A, B, C, G, and x0 transformation identities;
- switching order, phase, segment duration, continuity, and surrogate construction match the frozen packet;
- sampling projections and the deterministic observation contract match the packet;
- all N-B1 and N-B2/N-B3 confirmatory case IDs are disjoint.

## Identity checks

The validator binds protocol, packet/config, code/dependencies, environment, RNG/seed state where applicable, expected case IDs, and output schema. Any mismatch is DATA_CONTRACT_REFUSAL or FROZEN_CONTRACT_VIOLATION according to stage.

The validator may not inspect fitted scientific outcomes to repair a contract, choose a threshold, rank representations, or alter the frozen science. Failure stops the affected execution before scientific evaluation.
