# Bio Chi autonomous continuation checkpoint

**Created:** 22 September 2026  
**Last updated:** 23 September 2026  
**Status:** ACTIVE  
**Branch:** `chi-bio-recovery-p0d-20260922`  
**Authority:** SymC General Operations Manual v0.8.4  
**Purpose:** durable continuation after chat, polling, workflow, timeout, packaging, or session interruptions without requiring the user to restart the investigation.

## Non-negotiable resume rule

Every continuation run must:

1. read this checkpoint first;
2. verify branch/head, PR #6, literature-search state, workflow state, and `BIO_CHI/control/WORK_QUEUE.json`;
3. continue the first incomplete safe/mechanical task;
4. preserve every frozen scientific decision, failure, null, refusal, indeterminate result, and representation-dependent result;
5. never retune a cohort, endpoint, state representation, threshold, seed, null, comparator, mapping, boundary, or mode because of an observed result;
6. keep all working manuscript prose private;
7. treat queued jobs, timeouts, stale sessions, packaging failures, polling limits, and mechanically repairable workflow errors as recoverable interruptions rather than scientific stop conditions;
8. update durable GitHub provenance/checkpoint records before ending each run.

## Scientific stop conditions

Stop substantive progression only if proceeding would require:

- selecting or changing a scientific hypothesis after viewing decisive evidence;
- changing a frozen endpoint, cohort, threshold, boundary, state representation, null, comparator, mapping, or scientific seed set;
- choosing among materially different native biological models when that choice changes interpretation;
- opening decisive evidence before its required freeze/independence controls are complete;
- redefining `chi`, `chi_bio`, `Chi_bio`, Bio Chi, or an inheritance criterion;
- overriding or relabeling a failed/refused/indeterminate result;
- making an unlicensed publication-level causal or universal claim;
- a source defect that makes the frozen task scientifically non-evaluable and cannot be repaired mechanically.

## Current execution queue

The machine-readable source of record is `BIO_CHI/control/WORK_QUEUE.json`.

- **Q0 governance/reproducibility:** COMPLETE / MAINTAIN.
- **Q1 literature collision:** opening broad collision COMPLETE; targeted updates only.
- **Q2 dataset eligibility/source qualification:** ACTIVE; public source files are frozen and qualification continues.
- **Q3 known-truth qualification system:** PENDING Q2.
- **Q4 cancer recovery system:** PENDING Q2.
- **Q5 chi_bio scalar track:** native behavior and local-stability qualification completed for the current NF-kB model; scalar remains **NOT ADMITTED** pending representation/identifiability controls.
- **Q6 Chi_bio modal track:** descriptive six-mode generator inventory completed; this is a modal precursor only, not an admitted biological Chi representation. Full admission remains pending Q2/Q3 plus representation controls.
- **Q7 Bio Chi conglomerate:** PENDING Q3/Q4/Q6.
- **Q8 Stability Inheritance biological test:** PENDING carrier-qualified data.
- **Q9 working manuscript:** NOT OPEN / PRIVATE.

## Verified literature state

- The two broad Undermind searches remain COMPLETE:
  - biological stability / perturbation recovery / state inheritance;
  - native biological generators for `chi_bio`.
- No broad literature rerun is warranted. Search work is targeted-only when it closes a concrete execution/source gap.
- Jaruszewicz-Blońska et al. remains the active native-generator qualification model; it is not treated as evidence that a universal scalar biological chi exists.

## Source/reproducibility spine already closed

- External GEO/S1 source freeze completed and pinned.
- Jaruszewicz S1 Code archive and member hashes frozen.
- Untouched-source Octave portability failure preserved as a mechanical compatibility failure.
- MATLAB R2023b compatibility reproduction used exactly one documented API compatibility repair; equations, parameters, stimulation protocol, thresholds, and scientific interpretation were not changed.
- Authors' supplied `run_simulate_reduced.m` was audited: its seven protocol figures are not Figure 8A-C and are not relabeled as such.
- Native output capture preserves seven figures, 42 axes, and 42 numeric trajectories with authored axis semantics.

## Figure 8 native-behavior state

Durable pin: `BIO_CHI/config/JARUS_FIG8_V02_RESULT_PIN_v0_1.json`.

Corrected frozen Figure 8 execution and behavior adjudication completed under run **35854793170**.

Preserved finite-window outcomes:

- `FIG8A_NOMINAL_DAMPED`: **PASS_DAMPED_COMPATIBLE** under the frozen finite-window rule.
- `FIG8B_LIMIT_CYCLE`: **FAIL_NATIVE_BEHAVIOR** under the frozen finite-window sustained-compatibility rule because all ten complete peak-to-trough amplitudes decreased over the 30 h window.
- `FIG8C_RELAXATION_OSCILLATION`: **FAIL_NATIVE_BEHAVIOR** under the frozen finite-window sustained-periodicity rule because all ten complete peak-to-trough amplitudes decreased over the 30 h window.

These B/C failures remain failures and must never be relabeled. They also do not by themselves refute the distinct local/topological claim that an unstable equilibrium may be surrounded by a stable limit cycle; the finite-window rule did not adjudicate that topological claim.

No `chi_bio`, `Chi_bio`, or Bio Chi quantity was constructed from the finite-window trajectories.

## Local-stability qualification state

### Preserved failed/indeterminate paths

