# Historical NSD Source Audit v0.1

Date: 14 September 2026
Status: SOURCE-LEVEL RECONSTRUCTION COMPLETE FOR AVAILABLE MANUSCRIPT MATERIAL
Governing standard: SymC General Operations Manual v0.8.0 + NSD Project Protocol v0.1

## 1. Recovered source package

The user supplied the only historical NSD material presently worth treating as source evidence:

| File | Role | Size | SHA-256 |
| --- | --- | ---: | --- |
| `SymC_NSD.tex` | Main manuscript source | 50,025 bytes | `e2bf2d50053c18d2dfdc021173b3571566a07bc6b173de4e0452c1d890553a91` |
| `supmats.tex` | Supplementary source | 31,292 bytes | `5e443945bb834809285ec75332b1b5811118becafb2d94ee88ee2d4105eb4167` |
| `SymC_NSD.pdf` | Rendered main manuscript | 2,435,774 bytes | `4fefa187ccd03290d263a9435bd91acac5a3900f6a25f5d3abf1c24f6ef47485` |
| `SymC_NSDsupmats.pdf` | Rendered supplement | 1,332,164 bytes | `cfa60395ac4cc7caccfb1655a8224ea85899748681e84de84abb4bd88e69a1b2` |

The `.tex` files contain 995 and 851 lines respectively. They are now the highest-authority historical source text available for reconstruction. No source-code package that generated the plotted values has been recovered.

## 2. Central audit finding

The historical paper successfully **visualized a proposed architecture**, but its figures, thresholds, disorder coordinates, treatment mappings, and cross-domain numerical claims cannot be treated as empirical validation because the available source package does not provide the data lineage, code, preprocessing, subject inventory, or result-generation chain needed to establish them as measured results.

This is the most important reconciliation decision in the NSD rebuild:

> **The historical figures are architectural demonstrations unless and until a specific empirical provenance chain is independently reconstructed. They are not evidence merely because they look data-like.**

This distinction repairs the original confidence error without discarding the conceptual work that can still be tested.

## 3. Figure-by-figure classification

### Main Figure 1 — Prodromal Critical Cascade

Historical caption presents a time-series trajectory with stable, variance-spike, and mean-drift stages and interprets it as a pre-critical cascade.

Current classification: `ILLUSTRATIVE / HYPOTHESIS-GENERATING`.

Reason:
- no cohort or dataset identifier;
- no subject count or acquisition source;
- no code or model-parameter provenance in the source package;
- no uncertainty or inferential test;
- no event-aligned empirical validation.

Salvageable content:
- the experimental question that variance may change before the mean;
- the need to separate variance, mean, timescale, and recovery dynamics;
- the proposed falsifier that variance and mean do not separate temporally.

### Main Figure 2 — Neuro Stability Spectrum (N=100)

Historical caption calls the display a population analysis and shows disorder clusters in a two-dimensional drive/stability space.

Current classification: `SYNTHETIC ARCHITECTURE DISPLAY / NOT AN EMPIRICAL COHORT`.

Reason:
- the source package contains no subject table, raw values, dataset identity, enrollment criteria, or code lineage for the plotted 100 points;
- disorder clusters are visually assigned to attractor regions that mirror the theory being illustrated;
- the paper provides no independent path from measured neurophysiology to the plotted coordinates.

Critical correction:
- `N=100` in this historical figure must not be interpreted as 100 measured participants.

Salvageable content:
- the idea that a useful architecture should expose overlap, divergence, trajectories, and categorical/non-scalar states rather than force one disease per axis;
- the need to test whether disorder groups occupy distinct or overlapping regions under frozen feature construction.

### Main Figure 3 — “Inattentive Defense” / Live Neural Ticker

Historical caption describes a real-time trajectory from resting-state fMRI in an inattentive-ADHD subject and labels the state overdamped.

Current classification: `PROVENANCE-UNRESOLVED / CANNOT SUPPORT A RESULT`.

Reason:
- the source package does not identify the dataset, subject, acquisition, preprocessing, signal-to-coordinate transformation, or code;
- even if a real signal was used, the inferential step from signal amplitude to a damping coordinate is not documented;
- the displayed stability value therefore cannot currently be treated as a measured dynamical quantity.

Disposition:
- retain only as historical provenance of the architectural idea;
- do not copy into the new manuscript as evidence;
- a future analogous figure must be regenerated from a fully traceable subject/session pipeline.

### Main Figure 4 — Phase-Shifting Mechanical Lineage

The caption explicitly calls the 0-to-80-year display a longitudinal simulation.

Current classification: `ILLUSTRATIVE SIMULATION`.

Salvageable content:
- a candidate longitudinal hypothesis that different failure architectures may appear at different periods;
- a requirement for actual longitudinal data before any lineage claim is made.

Not salvageable as evidence:
- the specific ADHD -> bipolar -> depression -> dementia sequence;
- the timing or inevitability of transitions;
- the numerical trajectory.

### Main Figure 5 — Substrate Inheritance / Quantum-to-Neural comparison

The figure visually compares a quantum probability-style landscape with the neural stability spectrum and historically describes this as inheritance rather than analogy.

Current classification: `CONCEPTUAL ANALOGY / HISTORICAL OVERCLAIM`.

Reason:
- visual similarity is not a mechanistic inheritance proof;
- no derivation in the historical source establishes propagation of a damping boundary from QED through metabolism to neural dynamics;
- the neural side depends on the unvalidated Figure 2 coordinate display.

