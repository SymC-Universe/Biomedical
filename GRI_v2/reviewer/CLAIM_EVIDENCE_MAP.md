# GRI v2 claim-to-evidence map

This map is intentionally conservative. It connects current admissible statements to the exact records that support them and marks pending or forbidden promotion steps explicitly.

## Evidence map

| Topic | Current admissible statement | Status | Frozen/preregistered definition | Implementation / tests | Compact result | Audit / interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| Historical `CV/2` scalar | Historical scalar is reconstructable as a descriptive comparator, but is not biological chi and did not survive the construction-aware promotion standard | Closed, not promoted | historical provenance in milestone registry | archived implementation/provenance | archived | `../artifacts/MILESTONE_ARTIFACTS.md` |
| Static RNA variability/lineage | `V` and `L` are retained as static RNA observables, not damping coordinates | Closed development layer | Stage A plans | Stage A code/tests | retained Stage A outputs | `../docs/STAGE_A1_AUDIT_20260829.md` |
| Hallmark organization | `C_in` and `C_out` provide a reproducible static Hallmark-network map; they are not a master score or dynamical mechanism | Closed development layer | Stage A plans | Stage A implementations/tests | Stage A/A1.1 outputs | Stage A audits |
| Finite-sample construction | Fixed-`n=30`, 100-resample calibration controls sample-size inflation while preserving the development topology | Closed | `../config/stage_a1_1_calibration_plan.json` | `../src/run_stage_a1_1.py`; contract test | `../development_outputs/stage_a1_1/` | `../docs/STAGE_A1_1_AUDIT_20260829.md` |
| Purity/leukocyte context | Independent purity and methylation-derived leukocyte fraction explain a concentrated portion of the RNA geometry without erasing the broader topology | Closed | `../config/stage_b1_context_adjustment_plan.json` | B1 implementation/tests | `../development_outputs/stage_b1/` | `../docs/STAGE_B1_AUDIT_20260829.md` |
| B2 source provenance | Genomic and RPPA sources were reserved/audited before biological association testing | Closed | `../config/stage_b2_source_plan.json` | source probe/tests | `../development_outputs/stage_b2/` | `../docs/STAGE_B2_SOURCE_AUDIT_20260829.md` |
| Orthogonal RPPA coupling | Patient-aligned Hallmark RNA eigengenes show positive specific coupling to the fixed RPPA panel above the block-permutation floor across eligible cancers; static and non-causal | Closed | B2 integration plan | `../src/run_stage_b2_rppa.py`; RPPA test | `../development_outputs/stage_b2_rppa/` | `../docs/STAGE_B2_RPPA_AUDIT_20260829.md` |
| Genomic decomposition | Five documented genomic coordinates produce small distributed residualization effects while preserving almost all Hallmark module ordering, including beyond B1 composition | Closed | `../config/stage_b2_integration_plan.json` | genomic/resume implementations and tests | `../development_outputs/stage_b2_genomic/STAGE_B2_GENOMIC_SUMMARY.json` | `../docs/STAGE_B2_GENOMIC_AUDIT_20260830.md` |
| Static multiomic integration | RNA topology, composition effects, genomic decomposition, and orthogonal protein coupling form a layered static architecture; no master score is fitted | Closed architecture | closed component contracts | no new outcome-fitting implementation | closed component outputs | `../docs/STAGE_B2_STATIC_INTEGRATION_CLOSURE_20260830.md` |
| Stage C0 methylation source identity | The exact publication-era merged HM27/HM450 source passed cryptographic identity, 22,601-probe integrity, header parse, and pan-cancer coverage gates | **Closed source-gate PASS** | `../config/stage_c0_methylation_source_plan.json` | `../src/probe_stage_c0_methylation.py`; C0 tests | `../development_outputs/stage_c0_methylation/` | `../docs/STAGE_C0_METHYLATION_AUDIT_20260830.md` |
| Stage C0.1 one-to-one sample identity | Duplicate primary roots are prospectively excluded rather than averaged/selected; 9,460/9,546 Stage A tumors remain strict one-to-one methylation matches and all 32 cancers remain above n=30 | **Closed PASS** | `../config/stage_c0_1_sample_identity_plan.json` | `../src/run_stage_c0_1_sample_identity.py`; `../tests/test_stage_c0_1_sample_identity.py` | `../development_outputs/stage_c0_1_sample_identity/` | `../docs/STAGE_C0_1_SAMPLE_IDENTITY_AUDIT_20260830.md` |
| C1A annotation/regulatory architecture | Illumina HM450 v1.2 / ilmn12.hg19, positional many-to-many probe-gene-region mapping, regulatory strata, unmapped handling, and primary-vs-technical-robustness tracks were frozen before any C1 beta-value association | **Closed frozen contract** | `../config/stage_c1_annotation_feature_plan.json`; `../docs/STAGE_C1A_ANNOTATION_PREREGISTRATION_20260830.md` | C1A source/inventory implementations and contract tests | exact source + probe inventory | C1A source and probe audits |
| C1A external annotation source identity | Exact Bioconductor 3.8 annotation v0.6.0 and pinned Chen cross-reactive source passed cryptographic/source-schema audit; deterministic `SNPs.147CommonSingle` selected from the frozen annotation package | **Closed external-source PASS** | C1A frozen contract | `../src/fetch_stage_c1a_sources.py`; `../src/export_stage_c1a_annotation.R`; source-gate CI | portable 485,512-probe annotation export; 29,233 Chen TargetIDs | `../docs/STAGE_C1A_ANNOTATION_SOURCE_AUDIT_20260830.md` |
| C1A exact 22,601-probe representation | All 22,601 exact PanCanAtlas probes match the frozen annotation; 22,469 are RefGene-mapped, 132 remain unmapped for gene/Hallmark purposes, and the prespecified technical-mask union removes 579 probes leaving 22,022 for mandatory robustness | **Closed PASS** | C1A frozen contract | `../src/run_stage_c1a_probe_inventory.py`; Windows wrapper/tests | `../development_outputs/stage_c1a_probe_inventory/` | `../docs/STAGE_C1A_PROBE_INVENTORY_AUDIT_20260830.md` |
| Stage C1 formula/null/promotion specification | Exact modal, scalar, conglomeration, missingness, resampling, seed, null, regulatory-stratum, multiplicity, and promotion rules must be approved before beta-value biology opens | **Active scientific gate — DRAFT not frozen** | `../docs/STAGE_C1_ANALYSIS_CONTRACT_DRAFT_20260830.md` | implementation blocked from biological execution until approval | none | pending explicit user approval |
| Methylation biological relationship | No methylation-RNA/protein/genomic/outcome relationship is yet admitted | Not started | Stage C1 analysis contract must become frozen before association | not yet implemented | none | prospective |
| Modal + scalar + conglomeration | Methylation analysis must retain mode-resolved structure, scalar compression derived from and traceable to the modal carrier, and gene/Hallmark/system conglomeration as complementary views | Frozen conceptual constraint; exact formulas pending approval | C1A contract + Stage C1 draft + epistemic rules | biological implementation blocked | none | active design boundary |
| Substrate inheritance | Static cross-assay architecture is insufficient to establish inheritance; ordered/temporal evidence is required | Not promoted | future ordered/temporal protocol required | future | none | active epistemic boundary |
| Biological chi | No biological chi coordinate has been admitted from these static datasets | Not admitted | `../docs/CHI_ADMISSION_RULES.md` | future dynamic benchmark only | none | `../docs/EPISTEMIC_CONSTITUTION.md` |

