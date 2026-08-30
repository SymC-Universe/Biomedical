# GRI v2 repository workflow

## Branch model

- `main`: stable public biomedical history and released milestones.
- `gri-v2`: active Cancer Stability Atlas development branch.

Do not push ordinary development directly to `main`. Merge or promote only scientifically stable milestones after audit.

## Scientific steering rule

The active project is tool discovery and validation, not defense of the historical GRI manuscript. The manuscript may supply provenance, candidate hypotheses, and lessons from failure, but it does not define the target architecture. See `docs/TOOL_OBJECTIVE.md`.

## What belongs in GitHub

Keep the reproducible project spine here:

1. source code and launchers;
2. frozen/development configs;
3. tests and CI;
4. epistemic rules and scientific specifications;
5. compact result summaries and provenance hashes;
6. current build status and exact next step;
7. change records when a scientific assumption or test definition changes;
8. reviewer navigation and immutable submission-snapshot records.

Avoid filling the repository with repeated full ZIP snapshots or multi-gigabyte source data when the same state can be reconstructed from source + config + hashes.

## What belongs in ChatGPT milestone suites

Create and deliver a full suite in chat when there is a substantial milestone, including:

- a new frozen scientific phase;
- a substantial code/engine redesign;
- completion of a major computation;
- a manuscript-level revision after the evidence supports one;
- an adversarial audit/closure package;
- anything needed for clean local execution that GitHub cannot conveniently carry.

Record the suite filename and SHA-256 in `artifacts/MILESTONE_ARTIFACTS.md` so GitHub and chat remain congruent.

## Commit cadence

Group mechanical/documentation changes into logical commits. Do not commit every tiny edit separately.

Scientific-rule changes are different: document the change, why it is necessary, what prior state it supersedes, and whether it is pre-result or post-result. Failed branches remain archived and are never rewritten into success.

## Status protocol

`notes/BUILD_STATUS.md` is the canonical handoff file. It should always state:

- current scientific status;
- latest completed computation;
- current blocker, if any;
- exact next computational/scientific step;
- exact user action only when one is genuinely required.

## Reviewer and submission protocol

`reviewer/README.md` is the reviewer-facing entry point for the active GRI v2 program. It should provide a short evidence ladder and direct routes to the scientific definitions, code, tests, compact outputs, audits, and artifact registry.

A moving development branch is never the sole record cited for a submitted manuscript or data release. At submission time:

- create a new immutable tag/release for the exact submitted state;
- record the exact commit SHA;
- map manuscript claims to configs, code, tests, outputs, hashes, audits, figures, and tables;
- preserve a figure/table provenance map;
- preserve source-data identity and verification information;
- record the relevant test/CI state;
- include failed, null, deferred, exploratory, and explicit non-claims relevant to the submission;
- never move or rewrite an existing submission tag when revising a paper; create a new versioned snapshot instead.

The standing packaging checklist is `reviewer/SUBMISSION_RELEASE_CHECKLIST.md`. The current machine-readable stage/navigation record is `reviewer/REVIEWER_MANIFEST.json`.

## Data policy

Never commit the 1.882 GB PanCanAtlas expression matrix. Verify it by the frozen byte size and SHA-256 in `inputs/SOURCE_RUN.json`.

Large derived outputs should be committed only when they are necessary for reproducibility and not cheaply regenerable. Otherwise retain their hashes and generation recipe.
