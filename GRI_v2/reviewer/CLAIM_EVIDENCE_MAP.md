# GRI v2 claim-to-evidence map

This map is intentionally conservative. It connects current admissible statements to the repository records that support them and marks pending or forbidden promotion steps explicitly.

## Evidence map

| Topic | Current admissible statement | Status | Frozen/preregistered definition | Implementation / tests | Compact result | Audit / interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| Historical `CV/2` scalar | The historical scalar experiment can be reconstructed as a descriptive comparator, but it is not admitted as biological chi and did not survive the construction-aware promotion standard | Closed, not promoted | historical provenance recorded in milestone registry | archived historical implementation/provenance | archived milestone outputs | `../artifacts/MILESTONE_ARTIFACTS.md` and active-program summary in `../README.md` |
| Static RNA variability/lineage | `V` and `L` are retained as static RNA observables, not damping coordinates | Closed development measurement layer | Stage A plans under `../config/` | Stage A/A1 code under `../src/`; contracts under `../tests/` | Stage A compact outputs where retained | `../docs/STAGE_A1_AUDIT_20260829.md` |
| Hallmark internal/external organization | `C_in` and `C_out` provide a reproducible static Hallmark-network map; they are not a master stability score or dynamical mechanism | Closed development measurement layer | `../config/stage_a1_plan.json` | `../src/module_network.py`, `../src/module_network_accel.py`, Stage A tests | Stage A/A1.1 compact outputs | `../docs/STAGE_A1_AUDIT_20260829.md` |
| Finite-sample construction | Fixed-`n=30`, 100-resample calibration removes sample-size inflation in absolute-correlation magnitude while preserving the retained network topology sufficiently for the development map | Closed | `../config/stage_a1_1_calibration_plan.json` | `../src/run_stage_a1_1.py`; `../tests/test_stage_a1_1_contract.py` | `../development_outputs/stage_a1_1/` | `../docs/STAGE_A1_1_AUDIT_20260829.md` |
| Purity/leukocyte context | Independent tumor purity and methylation-derived leukocyte fraction explain a concentrated portion of the RNA network geometry, particularly immune/inflammatory modules, without erasing the broader topology | Closed | `../config/stage_b1_context_adjustment_plan.json` | `../src/run_stage_b1.py`, `../src/summarize_stage_b1.py`; B1 tests | `../development_outputs/stage_b1/` | `../docs/STAGE_B1_AUDIT_20260829.md` |
| B2 source provenance | The small genomic and RPPA sources used for B2 were reserved and audited before biological association testing | Closed | `../config/stage_b2_source_plan.json` | `../src/probe_stage_b2_sources.py`; source-contract tests | `../development_outputs/stage_b2/` | `../docs/STAGE_B2_SOURCE_AUDIT_20260829.md` |
| B2 integration rules | Genomic coordinates, RPPA panel rules, construction nulls, and integration logic were frozen before target B2 association results | Frozen | `../config/stage_b2_integration_plan.json` | B2 implementation and contract tests | n/a, preregistration record | `../docs/STAGE_B2_PREREGISTRATION_20260829.md` |
| Orthogonal RPPA coupling | Patient-aligned Hallmark RNA eigengenes show positive specific coupling to the fixed RPPA panel relative to the block-permutation construction null across the completed eligible cancers; the layer remains static and non-causal | Closed | B2 integration plan and RPPA source rules | `../src/run_stage_b2_rppa.py`; `../tests/test_stage_b2_rppa.py` | `../development_outputs/stage_b2_rppa/` | `../docs/STAGE_B2_RPPA_AUDIT_20260829.md` |
| Genomic decomposition | Five documented genomic coordinates produce small distributed residualization effects relative to the same-patient permuted-coordinate null while preserving almost all Hallmark module ordering; comparable bounded effects remain in the prespecified increment-beyond-B1 branch | Closed | `../config/stage_b2_integration_plan.json` | `../src/run_stage_b2_genomic.py`, `../src/run_stage_b2_genomic_resume.py`; genomic tests | `../development_outputs/stage_b2_genomic/STAGE_B2_GENOMIC_SUMMARY.json` | `../docs/STAGE_B2_GENOMIC_AUDIT_20260830.md` |
| Static multiomic integration | RNA topology, composition effects, genomic decomposition, and orthogonal protein coupling are retained as distinct but related static layers; no master stability score is admitted | Active closure step | B2 frozen design plus closed stage audits | no new outcome-fitting implementation yet | closed component outputs | `../README.md` and `../notes/BUILD_STATUS.md` |
| Genome-wide methylation | Acquisition/harmonization remains behind an independent gate; no genome-wide methylation result is currently promoted | Deferred | source/defer rules in current B2 records | no promoted genome-wide analysis | none | current status in `../README.md` and `../notes/BUILD_STATUS.md` |
| Biological chi | No biological chi coordinate has been admitted from these static datasets | Not admitted | `../docs/CHI_ADMISSION_RULES.md` | future dynamic benchmark only | none | `../docs/EPISTEMIC_CONSTITUTION.md` |

## Promotion rule

A manuscript claim should not be stronger than the highest closed evidentiary row that directly supports it. In particular:

- static cross-sectional coordinates do not become dynamical rates by interpretation;
- correlation or orthogonal-assay coupling does not establish causal control;
- positive results against a construction null do not establish universality;
- the completed genomic branch supports only weak distributed static decomposition, not a genomic master organizer;
- a scalar compression, if later useful, must preserve the modal carrier and system-level organization it summarizes rather than replacing them by assumption;
- any future biological chi claim requires the separate dynamic admission gate.

## Modal + scalar + conglomeration reporting rule

Where the investigation later introduces a compressed scalar coordinate, reviewers should be able to trace it back to both:

1. **modal structure**: the underlying eigenmode/eigenspectrum or other mode-resolved carrier; and
2. **conglomeration/system organization**: the module, network, or integrated system-level architecture from which the scalar is summarized.

A scalar is therefore treated as a compressed coordinate, not the whole state. Modal structure, scalar summaries, and conglomeration-level organization are complementary views and should be reported together whenever the data support all three.
