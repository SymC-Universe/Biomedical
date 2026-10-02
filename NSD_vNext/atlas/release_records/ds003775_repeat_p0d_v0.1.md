# Atlas Release Record — ds003775 Repeat P0-D v0.1

Date: 18 September 2026  
Status: COMMITTED ATLAS-P0-D / EXPLORATORY REFERENCE ARTIFACT  
Atlas version: `ds003775-repeat-p0d-v0.1`

## Scope

This is the first versioned Neurophysiological Reference Atlas artifact in the NSD vNext workspace.

It is intentionally narrow:

- OpenNeuro `ds003775`, pinned public release;
- 42 unique subjects;
- two repeat sessions per subject;
- 84 exact pinned EEG recordings;
- resting eyes closed;
- label-blind construction;
- descriptive spectral/repeatability Function- and Limit-Map structure only.

It is **not** a clinical normative model and defines no healthy/pathological cutoff.

## Canonical artifacts

- data: `../reference_models/ds003775_repeat_descriptive_reference_p0d_v0.1.json`
- manifest: `../manifests/ds003775_repeat_atlas_p0d_release_v0.1.json`
- schema: `../manifests/atlas_release_manifest_schema_v0.1.json`
- scientific result record: `../../docs/DS003775_REPEAT_POPULATION_T0_RESULT_v0.1.md`

Source population workflow:

- run `35337659470`
- exact population-summary digest:
  `sha256:0859c127ca1cac7f2789fb12b7e66b1453f9ec6fb250e20f11eed6e84b9e0bb2`

## Contents

The committed P0-D artifact preserves:

- population repeat spectral-shape summaries;
- descriptive periodic/aperiodic repeat summaries;
- model-family disagreement prevalence;
- zero-peak prevalence;
- width-boundary and peak-count saturation Limit-Map quantities;
- channel-wise aperiodic-exponent ICC(A,1);
- channel-wise exact peak-count agreement;
- channel-wise exact zero-peak-state agreement;
- method/hierarchy definitions;
- explicit interpretation ceiling.

It deliberately excludes:

- diagnosis;
- prognosis;
- clinical labels;
- healthy/pathological thresholds;
- admitted modal damping ratios;
- local chi values;
- any whole-system scalar.

## Evidence-path independence

This artifact is graded:

`NON_INDEPENDENT_FOR_ENGINE_VALIDATION`

for the descriptive Engine components qualified on the same ds003775 repeat data.

That limitation is explicit rather than hidden. The spectral operating region was frozen on known truth before the population result and no clinical labels or Atlas-driven thresholds were used, but the same source data contributed to T0 qualification and this reference build.

Permitted current uses:

- P0-D Function Map discovery;
- P0-D Limit Map discovery;
- Atlas serialization/versioning development;
- reporting/tool contract development;
- planning the next independent reference build.

Prohibited current uses:

- independent confirmation of Engine validity;
- P1 confirmation;
- clinical screening or diagnosis;
- prognosis;
- treatment guidance;
- externally valid normative cutoffs.

## Key reference findings

Across 64 channels:

- aperiodic-exponent ICC(A,1) median: **0.65882**;
- exponent ICC(A,1) range: **0.40278–0.83557**;
- exact peak-count agreement median: **0.53571**;
- exact zero-peak-state agreement median: **0.90476**.

These are reference/Limit-Map quantities, not diagnostic thresholds.

## Release consequence

The project has now crossed an implementation boundary:

> the Atlas is no longer only a design document; it has a versioned, machine-readable P0-D artifact with an explicit evidence ceiling.

The next Atlas step is not to invent stronger claims from this cohort. It is to build the next reference layer with greater population breadth and an evidence path appropriate to its intended use.
