# Submission / reviewer release checklist

Use this checklist whenever a manuscript, data note, supplement, or reproducibility package cites material from GRI v2.

The goal is simple: a reviewer should be able to move from a manuscript claim to the exact frozen code, config, data identity, result, audit, and test record without guessing which repository state was used.

## 1. Freeze the scientific state

Before submission:

- all stages used by the paper must be marked closed or explicitly labeled exploratory/development in the manuscript;
- no partial checkpoint may be promoted as a final result;
- the manuscript claim language must match the current claim-to-evidence map;
- any post-result change to a scientific definition must be documented as post-result rather than silently replacing the preregistered state;
- failed, null, deferred, and non-identifiable branches relevant to the paper must remain visible.

## 2. Create an immutable submission snapshot

For each submission version, create a new immutable tag/release rather than directing reviewers to the moving `gri-v2` branch.

Recommended tag pattern:

`gri-v2-<paper-short-name>-submission-v<major>.<minor>`

A revised submission receives a new tag. Existing submission tags are never moved or rewritten.

Record:

- exact Git commit SHA;
- tag/release name;
- manuscript title and version;
- submission date;
- journal or repository destination, if applicable;
- exact stages included in the paper;
- explicit stages excluded, deferred, or still in progress.

## 3. Build a submission-specific reviewer index

The submission snapshot should contain a short index that links each major manuscript claim to:

- scientific definition/config;
- analysis implementation;
- test file or CI record;
- compact result file;
- full-result artifact/hash when the full result is too large for Git;
- dated audit/interpretation record;
- manuscript figure/table that uses the result.

Do not make a reviewer reconstruct this mapping from directory names.

## 4. Freeze figure and table provenance

For every submitted figure and table, record:

- manuscript figure/table identifier;
- source data file(s);
- plotting/table-generation script;
- SHA-256 of the exact source table used;
- SHA-256 of the generated figure/table file when practical;
- any filtering or display-only transformation;
- whether the figure is primary, sensitivity, diagnostic, or explanatory.

A manuscript figure must not be a manually edited orphan that cannot be regenerated from preserved data and code.

## 5. Freeze result-file provenance

Record SHA-256 hashes for every result file relied upon by the paper.

For large results not committed to Git:

- give the exact filename;
- give SHA-256;
- state where the artifact is deposited or how it can be reconstructed;
- link the generating config and code;
- retain compact committed summaries sufficient to identify the result state.

`../artifacts/MILESTONE_ARTIFACTS.md` is the standing project registry for these larger artifacts.

## 6. Freeze source-data provenance

For each external source dataset used by the submission, record:

- dataset/project name;
- source organization;
- accession, DOI, UUID, or stable source identifier where available;
- exact downloaded filename or source object;
- version/date where available;
- byte size and SHA-256 when locally frozen;
- access/license restrictions;
- preprocessing source and whether preprocessing was performed by the project or upstream.

Do not commit multi-gigabyte public source data merely to make the repository look self-contained. Preserve identity and verification instead.

## 7. Record the executable environment

The release should identify:

- Python version;
- package requirements/lock file;
- operating-system-specific launchers if used;
- random-seed policy;
- deterministic/non-deterministic components;
- expected output counts;
- restart/resume semantics for long calculations.

## 8. Capture test and CI state

Before the submission tag is cut:

- run the complete relevant test suite;
- record the passing test count;
- record the CI workflow/run used when available;
- resolve or explicitly document any skipped or expected-failure tests;
- include integrity/contract tests that prevent frozen scientific settings from drifting unnoticed.

## 9. Maintain a non-claim ledger

Each submission should state, in one place, what the evidence does **not** establish.

For the current GRI v2 program this includes, unless later evidence changes the status through a documented gate:

- `CV/2` is not biological chi;
- static RNA/genomic/protein organization is not by itself a dynamical damping measurement;
- cross-assay coupling does not establish causal control;
- no universal cancer optimum is implied;
- `chi = 1` is not presumed to define health or treatment response;
- a compressed scalar does not replace its modal carrier or the system-level organization from which it is derived;
- deferred or failed branches are not silently converted into supporting evidence.

## 10. Reviewer-facing final check

A reviewer opening only the frozen submission snapshot should be able to answer all of the following without contacting the author:

1. What exactly is the paper claiming?
2. Which claims were preregistered or frozen before the target result?
3. Which results are primary versus sensitivity/diagnostic?
4. Where is the code that generated each result?
5. Where are the result data or their immutable hashes?
6. What source data were used?
7. Which tests verify the analysis contract?
8. What failed, remained null, or was deferred?
9. What changed after results were known?
10. Can the submitted figures and tables be regenerated from preserved source material?

If any answer requires inference from repository archaeology, the submission package is not ready yet.
