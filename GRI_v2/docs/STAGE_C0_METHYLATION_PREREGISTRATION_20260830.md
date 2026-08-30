# Stage C0 DNA-methylation source gate preregistration

Date: 2026-08-30

Status: **FROZEN AFTER STAGE B2 STATIC CLOSURE AND BEFORE DNA-METHYLATION DOWNLOAD OR BIOLOGICAL ASSOCIATION**

## Purpose

Stage C0 is a source-integrity and coverage gate for the pre-reserved PanCanAtlas DNA-methylation substrate layer. It does **not** test whether methylation agrees with RNA, RPPA, copy-number burden, clinical outcomes, treatment response, historical GRI variables, or any preferred SymC pattern.

The reason for separating C0 from the later biological analysis is methodological: the methylation representation, platform handling, sample matching, source identity, and probe inventory must be fixed and audited before any methylation association result can steer those choices.

Machine-readable contract: `config/stage_c0_methylation_source_plan.json`.

## Frozen primary source

Primary source:

- file: `jhu-usc.edu_PANCAN_merged_HumanMethylation27_HumanMethylation450.betaValue_whitelisted.tsv`
- GDC publication UUID: `d82e2c44-89eb-43d9-b6d3-712732bf6a53`
- GDC open-manifest size: `5,022,150,019` bytes
- GDC open-manifest MD5: `5cec086f0b002d17befef76a3241e73b`
- publication-era feature count expected from the PanCanAtlas processing description: `22,601` shared HM27/HM450 probes

The NCI GDC PanCanAtlas publication page identifies this file as the merged 27K+450K DNA-methylation supplemental matrix. The matching GDC open-data manifest supplies the frozen UUID, byte size, and MD5.

The primary processing description is Hoadley et al., *Cell* 2018, DOI `10.1016/j.cell.2018.03.022`. The PanCanAtlas methylation construction merged HM27 and HM450 measurements on probes shared by both platforms, rescaled HM27 values probe-by-probe against HM450 using repeated technical controls, and then removed 779 probes that retained a systematic platform difference of at least 0.1 in six or more tumor types. The resulting shared representation contains 22,601 probes.

## Platform handling frozen before acquisition

The primary C0/C1 representation is the **publication-era merged PanCanAtlas matrix as supplied**.

Stage C0 will not re-normalize the merged matrix and will not replace it with the current GDC SeSAMe-reharmonized methylation representation. This is not a claim that newer harmonization is inferior. It is a provenance decision that keeps the methylation layer aligned with the publication-freeze RNA, RPPA, genomic, purity, and leukocyte sources already used in Stages A-B2.

A newer re-harmonized representation may be tested later only as a separately specified robustness analysis. It may not silently replace the primary representation after results are seen.

## 450K-only source

The higher-density 450K-only PanCanAtlas matrix remains robustness-only:

- file: `jhu-usc.edu_PANCAN_HumanMethylation450.betaValue_whitelisted.tsv`
- GDC publication UUID: `99b0c493-9e94-4d99-af9f-151e46bab989`
- GDC open-manifest size: `41,541,692,788` bytes
- GDC open-manifest MD5: `a92f50490cf4eca98b0d19e10927de9d`

It will not be downloaded as part of C0. A later robustness use requires a separate prospective justification because it changes both feature density and the platform-eligible sample set.

## Frozen Stage C0 operations

C0 may perform only the following operations:

1. inspect the GDC `/data/{uuid}` endpoint without downloading the file and require the frozen content length;
2. download the exact primary file with restart/resume support;
3. require exact byte length and the GDC-manifest MD5;
4. calculate and record a SHA-256 for the acquired file;
5. parse the header to inventory TCGA sample identifiers;
6. require exactly 22,601 nonblank, unique probe rows;
7. match eligible primary-tumor methylation samples to the frozen Stage A sample universe using the established sample-root rule;
8. report per-cancer matched coverage and the existing `n >= 30` eligibility count;
9. retain only source/schema/coverage outputs.

C0 does not need to load the 5.02 GB matrix into memory. Probe inventory is streamed from disk.

## Frozen sample matching

The matching hierarchy remains the same one already used in the multiomic program:

1. exact TCGA sample root through vial, for example `TCGA-XX-YYYY-01A`;
2. patient-level fallback only when the external methylation source contains exactly one eligible primary measurement for that patient;
3. sample type `01` only;
4. no metastatic, recurrent, or normal sample substitution to rescue a cancer below the coverage gate.

The frozen Stage A profile cache SHA-256 is:

`e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`

A different cache does not satisfy C0.

## What C0 is forbidden to inspect

Before C0 is closed, the methylation matrix may not be used to calculate or select:

- methylation-RNA correlation;
- methylation-RPPA correlation;
- methylation-genomic-burden association;
- survival, treatment, subtype, or other outcome association;
- high-variance or high-correlation probes chosen because they produce a preferred biological result;
- Hallmark-specific methylation scores;
- a composite stability score;
- `CV/2`;
- a biological chi coordinate;
- a substrate-inheritance claim.

Technical source/schema quantities such as file hashes, row counts, duplicate IDs, sample coverage, and missing identifiers are allowed.

## Annotation gate after C0

Stage C0 intentionally does not yet map probes into genes, promoters, CpG islands, Hallmarks, or regulatory modules.

After source closure, an annotation sub-stage must freeze the exact annotation source, genome build, transcript/gene resolution rule, multi-mapping handling, promoter/regulatory-region definition, and unmapped-probe handling **before any cross-assay association is calculated**.

No annotation rule may be chosen because it improves agreement with Stage A, B1, B2, or a methylation result.

## Required architecture of the later biological protocol

The post-C0 biological protocol must preserve the three complementary views of the substrate architecture:

- **modal:** mode-resolved methylation structure, eigenspectrum, and participation/loadings;
- **scalar:** compressed coordinates only where separately justified and calibrated;
- **conglomeration:** module-to-module and whole-system organization across independently defined layers.

A scalar summary may compress part of the architecture, but it may not replace the modal or conglomeration views. None of these static methylation quantities is chi.

## Claim ceiling

Stage C0 can establish only source identity, integrity, schema, probe inventory, and sample coverage.

Even a successful C0 does not establish regulatory causality, substrate inheritance, temporal ordering, damping, recovery, criticality, a phase/state transition, treatment response, an optimum, or biological chi.

## C0 outputs

The local source gate produces only compact outputs for return/review:

- `STAGE_C0_METHYLATION_SOURCE_SUMMARY.json`
- `stage_c0_methylation_cancer_coverage.csv`

The 5.02 GB source file remains local and is identified by MD5 and SHA-256. It is not committed to GitHub.
