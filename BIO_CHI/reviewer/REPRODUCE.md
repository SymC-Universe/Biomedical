# Reproducing the Bio Chi investigation

This is the reviewer-facing reproducibility entry point for the active Bio Chi P0-D/P0-Q lineage.

**Current scientific ceiling:** P0-Q model-specific Bio Chi qualification in the NF-kB reference system plus independent ERK transport testing. NF-kB has model-specific `chi_bio`, `Chi_bio`, and Bio Chi admissions at P0-Q. ERK supports transport of the mode-specific `chi_bio` representation class but refuses complete `Chi_bio` admission under two distinct frozen modal gates. No P1 biological law, universal numeric chi, chi=1 biological boundary, or cross-system Bio Chi admission is claimed.

Working manuscript prose is intentionally private. The public repository contains the scientific contracts, source identities, code, controls, failures/refusals, workflow provenance, and executable verification paths needed to audit the work.

## Checkout

~~~bash
git clone https://github.com/SymC-Universe/Biomedical.git
cd Biomedical
git checkout bio-chi-erk-modal-v2-p0q-20260924
~~~

For any released manuscript claim, use the exact release commit/tag and SHA-256 manifest named by that release rather than the moving research branch.

## V1 — governance, nomenclature, and manuscript privacy

**[CLAIM]** The active Bio Chi lineage is governed by GOM v0.8.6 together with the later project-specific three-object nomenclature decision: `χ_bio` scalar, `Chi_bio` modal/vector, and Bio Chi conglomerate/system. The program-wide `χ` symbol is not a fourth biological object. The lineage has a durable continuation queue/checkpoint and excludes working-manuscript drafts from the public Bio Chi tree.

~~~bash
python BIO_CHI/src/validate_control.py
~~~

Expected terminal status:

~~~text
BIO_CHI_CONTROL_PASS
~~~

Primary inputs:
- BIO_CHI/control/WORK_QUEUE.json
- BIO_CHI/control/AUTORUN_CHECKPOINT.md
- BIO_CHI/reviewer/MANUSCRIPT_PRIVACY_FIREWALL.md
- GRI_v2/docs/CHI_BIO_NOMENCLATURE_AND_JOINT_TARGET_20260922.md

## V2 — generic public-source endpoint preflight

**[CLAIM]** Declared public source endpoints in the opening Bio Chi source manifest are mechanically reachable without opening biological target outcomes.

~~~bash
python BIO_CHI/src/preflight_sources.py
~~~

Expected terminal status:

~~~text
BIO_CHI_SOURCE_PREFLIGHT_PASS
~~~

Output: BIO_CHI/artifacts/generated/source_preflight_v0_1.json.

This is an endpoint/provenance check only. It does not validate a scientific result.

## V3 — Blum 2019 exact processed-archive identity

**[CLAIM]** Mendeley Data Version 2 for Blum et al. 2019 resolves through the supported public-files API to one exact data.zip whose frozen SHA-256 is 8bbd1ead46b5bb6b676bd47a5f415fdd790840a9c726321dc5c209b9c527bc62.

~~~bash
python BIO_CHI/src/freeze_blum_mendeley_source_v0_2.py
~~~

Expected terminal status:

~~~text
BIO_CHI_BLUM_MENDELEY_SOURCE_FREEZE_V02_PASS
~~~

Pinned result: BIO_CHI/config/BLUM2019_MENDELEY_SOURCE_FREEZE_V02_RESULT_PIN.json.

The freeze verifies archive bytes without opening member contents.

## V4 — Blum archive schema-only inventory

**[CLAIM]** The hash-pinned Blum archive can be enumerated at ZIP-directory level without reading member payloads.

~~~bash
python BIO_CHI/src/inventory_blum_mendeley_archive_v0_1.py
~~~

Expected terminal status:

~~~text
BIO_CHI_BLUM_SCHEMA_INVENTORY_PASS
~~~

Expected current inventory summary:
- archive SHA-256: 8bbd1ead46b5bb6b676bd47a5f415fdd790840a9c726321dc5c209b9c527bc62
- members: 103
- member_payloads_read: false

## V5 — Blum published-input mapping and Limit-Map refusal

**[CLAIM]** The public Figure-1 source package explicitly maps EKAR trajectories, condition grouping, and pulse-channel metadata, but the public article/supplement does not fully specify the histogram construction needed to claim an exact reproduction of the published Jeffries-Matusita Figure-1H result.

~~~bash
python BIO_CHI/src/map_blum_native_metric_inputs_v0_1.py
~~~

Expected terminal status:

~~~text
BIO_CHI_BLUM_NATIVE_INPUT_MAPPING_PASS
~~~

Expected source headers include:
- intensity_ekar,realtime,group.idx,id,fov
- group,group.idx
- fov,intensity_pulse,realtime,group.idx

