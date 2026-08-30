# GRI v2 claim-to-evidence map

This map is intentionally conservative. It connects current admissible statements to the exact records that support them and marks pending or forbidden promotion steps explicitly.

## Evidence map

| Topic | Current admissible statement | Status | Frozen/preregistered definition | Implementation / tests | Compact result | Audit / interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| Historical `CV/2` scalar | Historical scalar is reconstructable as a descriptive comparator, but is not biological chi and did not survive the construction-aware promotion standard | Closed, not promoted | historical provenance in milestone registry | archived implementation/provenance | archived | `../artifacts/MILESTONE_ARTIFACTS.md` |
| Static RNA variability/lineage | `V` and `L` are retained as static RNA observables, not damping coordinates | Closed development layer | Stage A plans | Stage A code/tests | retained Stage A outputs | `../docs/STAGE_A1_AUDIT_20260829.md` |
| Hallmark organization | `C_in` and `C_out` provide a reproducible static Hallmark-network map; they are not a master score or dynamical mechanism | Closed development layer | `../config/stage_a1_plan.json` | `../src/module_network.py`, accelerated implementation, Stage A tests | Stage A/A1.1 outputs | Stage A audits |
| Finite-sample construction | Fixed-`n=30`, 100-resample calibration controls sample-size inflation while preserving the development topology | Closed | `../config/stage_a1_1_calibration_plan.json` | `../src/run_stage_a1_1.py`; contract test | `../development_outputs/stage_a1_1/` | `../docs/STAGE_A1_1_AUDIT_20260829.md` |
| Purity/leukocyte context | Independent purity and methylation-derived leukocyte fraction explain a concentrated portion of the RNA geometry without erasing the broader topology | Closed | `../config/stage_b1_context_adjustment_plan.json` | B1 implementation/tests | `../development_outputs/stage_b1/` | `../docs/STAGE_B1_AUDIT_20260829.md` |
| B2 source provenance | Genomic and RPPA sources were reserved/audited before biological association testing | Closed | `../config/stage_b2_source_plan.json` | source probe/tests | `../development_outputs/stage_b2/` | `../docs/STAGE_B2_SOURCE_AUDIT_20260829.md` |
| B2 integration rules | Genomic coordinates, RPPA rules, construction nulls, and integration logic were frozen before target B2 association results | Frozen historical contract | `../config/stage_b2_integration_plan.json` | B2 code/tests | n/a | `../docs/STAGE_B2_PREREGISTRATION_20260829.md` |
| Orthogonal RPPA coupling | Patient-aligned Hallmark RNA eigengenes show positive specific coupling to the fixed RPPA panel above the block-permutation floor across eligible cancers; static and non-causal | Closed | B2 integration plan | `../src/run_stage_b2_rppa.py`; RPPA test | `../development_outputs/stage_b2_rppa/` | `../docs/STAGE_B2_RPPA_AUDIT_20260829.md` |
| Genomic decomposition | Five documented genomic coordinates produce small distributed residualization effects while preserving almost all Hallmark module ordering, including beyond B1 composition | Closed | `../config/stage_b2_integration_plan.json` | genomic/resume implementations and tests | `../development_outputs/stage_b2_genomic/STAGE_B2_GENOMIC_SUMMARY.json` | `../docs/STAGE_B2_GENOMIC_AUDIT_20260830.md` |
| Static multiomic integration | RNA topology, composition effects, genomic decomposition, and orthogonal protein coupling form a layered static architecture; no master score is fitted | Closed architecture | closed component contracts | no new outcome-fitting implementation | closed component outputs | `../docs/STAGE_B2_STATIC_INTEGRATION_CLOSURE_20260830.md` |
| Stage C0 methylation source identity | The exact publication-era merged HM27/HM450 source, platform representation, file identity, 22,601-probe expectation, matching rules, and allowed source/schema operations were frozen before methylation acquisition/association; the live endpoint size has been independently confirmed | **Frozen; local source audit next** | `../config/stage_c0_methylation_source_plan.json` | `../src/probe_stage_c0_methylation.py`; `../tests/test_stage_c0_methylation_contract.py`; CI run `33292691811` | no biological result | `../docs/STAGE_C0_METHYLATION_PREREGISTRATION_20260830.md` |
| Methylation biological relationship | No methylation-RNA/protein/genomic/outcome relationship is yet admitted | Not started | annotation + Stage C1 analysis protocol must be frozen after C0 and before association | not yet implemented | none | prospective |
| Modal + scalar + conglomeration | The next biological substrate protocol must retain mode-resolved structure, licensed scalar coordinates, and whole-system/conglomeration organization as complementary views | Prospective design constraint | encoded in C0 contract and existing B2 closure | C1 pending | none | C0 preregistration + B2 static closure |
| Substrate inheritance | Static cross-assay architecture is insufficient to establish inheritance; ordered/temporal evidence is required | Not promoted | future ordered/temporal protocol required | future | none | active epistemic boundary |
| Biological chi | No biological chi coordinate has been admitted from these static datasets | Not admitted | `../docs/CHI_ADMISSION_RULES.md` | future dynamic benchmark only | none | `../docs/EPISTEMIC_CONSTITUTION.md` |

## Promotion rule

A manuscript claim cannot be stronger than the highest closed evidentiary row that directly supports it. In particular:

- static cross-sectional coordinates do not become dynamical rates by interpretation;
- correlation or orthogonal-assay coupling does not establish causal control;
- a construction-null result does not establish universality;
- the completed genomic branch supports weak distributed static decomposition, not a genomic master organizer;
- the integrated B2 architecture does not establish substrate inheritance;
- C0 source/schema validation cannot establish a methylation mechanism or cross-assay relationship;
- a scalar compression, if later useful, must preserve the modal carrier and system-level organization it summarizes rather than replacing them by assumption;
- any biological chi claim requires the separate dynamic admission gate.

## Modal + scalar + conglomeration reporting rule

Whenever a future compressed scalar is introduced, reviewers must be able to trace it to both:

1. **modal structure:** the underlying eigenmode/eigenspectrum or other mode-resolved carrier; and
2. **conglomeration/system organization:** the module, network, or integrated system architecture being summarized.

A scalar is a compressed coordinate, not the whole state. Modal structure, scalar summaries, and conglomeration-level organization should be reported together whenever the data support all three.