## Promotion rule

A manuscript claim cannot be stronger than the highest closed evidentiary row that directly supports it. In particular:

- static cross-sectional coordinates do not become dynamical rates by interpretation;
- correlation or orthogonal-assay coupling does not establish causal control;
- the completed genomic branch supports weak distributed static decomposition, not a genomic master organizer;
- the integrated B2 architecture does not establish substrate inheritance;
- C0 source/schema validation cannot establish a methylation mechanism or cross-assay relationship;
- C0.1 sample identity cannot establish methylation biology;
- C1A annotation/source/probe inventory cannot establish methylation biology;
- annotation or technical-mask choices may not be selected because they improve downstream agreement;
- primary and technical-mask robustness tracks must both be reported; a favorable-only track cannot drive promotion;
- secondary methylation regulatory strata may not be substituted for a failed primary stratum after results are seen;
- a scalar compression must preserve and remain traceable to the modal carrier and system-level organization it summarizes rather than replacing them by assumption;
- any biological chi claim requires the separate dynamic admission gate.

## Modal + scalar + conglomeration reporting rule

Whenever a compressed scalar is introduced, reviewers must be able to trace it to both:

1. **modal structure:** the underlying eigenmode/eigenspectrum or other mode-resolved carrier; and
2. **conglomeration/system organization:** the module, network, or integrated system architecture being summarized.

A scalar is a compressed coordinate, not the whole state. Modal structure, scalar summaries, and conglomeration-level organization should be reported together whenever the data support all three.


## 22 September 2026 current-state supersession addendum

The historical table above is retained as provenance for the earlier GRI v2 build sequence. The following rows supersede any earlier statement that Stage C1 or later architecture work is still "not started."

