# Neurophysiological reference Atlas scaffold

Status: ACTIVE IMPLEMENTATION / FIRST ATLAS-P0-D ARTIFACT COMMITTED

This directory will contain versioned reference artifacts generated from a frozen, qualified Structural Engine.

The Atlas is constructed independently of disorder-specific model fitting. It describes ordinary/reference variation, test-retest structure, acquisition effects, spatial/modal organization, admission/refusal prevalence, and Function/Limit regions. This does not automatically make every Atlas evidence path independent for Engine validation; that grade is recorded per reference family.

The Atlas must not be rebuilt per disorder to improve separation.

Canonical design: `../docs/NEUROSTABILITY_ATLAS_SPEC_v0.1.md`.

Expected future artifact families:

```text
manifests/
reference_models/
function_maps/
limit_maps/
release_records/
```

Each released Atlas artifact must declare the Engine version, datasets, subject inclusion identity, recording conditions, covariates, preprocessing/configuration hashes, scope, and a GOM 16.4 evidence-path independence audit for each decisively used reference family.

The machine-readable release contract is `manifests/atlas_release_manifest_schema_v0.1.json`.

## First committed P0-D artifact

The first exploratory reference artifact now exists:

- `reference_models/ds003775_repeat_descriptive_reference_p0d_v0.1.json`
- release manifest: `manifests/ds003775_repeat_atlas_p0d_release_v0.1.json`

Scope is deliberately narrow: 42 label-blind repeat-session subjects / 84 recordings from the pinned ds003775 release, descriptive spectral/repeatability Function- and Limit-Map structure only.

This is **not** a clinical normative model, does not define healthy/pathological cutoffs, contains no admitted modal damping ratio, and is graded `NON_INDEPENDENT_FOR_ENGINE_VALIDATION` for the Engine components that were qualified on the same source data.

Its immediate uses are P0-D Atlas serialization, Function/Limit discovery, reporting/tool contract development, and planning of the next independent reference build.
