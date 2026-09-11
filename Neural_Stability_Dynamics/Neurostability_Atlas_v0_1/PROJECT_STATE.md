# Neurostability Atlas v0.1 Project State

Date: 2026-09-11
Governing System Model: **NSD System Model v1.0, architecture locked**
Protocol: **General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum**

## Current status

**A0 coordinate ontology: LOCKED.**

**A1 initial source-selection architecture: LOCKED.**

**A2 first numerical coordinate lane: ACTIVE, SRM observational CSD-SVD repeatability pilot.**

**A2 SRM P0-Q reservoir: SEALED, 34 repeat-session participants.**

**A3 model-conditional derived coordinates: NOT OPENED.**

**P1 / Engine confirmation: NOT AUTHORIZED.**

## Active scientific purpose

Establish whether an Engine-independent, source-provenance-preserving Atlas can reconstruct stable frequency-resolved observable spectral/carrier coordinates on ordinary healthy resting EEG before the Atlas is asked to map perturbations or transitions.

The active pilot is intentionally not a chi reconstruction and not an SSI/DMD analysis. It uses observational cross-spectral matrix SVD on a frozen 1–45 Hz grid with no peak picking.

## Active execution

Source: `ATLAS-SRC-002-SRM`, OpenNeuro `ds003775` snapshot `1.2.1`.

Frozen P0-D pilot subjects: `sub-002, sub-003, sub-005, sub-007, sub-011, sub-020, sub-021, sub-026`, each with `ses-t1` and `ses-t2`.

Selection basis: repeat-session file availability plus lexicographic subject ID only, frozen before EEG inspection.

Input layer: source-provided `derivatives/cleaned_epochs`, explicitly labeled pinned derivative rather than raw EEG.

Current execution path:

`Atlas locks/tests -> exact source-annex retrieval -> source MD5E verification + Atlas SHA-256 -> CSD-SVD reconstruction -> 16 session entries + 8 paired repeat entries -> environment/output hashes`

Transport failures remain mechanical failures and do not permit changes to the frozen pilot design.

## Protected evidence

The remaining 34 SRM repeat participants are frozen in `registries/A2_SRM_REPLICATION_RESERVOIR_FREEZE.json` and may not be downloaded or inspected until an explicit P0-Q qualification freeze exists.

If any reserved EEG is accessed early, the affected evidence must be downgraded as non-independent rather than silently reused as prospective qualification.

## Coordinates active in A2

The first lane maps:

- exact FFT `frequency_hz` grid;
- frequency-resolved cross-spectral strength/singular-value structure;
- leading observational spectral carrier direction;
- leading two-dimensional spectral subspace;
- leading-carrier channel participation;
- within-session split-half carrier/subspace/participation stability;
- t1/t2 carrier MAC;
- t1/t2 subspace similarity;
- t1/t2 participation distance;
- spectral-shape repeatability.

No pass threshold is attached to these quantities in P0-D.

## Explicitly withheld in A2

- continuous-time pole real part;
- decay rate / decay time;
- second-order damping parameter;
- whole-system scalar;
- `chi`;
- disease/phenotype interpretation;
- universal healthy range;
- Engine-validation claim;
- exact t1→t2 elapsed-time coordinate until the source timestamp discrepancy is reconciled.

## Next scientific gate

If A2 mechanically and numerically completes:

1. preserve the full pilot distribution, including poor-repeatability frequencies/participants;
2. audit Function/Limit structure without selecting a pass threshold from the same pilot;
3. decide whether the CSD-SVD reconstruction itself needs revision;
4. if the method is retained, version/freeze the reconstruction and a claim-specific P0-Q scoring/adjudication plan **before** opening the 34-subject reservoir;
5. qualify repeatability prospectively on the reservoir;
6. then reuse the same Atlas contract architecture for perturbation sources (cognitive load, sleep deprivation) and transition sources (sleep/wake, seizure context).

## Why this is on the finish-line path

The Atlas must establish an independently reconstructed coordinate landscape before any later Engine/Atlas comparison can mean more than self-agreement. Starting with nominal repeatability asks the smallest prerequisite question first: whether the coordinate ruler is stable enough to deserve use on perturbations and limits.
