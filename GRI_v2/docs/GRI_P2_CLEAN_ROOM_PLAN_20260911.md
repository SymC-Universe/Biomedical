# GRI P2 clean-room qualification plan

**Date:** 2026-09-11  
**Status:** PREPARATION ONLY  
**Protocol:** v0.7.1 Sections 27, 32-34, 51 + v0.7.1A

## Purpose

Prepare the exact release-grade reproduction sequence that a future consolidated GRI Engine must pass before P2 qualification. No current result is promoted by this plan.

## Preconditions

Clean-room execution begins only after:

1. post-C1 sensitivity is dispositioned;
2. supported System Model scope is frozen;
3. production Engine entry point exists;
4. release input/output/refusal schemas are frozen;
5. release dependencies and seed namespace are frozen;
6. release manifest and semantic capability registry are generated;
7. Atlas version is supplied only when testing Tool-level behavior.

## Clean-room sequence

### CR1 Release acquisition
- obtain exact tagged commit/archive;
- verify archive/file hashes before execution;
- verify semantic manifest fields before execution.

### CR2 Fresh environment
- new Python/R environment as applicable;
- install only declared dependencies;
- capture OS, interpreter, package versions, CPU/BLAS information where material;
- fail on undeclared local-only dependency.

### CR3 Hidden-state exclusion
- no old `WORKING_STATE`;
- no old cache unless the test explicitly verifies immutable frozen-parent reuse;
- no precomputed results accepted as a substitute for regeneration where regeneration is claimed;
- user-specific absolute paths prohibited from the release interface.

### CR4 Known-truth qualification
- execute full production-path known-truth suite;
- execute known-bad/refusal suite;
- confirm checks actually fail when the guarded property is violated.

### CR5 Mutation qualification
- apply declared temporary mutations;
- prove at least one required test fails per mutation family;
- restore pristine release and reverify hashes.

### CR6 Real-data non-confirmatory reproduction
- acquire/mount one authoritative real-data benchmark or frozen parent state;
- verify source identity before preprocessing;
- regenerate declared outputs through production Engine;
- compare scientific quantities to frozen expected numerical/semantic tolerances.

### CR7 Resume/interruption
- interrupt after valid checkpoint;
- resume and compare to uninterrupted output;
- corrupt checkpoint and verify refusal;
- alter input hash and verify checkpoint rejection;
- ensure no duplicated/skipped analysis units.

### CR8 Atlas interface, if Tool-level release
- load explicit Atlas version/hash;
- verify Engine core output can be produced without Atlas tuning;
- query Atlas read-only;
- verify non-independent rows cannot satisfy independent-validation state;
- verify `NO_ATLAS_MATCH` is legal.

### CR9 Function/Limit output
- ensure Function Map and Limit Map fields are both present where applicable;
- verify `WORKS_HERE`, `STOPS_WORKING_HERE`, `NOT_KNOWN_HERE` are emitted through deterministic rules;
- verify one map cannot overwrite the other.

### CR10 Final release verification
- rebuild outputs/package;
- hash shipped artifacts;
- run semantic validator against the shipped archive, not build temporaries;
- extract archive into a second clean directory;
- rerun test/validation suite;
- archive clean-room transcript and environment metadata.

## Required evidence bundle

A successful P2 clean-room record should contain:

- `RELEASE_MANIFEST.json`
- `SEMANTIC_MANIFEST.json`
- `ENVIRONMENT_LOCK.*`
- `CLEAN_ROOM_RUN_LOG.txt`
- `KNOWN_TRUTH_RESULTS.json`
- `NEGATIVE_REFUSAL_RESULTS.json`
- `MUTATION_TEST_RESULTS.json`
- `REPEATABILITY_RESULTS.json`
- `RESUME_TEST_RESULTS.json`
- `REAL_DATA_BENCHMARK_RESULTS.json`
- `ATLAS_INTERFACE_RESULTS.json` when applicable
- `FUNCTION_LIMIT_OUTPUT_RESULTS.json`
- `OUTPUT_SHA256.json`
- `P2_QUALIFICATION_SUMMARY.json`

## Failure handling

Mechanical failure -> repair only if frozen scientific meaning is unchanged, then restart the failed release qualification step with provenance.

Science-adjacent or semantic failure -> do not silently repair. If the failure reveals that the Engine capability/threshold/refusal rule must change, create a new Engine version and rerun qualification.

Scientific failure on an external P1 claim is not a P2 engineering bug. Preserve it under the scientific claim's MFR-14 failure consequence.

## Current execution status

Not runnable yet because the consolidated production Engine release does not yet exist. This plan is ready to become the release checklist once that Engine is frozen.