Adjudication pin: BIO_CHI/config/BLUM2019_NATIVE_METHOD_QUALIFICATION_PIN_v0_1.json.

Expected disposition:

~~~text
EXACT_NATIVE_METRIC_REPRODUCTION_BLOCKED_METHOD_UNDERSPECIFIED
~~~

This refusal is part of the Limit Map. A reviewer should not substitute an arbitrary histogram binning rule and call it the published implementation.

## V6 — Harmange and Shaffer metadata-only source lineage

**[CLAIM]** Hash-pinned GEO metadata resolves the Harmange GSE237228 and Shaffer GSE97682 source lineages without reading molecular values or cell-level metadata rows.

~~~bash
python BIO_CHI/src/audit_geo_lineage_metadata_v0_1.py
~~~

Expected terminal status:

~~~text
BIO_CHI_GEO_LINEAGE_METADATA_AUDIT_PASS
~~~

Pinned result: BIO_CHI/config/P0D_GEO_LINEAGE_METADATA_V01_RESULT_PIN.json.

Current source-level expectations:
- Harmange: GSE237228 → PRJNA994430, 22 GEO samples with explicit SRA experiment links.
- Shaffer: GSE97682 → GSE97679/GSE97680/GSE97681 + PRJNA382641, 155 GEO samples with explicit SRA experiment links.
- molecular values read: false.

## V7 — Lee 2014 public SRA run map

**[CLAIM]** Paper-reported SRP040309 resolves reproducibly to 19 public paired-end RNA-seq runs under PRJNA241034 without downloading sequence reads.

~~~bash
python BIO_CHI/src/map_lee2014_sra_source_v0_1.py
~~~

Expected terminal status:

~~~text
BIO_CHI_LEE2014_SRA_SOURCE_MAP_PASS
~~~

Pinned result: BIO_CHI/config/LEE2014_SRP040309_SOURCE_MAP_V01_RESULT_PIN.json.

Current expected count: 19 runs.

## V8 — Lee 2014 sample/state metadata and recovery-source limitation

**[CLAIM]** Public SRP040309 metadata explicitly identifies untreated, stressed, and drug-tolerant RNA-seq states, but contains no explicitly labeled reconverted/post-withdrawal RNA state.

~~~bash
python BIO_CHI/src/map_lee2014_sample_metadata_v0_1.py
~~~

Expected terminal status:

~~~text
BIO_CHI_LEE2014_SAMPLE_METADATA_PASS
~~~

Pinned result: BIO_CHI/config/LEE2014_SRA_SAMPLE_METADATA_V01_RESULT_PIN.json.

Expected current source-level state counts:
- single-cell: 5 untreated, 5 stressed, 5 drug-tolerant
- bulk: 1 untreated, 1 stressed, 2 drug-tolerant
- explicitly labeled reconverted/post-withdrawal RNA samples: 0

This does not claim that biological reconversion is absent. It means the public SRP040309 RNA deposit is not itself a direct transcriptomic recovery trajectory.

## V9 — BioProject parent/child SRA provenance reconciliation

**[CLAIM]** Harmange and Shaffer public SRA identities can be reconciled without flattening parent/child BioProject structure or opening molecular outcomes.

~~~bash
python BIO_CHI/src/reconcile_bioproject_sra_v0_2.py
~~~

Expected terminal status:

~~~text
BIO_CHI_BIOPROJECT_SRA_RECONCILIATION_V02_PASS
~~~

Pinned result: BIO_CHI/config/P0D_BIOPROJECT_SRA_RECONCILIATION_V02_RESULT_PIN.json.

Expected current provenance:
- Harmange: PRJNA994430 → SRP449288 → 23 SRA runs.
- Shaffer umbrella query PRJNA382641 → SRP103825 / SRP103827 / SRP103828 → child BioProjects PRJNA382674 / PRJNA382752 / PRJNA382753 → exact 155-run union.
- missing/extra runs in child union: 0/0.

The v0.1 hierarchy failure remains pinned separately and is not erased.

## V10 — Su 2026 M397 native-method source metadata

**[CLAIM]** The prospectively frozen 15-point M397 RNA trajectory is present in hash-verified GSE255671 metadata and its public processing route can be identified without opening expression values or computing surprisal/hysteresis.

~~~bash
python BIO_CHI/src/audit_su_native_source_metadata_v0_1.py
~~~

Expected terminal status:

~~~text
BIO_CHI_SU_NATIVE_SOURCE_METADATA_PASS
~~~

Pinned result: BIO_CHI/config/SU2026_NATIVE_METHOD_SOURCE_METADATA_V01_RESULT_PIN.json.

Expected current source facts:
- expected M397 RNA GSMs: 15
- missing GSMs: 0
- expression_values_read: false
- surprisal_computed: false

Public analysis-code identity is pinned in BIO_CHI/config/SU2026_PUBLIC_CODE_PIN_v0_1.json. This verification does not reproduce the biological hysteresis result and does not create a new hysteresis scalar.

