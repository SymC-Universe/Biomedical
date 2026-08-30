# SymC Biomedical Repository

This repository contains biomedical research branches within the broader SymC program.

## Active oncology development on this branch

The `gri-v2` branch contains the active **GRI v2 / Cancer Stability Atlas** rebuild.

**Current status:** development program, not a validated cancer tool.  
**Current gate:** prospective substrate-extension design; Stage B2 static computation and integration are closed.  
**Reviewer entry point:** `GRI_v2/reviewer/README.md`.

The active GRI v2 program is deliberately separated from stronger historical oncology interpretations. The historical GRI manuscript and earlier SymC oncology work remain provenance and hypothesis history; they do not define the evidentiary status of the current rebuild.

In particular, the active program currently holds that:

- historical `CV/2` is a descriptive comparator and is **not** biological chi;
- no valid biological chi coordinate has yet been admitted;
- static RNA, genomic, protein, and composition observables remain distinct unless later model competition justifies a reduction;
- the completed genomic branch shows weak distributed static decomposition effects with strong preservation of the Hallmark topology, not a genomic master organizer;
- the completed RPPA branch shows reproducible patient-aligned RNA/protein coupling above its construction-null floor, but remains static and non-causal;
- the closed Stage B2 integration supports a layered static architecture, not causal substrate inheritance;
- `chi = 1` is not presumed to be a cancer optimum, healthy state, therapeutic target, or maximum-organization state;
- modal structure, scalar summaries, and conglomeration/system organization are complementary views; a scalar is not allowed to replace the richer structure by assumption;
- failed, null, deferred, and non-identifiable branches remain part of the record.

For the current scientific state, use the files under `GRI_v2/`, especially:

- `GRI_v2/README.md` - active scientific overview;
- `GRI_v2/reviewer/README.md` - reviewer navigation;
- `GRI_v2/reviewer/CLAIM_EVIDENCE_MAP.md` - claim-to-evidence mapping;
- `GRI_v2/notes/BUILD_STATUS.md` - canonical current handoff;
- `GRI_v2/docs/STAGE_B2_GENOMIC_AUDIT_20260830.md` - completed genomic audit;
- `GRI_v2/docs/STAGE_B2_STATIC_INTEGRATION_CLOSURE_20260830.md` - closed B2 cross-layer architecture;
- `GRI_v2/docs/EPISTEMIC_CONSTITUTION.md` - evidentiary guardrails;
- `GRI_v2/docs/CHI_ADMISSION_RULES.md` - requirements before any biological chi claim;
- `GRI_v2/artifacts/MILESTONE_ARTIFACTS.md` - artifact hashes and provenance.

## Other biomedical work

The repository also preserves earlier and parallel work in oncology, viral dynamics, neurodegeneration, pain, addiction, psychiatric stability, and related biomedical control questions. Those materials should be read according to their own version, status, and evidence records rather than treated as automatic support for GRI v2.

## Submission and review policy

The moving development branch is not intended to serve as the immutable record for a manuscript or data submission. Each future submission should point to an exact tagged/released snapshot with its own claim-to-evidence map, result hashes, figure/table provenance, source-data record, test/CI state, and null/failure/non-claim ledger.

See `GRI_v2/reviewer/SUBMISSION_RELEASE_CHECKLIST.md`.
