# Neurophysiological reference Atlas scaffold

Status: IMPLEMENTATION PLACEHOLDER / ATLAS NOT YET POPULATED

This directory will contain versioned reference artifacts generated from a frozen, qualified Structural Engine.

The Atlas is independent of disorder-specific model fitting. It describes ordinary/reference variation, test-retest structure, acquisition effects, spatial/modal organization, admission/refusal prevalence, and Function/Limit regions.

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

Each released Atlas artifact must declare the Engine version, datasets, subject inclusion identity, recording conditions, covariates, preprocessing/configuration hashes, and scope.

The first machine-readable release contract is `manifests/atlas_release_manifest_schema_v0.1.json`. It defines version/provenance/scope fields only and does not imply that an Atlas release currently exists.
