# Stage D User Action Checklist

## Current gate
D0 metadata/design inventory only.

## What you should do right now

### Option A - preferred if GitHub preflight succeeds
Nothing manually. The GitHub workflow `GRI Stage D preflight` will run the metadata-only inventory on branch `gri-stage-d-perturbation-recovery`. Wait for the workflow result to be reviewed.

### Option B - only if GitHub live metadata inventory fails because of network/service access
Use Kaggle Phase A:
1. Open Kaggle and create a new notebook.
2. Turn Internet ON.
3. Leave accelerator as NONE.
4. Run the three cells in `GRI_v2/kaggle/STAGE_D_KAGGLE_RUNBOOK.md` exactly as written.
5. Download `STAGE_D_D0_METADATA_RETURN.zip`.
6. Upload that ZIP back to ChatGPT.
7. Do not open/edit the generated CSV/JSON files manually.

## What you should NOT do yet

- Do not download and inspect the numeric methylation/RNA/Hi-C matrices on your own.
- Do not create plots or differential-expression/methylation contrasts.
- Do not choose genes/Hallmarks because they look interesting.
- Do not start D3/D4 transformation analysis.
- Do not run the old post-C1 runner if a newer amended runner is supplied before execution.

## What happens next after D0 metadata returns

ChatGPT will:
1. verify accession/file/sample metadata;
2. resolve or explicitly retain ambiguous sample labels;
3. build the D0.2 assay-overlap/design audit;
4. freeze D0.3 exact analysis rules;
5. build the heavy Kaggle/PowerCell runner;
6. give you one exact run sequence and the expected return artifact.