| Topic | Current admissible statement | Status | Current evidence / audit |
| --- | --- | --- | --- |
| Stage C1 methylation/RNA architecture | Historical Stage C1 completed under its frozen contract across 32 cancers and 9,457 shared eligible samples with 100 resamples per cancer. The result is a static preregistered methylation/RNA architecture, not biological damping or scalar chi. | **Closed historical development result** | `../artifacts/GRI_CONGLOMERATE_CHI_C1_CARRIER_CONTRACT_CLOSURE_20260918.md`; `../docs/GRI_C1_CARRIER_MATERIALIZATION_RECOVERY_BOUNDARY_20260922.md` |
| Patient-level heavy C1 carrier bytes | Exact full patient-level contribution arrays are provenance-identified but not currently available on the connected surface. Do not reconstruct them from summaries or rerun Stage C1 unless a future frozen task demonstrates that patient-level values are necessary. | **Execution/provenance boundary, not scientific failure** | `../docs/GRI_C1_CARRIER_MATERIALIZATION_RECOVERY_BOUNDARY_20260922.md` |
| Capital-Chi biological architecture | Capital Chi-bio is a typed multirepresentational carrier that preserves RNA/regulatory, epigenetic, modal/vector, temporal/contextual, uncertainty and refusal structure. It is not a master scalar. | **P0-D/P0-Q architecture** | `../docs/GRI_GOM_V083_CONTINUITY_AND_SOURCE_OF_RECORD_20260921.md`; `../docs/GRI_CHI_CAPITALCHI_JOINT_MEANING_INVESTIGATION_20260921.md` |
| SCC25 local scalar admission | The current chronic SCC25 weekly G2 representation does not license biological lowercase chi. Rank 2 has no complex pair; rank 3 pair structure is representation-dependent and no continuous generator/logarithm branch is independently licensed. | **Closed refusal for current representation** | `../docs/GRI_SCC25_G2_SCALAR_ADMISSION_POSTRESULT_AUDIT_20260922.md` |
| SCC25 joint local/modal <-> capital-Chi task | The next joint-meaning investigation must proceed through a no-scalar local/modal branch unless a future prospective derivation independently earns a scalar. Outcome-bearing execution is blocked until Decisions A-H are prospectively frozen. | **Scientific freeze required** | `../docs/GRI_SCC25_JOINT_MEANING_NEXT_SCIENCE_DECISION_PACKET_20260922.md` |
| External breast/prostate identity | Breast 72/72 expression samples crosswalk uniquely to methylation by patient/state; prostate 121/121 RNA samples crosswalk uniquely to 450K/EPIC methylation under frozen source-title rules. No GRI outcome was computed and no P1 cohort was selected. | **Source identity closed for metadata scope** | `../docs/GRI_EXTERNAL_GEO_IDENTITY_POSTRESULT_AUDIT_20260922.md` |
| External melanoma identity | The source family is inventoried but three Pt22-DDP title/description patient-identity conflicts remain quarantined. | **Source manifest complete with anomalies** | `../docs/GRI_EXTERNAL_GEO_IDENTITY_POSTRESULT_AUDIT_20260922.md` |
| External P1 confirmation | No external cohort is currently selected or frozen as decisive P1. The bottleneck is claim/representation maturity, not source discovery. | **Pre-confirmatory only** | `../docs/GRI_MFR14_EXTERNAL_CONFIRMATION_READINESS_20260916.md` |
| Biological scalar chi | No biological scalar chi is currently admitted in the active GRI program. Historical CV/2 remains descriptive/historical only; SCC25 G2 scalar admission is refused for the current representation. | **Not admitted** | `../docs/CHI_ADMISSION_RULES.md`; `../docs/GRI_SCC25_G2_SCALAR_ADMISSION_POSTRESULT_AUDIT_20260922.md` |
| Perturbation / recovery | Static TCGA organization is not recovery evidence. Any future perturbation/recovery claim must prospectively separate resistance, finite-time response, first reclaim, sustained recovery, reorganization, basin robustness and repeated-perturbation behavior. | **Prospective evidence layer** | `../docs/GRI_GOM_V083_CONTINUITY_AND_SOURCE_OF_RECORD_20260921.md` |

### Current manuscript ceiling

A reviewer-facing manuscript may now describe:
- the historical static multiomic architecture and its frozen qualifications;
- the development of a block-preserving capital-Chi architecture;
- explicit refusal of biological scalar chi where the generator does not license it;
- negative/representation-dependent SCC25 scalar-admission results;
- source-qualified external confirmation candidates and their unresolved independence/representation gates;
- the exact next falsifiable experiments and confirmation requirements.

It may **not** describe:
- a validated clinical diagnostic or prognostic tool;
- a universal cancer stability scalar;
- a cancer optimum at chi=1;
- static architecture as dynamic recovery;
- the current SCC25 operator as a continuous-time biological damping system;
- any external source as confirmed P1 before its claim/task/representation/comparator/falsifier freeze and untouched test.
