# NSD Long-Run Conveyor Ceiling v0.1

**Status:** FROZEN OPERATIONAL CEILING  
**Date:** 29 September 2026  
**Governance:** SymC General Operations Manual v1.0

## Purpose

This document separates scientific authority from execution plumbing.

GitHub Actions may execute only prospectively frozen work, preserve evidence, verify contracts, checkpoint progress, resume after interruption, and package evidence for review. GitHub Actions may not make scientific decisions.

## Scientific authority

Scientific interpretation, claim promotion, architecture revision, threshold selection, new hypothesis selection, and decisions about chi/Chi/system meaning remain with the researcher and ChatGPT.

The conveyor must never:

- invent or alter a scientific threshold;
- change a frozen generator, comparator, metric, horizon, seed, sampling contract, observation mapping, or perturbation;
- decide whether a result supports or falsifies a scientific claim;
- decide whether local chi is scientifically admitted to real EEG;
- collapse local chi, modal/vector Chi, and system/conglomerate behavior;
- convert designed qualification frequencies into prevalence;
- repair a scientific failure by changing the design.

## Ceiling

The conveyor is authorized to run continuously through the following operational ceiling for both N-B1 and N-B2/N-B3:

1. `PACKET_BOUND`
2. `FROZEN_INPUT_VALIDATED`
3. `IMPLEMENTATION_TESTED`
4. `PREFLIGHT_PASS`
5. `FULL_EXECUTION_COMPLETE`
6. `MERGED_EVIDENCE_COMPLETE`
7. `REPRODUCIBILITY_CHECK_COMPLETE`
8. `SCIENTIFIC_REVIEW_READY`

The conveyor stops at `SCIENTIFIC_REVIEW_READY`. Scientific adjudication occurs outside GitHub.

## Early stop conditions

The conveyor may stop earlier only for:

- `MECHANICAL_FAILURE`
- `FROZEN_CONTRACT_VIOLATION`
- `SOURCE_OR_DEPENDENCY_BLOCK`
- `CHECKPOINT_CORRUPTION`

A numerical result that is surprising, unfavorable, null, pathological, or outlying is not an early-stop condition by itself. It is preserved as evidence.

## Checkpoint contract

A machine-readable checkpoint is written after every ceiling stage. Every checkpoint contains:

- lane;
- stage;
- UTC timestamp;
- git SHA;
- packet/config digest;
- completed case identities;
- incomplete case identities;
- artifact paths and hashes where available;
- next exact mechanical action;
- stop reason if stopped.

On restart, the conveyor resumes from the newest internally consistent checkpoint and must not recompute completed cases unless their artifact is missing or hash-invalid.

## Runtime contract

One GitHub Actions run may execute for up to 330 minutes. The conveyor should keep moving within the same run as long as mechanically authorized work remains. Near the runtime reserve, it must checkpoint and exit cleanly. A scheduled successor run resumes from that checkpoint.

This ceiling does not authorize any real-EEG local-chi inference or new scientific claim.