- v0.1 log-coordinate root/local-stability route: **INDETERMINATE**, preserved in `BIO_CHI/config/JARUS_LOCAL_STABILITY_V01_RESULT_PIN.json`.
- v0.2 physical-coordinate route: **INDETERMINATE**, preserved in `BIO_CHI/config/JARUS_LOCAL_STABILITY_V02_RESULT_PIN.json`.
- v0.3 bounded-residual route successfully found one accepted positive equilibrium per frozen case at residuals far below the unchanged `1e-9` residual gate, but its aggregate `max_real_eigenvalues` summary serialized incorrectly as `[0,0,0]` even though the immutable per-step Jacobian records contained the correct nonzero values. This is preserved as **MECHANICAL_POSTPROCESS_INCONSISTENCY** in `BIO_CHI/config/JARUS_LOCAL_STABILITY_V03_RESULT_PIN.json`; the defective v0.3 classification is not promoted.

### Frozen artifact-only v0.4 repair

Before repair output was generated, `BIO_CHI/config/JARUS_LOCAL_STABILITY_POSTPROCESS_FREEZE_v0_4.json` froze an artifact-only adjudication against immutable v0.3 evidence. Root finding and Jacobians were not rerun and no scientific rule changed.

Workflow run **35857105311** completed successfully. Artifact **10747972701**, ZIP SHA-256 `2a0143fec6d77037222f8207c939d05a7708e2c2354041cb83d0a268cb5a0498`.

Durable pin: `BIO_CHI/config/JARUS_LOCAL_STABILITY_V04_RESULT_PIN.json`.

Frozen local-stability result:

- `FIG8A_NOMINAL_DAMPED`: one accepted root, residual `2.4210600429834528e-14`; spectral-abscissa samples all negative -> **STABLE / PASS**.
- `FIG8B_LIMIT_CYCLE`: one accepted root, residual `1.0787811616230769e-17`; spectral-abscissa samples all positive -> **UNSTABLE / PASS** for the frozen local-equilibrium claim.
- `FIG8C_RELAXATION_OSCILLATION`: one accepted root, residual `1.0344097800540908e-16`; spectral-abscissa samples all positive -> **UNSTABLE / PASS** for the frozen local-equilibrium claim.

Overall native local-stability gate: **PASS_ALL_FROZEN_FIG8_CASES**.

This does **not** prove a stable limit cycle, does not erase the finite-window B/C failures, and does not license `chi_bio`.

## Descriptive six-mode generator inventory

A post-view descriptive inventory was explicitly frozen as non-prospective in `BIO_CHI/config/JARUS_MODAL_INVENTORY_FREEZE_v0_1.json`. It preserves all six modes, uses the immutable v0.3 Jacobian records only, performs no new root solve/Jacobian calculation, selects no preferred mode, and cannot serve as prospective validation.

Workflow run **35857535131** completed SUCCESS. Artifact **10747927367**, ZIP SHA-256 `e3a28759b4b8dc9de0885170cc2d365d8678852090b3f70ff51c1efea2686d5a`.

Durable pin: `BIO_CHI/config/JARUS_MODAL_INVENTORY_V01_RESULT_PIN.json`.

Descriptive findings:

- Every frozen Figure 8 equilibrium contains **four stored exactly-real eigenvalues plus one nonreal conjugate pair** at each of the three already-computed finite-difference step multipliers.
- All-mode matching across the three step multipliers is numerically stable; maximum observed relative complex spread across matched modes is approximately `4.87e-11` (A), `1.60e-11` (B), and `2.27e-11` (C). These are descriptive observations, not promotion thresholds.
- Figure 8A reference-step complex pair is approximately `-1.9998283e-4 +/- 9.1682477e-4 i`, but the spectral abscissa is a **separate real mode** at approximately `-1.5742807e-4`. Thus the oscillatory pair is not the slowest local decay mode in the nominal stable case.
- In Figure 8B and Figure 8C, the unique complex pair has positive real part and sets the local spectral abscissa.

No preferred complex pair has been selected for a biological scalar. No `chi_bio` has been defined. The descriptive mode inventory is a **modal precursor**, not admitted `Chi_bio`.

## Current workflow state at checkpoint

- PR #6 remains OPEN, DRAFT, and mergeable on `chi-bio-recovery-p0d-20260922`.
- Modal inventory run **35857535131** is terminal SUCCESS.
- The subsequent ordinary governance/privacy and GRI regression checks triggered by queue/provenance commits were still running at the moment this checkpoint was written; these are mechanical CI and are not a scientific stop condition. Inspect and repair only if they fail.
- Working manuscript material remains private.

## Exact next safe resume

1. Verify current PR/head and the terminal state of governance/privacy and GRI regression checks. Repair only demonstrated mechanical failures.
2. Preserve the finite-window B/C failures, v0.1/v0.2 indeterminates, and v0.3 postprocess failure exactly as recorded.
3. The next Q5/Q6 gate is **representation/identifiability sensitivity before scalar reduction**. Any such gate must retain the complete six-mode generator and must be frozen before opening new decisive representation-dependent results.
4. A safe first representation control may test full-state invertible coordinate transformations as a necessary numerical invariance check, but it must be labeled necessary-not-sufficient and cannot establish biological representation independence by construction.
5. Do **not** choose a preferred complex pair, define a damping-like scalar, call the unique oscillatory pair the system-wide governing mode, or admit `chi_bio` from the current observed spectrum. Figure 8A already demonstrates that the oscillatory pair and the spectral-abscissa mode are distinct.
6. Continue Q2 source/testbed qualification in parallel where outcome-blind and mechanically defined. Known-truth and cancer recovery promotion remain gated by Q2.
7. Stop and surface the issue only if the next step requires a genuinely new scientific representation/model choice under the stop conditions above.
8. Keep manuscript prose private and update this checkpoint plus machine-readable provenance before ending the next run.