Disposition:
- retire the historical “not analogy but inheritance” evidentiary claim from NSD;
- any future substrate-inheritance claim must be independently derived and tested at each interface.

### Supplementary Figure S1 — Scale invariance

Current classification: `ILLUSTRATIVE CROSS-DOMAIN CARTOON`.

The figure places selected underdamped, critical, and overdamped states at different nominal frequencies. It demonstrates how the proposed coordinate system can be drawn across timescales; it does not establish empirical scale invariance.

### Supplementary multi-scale signal texture figure

Current classification: `ILLUSTRATIVE SIGNAL SHAPES`.

The anxiety/health/depression waveforms demonstrate a visual concept but do not establish disorder-specific waveforms or a whole-system mechanical failure mode.

### Supplementary regional heatmaps

Current classification: `ILLUSTRATIVE TOPOLOGY`.

The heatmaps are useful design sketches for what a regional architecture could look like. Their cell values are not established patient measurements in the available source package.

## 4. Table and numerical-claim classification

The historical paper contains many exact numerical disorder coordinates, thresholds, expected treatment effects, relapse rules, cross-domain values, and proposed clinical cutoffs. The available source package does not provide the empirical derivation required to elevate those numbers beyond hypothesis or illustration.

Examples requiring retirement or reset include:
- universal adaptive windows such as `chi = 0.8-1.0` as a health claim;
- disorder-specific coordinates such as anxiety near `0.65`, depression near `1.35`, and similar table entries;
- exact regional-divergence thresholds;
- exact breach-duration thresholds;
- exact HRV-to-chi mapping coefficients;
- exact relapse-risk thresholds for rolling variance;
- claimed treatment-induced percent changes in omega, gamma, or chi;
- claimed cross-domain empirical chi values and event trajectories;
- exact cross-modal correlations described as preliminary data;
- the claim that a cumulative chi-deviation integral predicts later cognition at a specified correlation.

Current status for all such historical values: `NOT EARNED / DO NOT TRANSFER AS RESULTS` unless a separate auditable evidence path is later recovered.

## 5. Citation architecture problem

The recovered TeX contains a bibliography but no inline `\cite{...}` commands in either the main or supplementary source. This means the source package does not bind individual mechanistic, numerical, treatment, epidemiological, or biomarker statements to particular references.

Consequences:
- the reference list cannot be treated as claim-level support;
- each surviving statement in the rebuilt manuscript requires a new claim-to-source mapping;
- historical statements that are retained only as hypotheses should be labeled as hypotheses rather than retroactively “supported” by a nearby bibliography entry.

## 6. What the old paper genuinely contributes

The historical paper is scientifically useful as a **design document** even though it is not a validated empirical study.

High-value architectural ideas to preserve and test:
1. stability should be treated as multiscale rather than a single static number;
2. timescale can matter independently of mean state;
3. regional/modal divergence may carry information hidden by global averages;
4. comorbidity can be posed as a geometry/organization question rather than assumed to be multiple independent diseases;
5. a system may need distinct scalar, modal, spatial, and system-level descriptions;
6. longitudinal recovery, variance, and residence may matter separately;
7. proposed failure modes are useful as candidate phenotypes if allowed to fail empirically;
8. experiments can be written with explicit falsifiers;
9. categorical diagnostic labels need not be the only coordinate system used to study neurophysiology.

These are hypotheses and architecture, not historical validations.

## 7. What must be retired from the forward evidence base

The following historical formulations are not allowed to enter the new manuscript as established findings:
- “all major psychiatric disorders are coordinates in one stability space”;
- “the comorbidity paradox dissolves” as a demonstrated result;
- a universal neural `chi ~ 0.9` health optimum;
- direct identification of aperiodic exponent with dynamical chi;
- routine identification of EEG peak width with mechanical damping;
- direct mapping of neurotransmitter systems onto a single gamma damping coefficient;
- exact disorder-specific chi values without empirical derivation;
- claims that specific therapies move gamma, omega, or chi by stated amounts without direct evidence;
- the phase-shifting ADHD -> bipolar -> depression -> dementia lineage as an observed clinical sequence;
- quantum-to-neural inheritance inferred from visual/geometric similarity;
- cross-domain validation based on analogous plots or hand-assigned coordinates.

## 8. Reclassification under the current maturity ladder

The historical NSD work is best classified as:

- `P0-D`: architecture discovery, visualization, hypothesis generation, experiment design;
- not yet `P0-Q` for empirical scalar qualification;
- not `P1` confirmation;
- not `P2` tool or clinical framework.

This is not a demotion of the useful part of the work. It places the original contribution at the stage it actually supports.

## 9. Immediate manuscript consequence

The rebuilt manuscript should explicitly state that the 2025 historical manuscript contained architecture-first displays that were later recognized as non-empirical demonstrations. This correction is part of the provenance record and should be retained because it explains why the new framework separates:

`visualizable architecture -> recoverable signal structure -> licensed estimator -> audited data -> frozen test -> claim`.

## 10. Remaining historical-source gap

The source text and rendered PDFs are now reconstructed. The remaining unrecovered historical dependency is the original code/data package behind any plots that may have used real inputs. Unless that package reappears, the old plotted values remain non-evidentiary.

No future work should block on recovering that package. The forward program should regenerate every empirical figure from traceable current data and code.