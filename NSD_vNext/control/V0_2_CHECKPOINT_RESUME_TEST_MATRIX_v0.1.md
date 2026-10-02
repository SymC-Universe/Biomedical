# NSD v0.2 Checkpoint and Resume Identity Test Matrix v0.1

Status: PREFREEZE MECHANICAL DESIGN / NO EXECUTION AUTHORITY.

The final implementation must test these identity changes before substantive execution: authority plan, packet/config, code manifest, dependency lock, environment identity, RNG/seed identity when applicable, expected case-set digest, output-schema identity, completed artifact hashes, duplicate or conflicting case IDs, cross-lane ID overlap, stale checkpoints, and recovery-path information access.

For every identity mismatch, resume must stop with FROZEN_CONTRACT_VIOLATION. Missing or hash-invalid completed artifacts return only the affected case to incomplete status under the same frozen scientific identity. A valid unfavorable, null, or outlying scientific result is preserved and does not by itself stop or retune execution. The recoverability path must fail implementation tests if it can read hidden exact descriptors. Output schemas must reject automated scientific PASS/rank/combined-lane verdict fields. A valid terminal run stops at SCIENTIFIC_REVIEW_READY.

These are implementation contracts, not scientific thresholds.
