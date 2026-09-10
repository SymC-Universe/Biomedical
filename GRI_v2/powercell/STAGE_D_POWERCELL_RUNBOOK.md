# Stage D PowerCell Runbook

Status: USER EXECUTION GUIDE; SCIENTIFIC LOGIC REMAINS IN GITHUB
Branch: `gri-stage-d-perturbation-recovery`

## Role

PowerCell is the restart-safe backend for long or repeated Stage-D jobs. It is not used to define new scientific rules. Every run must record the exact GitHub commit and use the same frozen Python source as Kaggle/GitHub.

## Before any long Stage-D run

1. Keep existing GRI/C1 `WORKING_STATE` intact. Stage D uses a separate directory.
2. Obtain the exact Stage-D runner package or clone/export of the frozen branch supplied for the active gate.
3. Confirm the package/run log prints the expected GitHub commit SHA.
4. Do not modify JSON configs manually.
5. Keep the machine awake for the run unless the runner is documented as restart-safe.

## Directory convention

A Stage-D PowerCell runner will use:

- `WORKING_STATE/` - checkpoints and downloaded/cache identities;
- `RETURN_TO_CHAT/` - compact result packages only;
- `RUN_LOG.txt` - full execution log;
- `PROVENANCE/` - source hashes, environment, commit identity.

Existing C1 state is read only when an explicitly frozen analysis requires it. Stage D must never overwrite the C1 state directory.

## Failure rule

If a run stops:
- do not delete `WORKING_STATE`;
- do not start over unless instructed;
- return `RUN_LOG.txt` and any file already present in `RETURN_TO_CHAT`;
- preserve the runner directory exactly as it is.

Mechanical repairs may continue from the checkpoint. Scientific changes require a new committed amendment before restart.

## Independent verification use

When Kaggle completes a primary heavy run, PowerCell may independently rerun:
- hashes and manifest checks;
- final matrix dimensions;
- compact sufficient statistics;
- frozen model outputs;
- repeated-null summaries;
- figure/table inputs.

The verification run must use the same commit/config but may use a different machine/environment. Environment differences are recorded rather than hidden.

## Current action

No PowerCell biological Stage-D run is authorized yet. The current gate is D0 metadata/design inventory. The first heavy PowerCell package will be built only after D0.3 freezes the exact assay files, feature universes, preprocessing, nulls, and model families.
