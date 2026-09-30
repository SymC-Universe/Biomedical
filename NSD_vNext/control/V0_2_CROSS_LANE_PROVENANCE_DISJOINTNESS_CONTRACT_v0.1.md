# NSD v0.2 Cross-Lane Provenance Disjointness Contract v0.1

**Status:** PREFREEZE / REQUIRED BEFORE FINAL CASE FREEZE  
**Governance:** SymC GOM v1.0 + Continuity Hardening Addendum

Final N-B1 and N-B2/N-B3 confirmatory cases must be disjoint by scientific ancestry, not merely by case label. The final provenance graph for every case must record source case, generator instance, template identity, seed or deterministic identity, parameter draw, observation/input transform ancestry, and any derived or matched variant.

A final case is cross-lane non-disjoint if its scientific ancestry overlaps another lane in a way that would allow one lane's confirmatory result to inform the other's confirmatory case. Label changes do not repair such overlap.

Shared software libraries, numerical kernels, or mathematical identities may be common across lanes only when they are listed in the common-dependency register and independently verified for the roles they serve. Shared implementation is not evidence of independent confirmation.

Before final freeze, an outcome-blind audit must construct the cross-lane ancestry graph and return PASS only when the final case sets are scientifically disjoint under this contract. Any unresolved ancestry returns NEED_MORE_INFO and blocks final packet freeze.

This contract does not alter lane-specific scientific targets and grants no execution authority.