## V11 — master smoke test

**[CLAIM]** The current public Bio Chi evidence spine is internally consistent with the active nomenclature, privacy rule, source pins, NF-kB model-specific P0-Q admissions, preserved ERK v1/v2 refusals, and current cross-system claim ceiling.

~~~bash
python BIO_CHI/src/reviewer_smoke_test.py
~~~

Expected terminal status:

~~~text
BIO_CHI_REVIEWER_SMOKE_PASS
~~~

The smoke test chains the current pinned control assertions, including the NF-kB three-object state and both ERK modal refusals. It does not upgrade self-consistency into independent biological validation.

## V12 — ERK B3 modal lineage and v1 Limit Map

**[CLAIM]** The first ERK complete-modal nonlinear qualification failed under its frozen eight-direction rule even though every frozen FRET-visible complex-pair lane passed. That failure is preserved as a Limit Map and is not overwritten by the later v2 lineage.

~~~bash
python BIO_CHI/src/run_blum_b3_local_nonlinear_roundtrip_v01.py
~~~

Expected scientific status in the generated JSON:

~~~text
FAIL_B3_FULL_MODAL_LOCAL_ROUNDTRIP
~~~

Pinned result:
- `BIO_CHI/config/BLUM_B3_LOCAL_NONLINEAR_ROUNDTRIP_V01_RESULT_PIN.json`
- `BIO_CHI/config/ERK_B3_LIMIT_MAP_V01.json`

Current preserved v1 failing source-stoichiometric columns:
- primary FGF 2.5: 4, 6, 10, 14
- primary FGF 250: 10, 12, 14
- sensitivity FGF 2.5: 6, 10, 14
- sensitivity FGF 250: 10, 12, 14

This result limits complete arbitrary-direction local linear adequacy. It does not erase the generator-derived scalar factors.

## V13 — ERK invariant-modal v2 qualification

**[CLAIM]** After v1 was frozen as a limit, a separately frozen P0-Q lineage tested every natural invariant modal carrier of the same qualified 8D ERK generator using the same primary amplitude-convergence rule. The v2 test also refuses complete ERK `Chi_bio` admission.

~~~bash
python BIO_CHI/src/run_erk_b3_invariant_modal_v2.py
~~~

Expected terminal scientific status:

~~~text
FAIL_ERK_COMPLEX_SUBSPACE_ROUNDTRIP_V2
~~~

Pinned result:
`BIO_CHI/config/ERK_B3_INVARIANT_MODAL_V2_RESULT_PIN.json`

Expected frozen summary:
- direction tests: 64
- directions passing: 52
- carrier-context records: 25
- carrier-context records passing: 15
- real-mode directions: 26/36 pass
- complex-pair directions: 26/28 pass
- the two complex-pair direction failures occur only in the frozen FGF=250 contexts

The v2 failure does not retroactively change v1. It establishes a second, distinct boundary: local nonlinear adequacy is not uniform even across every frozen natural invariant carrier direction at the tested perturbation scales.

## V14 — complete ERK lineage disposition

**[CLAIM]** The complete ERK B3 lineage preserves the source/native-model qualification, finite-difference generator refusal, analytic-generator repair, scalar-class transport, v1 modal limit, v2 invariant-modal refusal, and the resulting three-object claim ceiling without collapsing these outcomes into one score.

~~~bash
python BIO_CHI/src/reviewer_smoke_test.py
~~~

Expected terminal status:

~~~text
BIO_CHI_REVIEWER_SMOKE_PASS
~~~

Canonical lineage records:
- machine-readable: `BIO_CHI/config/ERK_B3_MODAL_LINEAGE_V01.json`
- reader-facing: `BIO_CHI/docs/ERK_B3_MODAL_LINEAGE_RECORD_20260924.md`

Current disposition:

~~~text
chi_bio: cross-system representation class supported at P0-Q, with explicit ERK directional nonlinear limits
Chi_bio: NF-kB model-specific admitted; ERK generator precursor qualified; ERK v1 and v2 admissions refused
Bio Chi: NF-kB model-specific admitted; ERK cross-system transport not opened
P1 confirmation: not claimed
~~~

## Reproducibility levels and claim ceiling

The exact demonstrated level must be stated beside each future promoted result. Source identity, same-code reproducibility, known-truth qualification, and independent biological validation are different evidence classes and are not interchangeable.

Current branch-level rule:

~~~text
source qualification != scientific validation
model self-consistency != biological validation
native-model reproduction != chi_bio admission
mode-specific chi_bio transport != complete Chi_bio transport
modal generator qualification != nonlinear modal admission
NF-kB Bio Chi admission != cross-system Bio Chi transport
cross-layer association != Stability Inheritance
~~~

Failures, refusals, indeterminate results, access limitations, and representation failures remain part of the evidence record rather than being deleted when later steps succeed.
