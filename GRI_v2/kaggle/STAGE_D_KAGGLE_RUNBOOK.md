# Stage D Kaggle Runbook

Status: USER EXECUTION GUIDE; SCIENCE LIVES IN THE FROZEN GITHUB CONFIG/PROTOCOL
Branch: `gri-stage-d-perturbation-recovery`

## Rule zero

Kaggle is a compute backend, not a second scientific implementation. The notebook must clone the exact frozen GitHub branch/commit and run the canonical scripts from that checkout. Do not paste alternate analysis code into the notebook after biological results begin.

## Phase A - metadata/design only

Use Kaggle only after the GitHub metadata preflight passes or if GitHub cannot reach NCBI reliably. Phase A is allowed to read GEO/SRA sample metadata and file listings, but not to inspect numeric biological matrices for outcome differences.

### Exact notebook cell 1 - clone authoritative branch

```bash
!git clone --branch gri-stage-d-perturbation-recovery --single-branch https://github.com/SymC-Universe/Biomedical.git /kaggle/working/Biomedical
!cd /kaggle/working/Biomedical && git rev-parse HEAD
```

Record the printed commit SHA in the Kaggle run output.

### Exact notebook cell 2 - run metadata inventory

```bash
!cd /kaggle/working/Biomedical && python GRI_v2/src/stage_d_acquisition_inventory.py --registry GRI_v2/config/stage_d_dataset_registry_v0.1.json --out /kaggle/working/STAGE_D_D0_METADATA
```

### Exact notebook cell 3 - package return artifact

```bash
!cd /kaggle/working && zip -r STAGE_D_D0_METADATA_RETURN.zip STAGE_D_D0_METADATA
```

Download `STAGE_D_D0_METADATA_RETURN.zip` and return it to ChatGPT before proceeding to numeric biological matrices.

## Phase B - heavy acquisition/preprocessing

DO NOT START PHASE B until the D0.3 final analysis freeze is committed. The D0 metadata/design audit may force assay-specific choices that must be frozen before matrix inspection.

When Phase B is authorized, the canonical heavy runner will be added to this same branch. It will:
- download only the frozen files in the acquisition manifest;
- verify byte size and SHA-256;
- checkpoint every large transformation;
- write state under `/kaggle/working/WORKING_STATE`;
- write compact outputs under `/kaggle/working/RETURN_TO_CHAT`;
- never store third-party raw matrices in GitHub.

## Kaggle settings

Recommended initial settings:
- Internet: ON, because GEO/SRA files are public network sources;
- Accelerator: NONE unless a later frozen model explicitly uses GPU;
- Persistence: save notebook version after each completed gate;
- RAM: use standard/high-RAM session as available;
- Working directory: `/kaggle/working`.

Do not enable GPU merely because it is available. Most Stage-D linear algebra is CPU/RAM bound unless a later frozen nonlinear model explicitly benefits from GPU.

## What to return after Phase A

Return exactly:
- `STAGE_D_D0_METADATA_RETURN.zip`
- the Kaggle notebook commit SHA printed by `git rev-parse HEAD`
- any visible error message if the run did not finish.

Do not manually edit the generated CSV/JSON files before returning them.
