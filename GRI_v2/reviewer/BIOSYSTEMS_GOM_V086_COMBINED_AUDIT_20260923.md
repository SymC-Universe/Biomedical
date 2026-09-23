# BioSystems v18 GOM v0.8.6 combined paper-building audit

**Date:** 23 September 2026  
**Status:** SCIENCE PASS / PAPER-BUILDING REPAIR REQUIRED  
**GOM authority:** SymC General Operations Manual v0.8.6, Definitive Active Baseline  
**Current main:** `GRI_BioSystems_working_v18_R1_2026-09-23.tex/.pdf`  
**Current supplement:** `GRI_BioSystems_supplement_working_v15_R1_2026-09-23.tex/.pdf`  
**Current private archive:** `BioSystems_Resubmission_MeatBone_v18_20260923.zip`  
**Archive SHA-256:** `d72f6b3fdf9f138d6eda21ac610d2804dc69ba25f6581161c0b3847ea767a5e7`  
**Scientific snapshot:** `biosystems-meat-bone-v18-20260923`

This audit supersedes the earlier v0.8.4 audit. It applies the front-loaded paper-building standard in GOM v0.8.6 section 0.4, including the newly binding section-by-section lay-explanation gate and combined pre-final audit.

## Executive disposition

No new biological computation is required.

The scientific claim/evidence architecture remains acceptable under v0.8.6. The package must **not** be called GOM-final or submission-ready yet because the reader-facing paper-building layer and reproducibility presentation are incomplete.

The dominant blocker is 0.4.7: the current main and supplement contain **71 scientific headings** and no formal inline or consolidated lay-explanation layer. Every scientific heading is therefore `REPAIR_REQUIRED` until one-to-one coverage exists and passes the v0.8.6 comprehension gate.

## Scientific architecture

**PASS**
- native-model/statistical structure precedes SymC interpretation;
- no unlicensed biological chi is inserted;
- historical scalar chi_bio remains outside the current manuscript claim;
- H1, H2/H3a, H3b, P0, tumor-normal, and external P1 can succeed or fail separately;
- P0 remains below its promotion floor;
- post-result adversarial controls remain explicitly post-result and do not rewrite canonical confirmation;
- PCPG, H3b limits, missingness limits, five Hallmark refusals, external H2/H3a nontransport, and external RNA nonconfirmation remain visible;
- static tumor-normal contrasts are not promoted to recovery, temporal decline, treatment response, causality, or clinical utility;
- external prostate P1 remains partial transport rather than whole-framework replication;
- function and limit information are both retained;
- standard methods are acknowledged without an unsupported ADDS claim.

## Joint chi / Chi disposition

**PASS SCIENTIFICALLY / DOCUMENTATION POINTER NEEDED**

The current study does not admit a licensed biological scalar chi. The broader empirical architecture is partially supported. GOM 2.5.1 does not authorize inventing a scalar merely to make a joint analysis symmetrical. The project-level joint outcome is therefore:
- scalar chi_bio: NOT_ADMITTED in the tested historical lineage;
- broader architecture: partially supported as empirical molecular organization;
- joint chi/Chi interpretation: unresolved because the licensed scalar side is absent;
- smallest meaningful resolving path: a separately frozen dynamic/recovery lineage capable of testing whether a licensed scalar can be identified and whether it adds information to the broader architecture.

The current BioSystems paper should remain free of a manufactured chi claim. The release record should link the existing chi_bio closure/distance-to-admission records so the required joint-meaning disposition is explicit at project level.

## GOM 0.4.2 voice, punctuation, scope language

**PASS**
- no true first-person authorial prose was found; apparent single-letter hits are mathematical indices or author names;
- no em dash or en dash appears in manuscript/supplement prose;
- no reader-facing rc/release-candidate labels were found;
- uses of "universal" are scope-limiting negations, not universality claims;
- no table cell using a prose dash as a missing-value placeholder was detected in the current TeX.

## GOM 0.4.3 default source setup

**REPAIR_REQUIRED OR DOCUMENT VENUE OVERRIDE**

Main:
- 11pt article: PASS;
- current geometry: 0.55/0.72/0.72/0.72 in, not the 1-inch default;
- `booktabs`: present;
- `natbib`: absent; bibliography is manual;
- `hyperref`: present but not the canonical `hidelinks,pdfusetitle` default.

Supplement:
- 10pt article, not the 11pt default;
- geometry is 0.55/0.70/0.62/0.62 in;
- `booktabs`/longtable: present;
- `natbib`: absent.

The GOM permits venue mechanics to override these defaults, but no current package record documents a BioSystems/Elsevier requirement that explains the deviation. Either return the working source to the 0.4.3 defaults or record the exact venue override.

## GOM 0.4.4 table semantics

**PASS WITH CURRENT TABLE SET**
- longtable is used for the multi-page source-site table;
- no missing table cell encoded as a dash was detected;
- no blocked value is visually presented as an ordinary reportable number;
- grouped summaries use medians/ranges or explicit selection rules where material.

## GOM 0.4.5 structural references

**PASS**
- no undefined LaTeX `\ref`/autoref/pageref targets were found;
- no stale "Part III"/nonexistent-section pointer was detected;
- internal development labels such as rc identifiers do not appear reader-facing.

Five figure labels exist but are not referenced through `\ref`; that is not a broken cross-reference.

## GOM 0.4.6 self-consistency, numeric provenance, validation language

**PARTIAL / REPAIR_REQUIRED**

Validation language is appropriately bounded:
- internal/held-out/external evidence are distinguished;
- external H1 is not called magnitude replication;
- repeated draws are not called independent biological replicates;
- construction-null and stronger-null roles are separated.

Numeric provenance is not yet in canonical release form. The manuscript/supplement contain many scientific values whose source is recoverable from the project lineage, but v0.8.6 requires every reported scientific number to retain a traceable source/evidence tier in the paper, supplement, or directly linked reproducibility record. The current public reproducibility index is stale at the v12 binding and is not a claim-by-claim v18 numeric provenance map.

This can be closed in the v18 canonical reproducibility guide by mapping each headline claim/result family to:
- source artifact/run or table;
- evidence tier/class;
- exact verification command;
- expected output;
- current release identity.

## GOM 0.4.7 lay-explanation comprehension gate

**FAIL / BLOCKS FINALIZATION**

## 0.4.7 heading-by-heading lay coverage inventory

Current reader-facing source contains 23 scientific headings in the main and 48 in the supplement. No inline lay blocks and no consolidated `Lay Explanation Map` were found. Under GOM v0.8.6 section 0.4.7, every scientific heading below is therefore `REPAIR_REQUIRED` until a matching plain-language entry is added and audited for purpose, operation, meaning, importance, evidence, and limits.

### Main manuscript

| line | level | heading | status |
|---:|---|---|---|
| 36 | section | Introduction | REPAIR_REQUIRED |
| 45 | section | Methods | REPAIR_REQUIRED |
| 46 | subsection | Study design, sources, and upstream controls | REPAIR_REQUIRED |
| 51 | subsection | Prospectively frozen tumor-normal control | REPAIR_REQUIRED |
| 54 | subsection | Prospectively frozen independent prostate transport | REPAIR_REQUIRED |
| 59 | subsection | Stage C1 sources and analysis units | REPAIR_REQUIRED |
| 62 | subsection | H1: all-probe methylation spectral concentration | REPAIR_REQUIRED |
| 69 | subsection | H2 and H3: cross-layer patient and Hallmark correspondence | REPAIR_REQUIRED |
| 82 | subsection | Composition projection, inference, and adversarial sensitivities | REPAIR_REQUIRED |
| 86 | section | Results | REPAIR_REQUIRED |
| 87 | subsection | Upstream calibration and internal holdout set the claim ceiling | REPAIR_REQUIRED |
| 92 | subsection | H1 survives progressively stronger internal nulls | REPAIR_REQUIRED |
| 97 | subsection | H2/H3a show broad internal alignment; H3b remains small | REPAIR_REQUIRED |
| 102 | subsection | Hallmark-level associations remain descriptive | REPAIR_REQUIRED |
| 112 | subsection | Tumors show reproducible weakening of RNA organization relative to adjacent normal tissue | REPAIR_REQUIRED |
| 124 | subsection | Multiomic tumor-normal control favors pre-existing structure with reorganization | REPAIR_REQUIRED |
| 136 | subsection | Independent prostate transport reproduces H1 but not the cross-layer architecture | REPAIR_REQUIRED |
| 147 | section | Discussion | REPAIR_REQUIRED |
| 148 | subsection | The recurrent result is strongest within methylation | REPAIR_REQUIRED |
| 153 | subsection | Tumor-normal controls show a state difference, not a recovery mechanism | REPAIR_REQUIRED |
| 158 | subsection | Semantic specificity is deliberately bounded | REPAIR_REQUIRED |
| 163 | subsection | Relationship to standard methods and limitations | REPAIR_REQUIRED |
| 167 | section | Conclusion | REPAIR_REQUIRED |

Administrative headings are exempt from the scientific lay map:

- line 169: Data and code availability — NOT_SCIENTIFIC
- line 172: Acknowledgements — NOT_SCIENTIFIC
- line 175: Funding — NOT_SCIENTIFIC
- line 178: Competing interests — NOT_SCIENTIFIC
- line 181: Author contributions — NOT_SCIENTIFIC
- line 184: Declaration of generative AI and AI-assisted technologies in the manuscript preparation process — NOT_SCIENTIFIC

### Supplement

| line | level | heading | status |
|---:|---|---|---|
| 35 | section | Purpose and evidence hierarchy | REPAIR_REQUIRED |
| 48 | subsection | Evidence architecture and AI-assisted verification | REPAIR_REQUIRED |
| 58 | section | Historical reconstruction and retired claims | REPAIR_REQUIRED |
| 70 | section | Stage A: RNA network reconstruction | REPAIR_REQUIRED |
| 71 | subsection | Source, transform, and module rules | REPAIR_REQUIRED |
| 76 | subsection | Stage A1 construction failure and A1.1 repair | REPAIR_REQUIRED |
| 83 | section | Stage B1: purity/leukocyte context decomposition | REPAIR_REQUIRED |
| 88 | section | Stage B2: orthogonal multiomic lineage | REPAIR_REQUIRED |
| 91 | subsection | RPPA branch | REPAIR_REQUIRED |
| 94 | subsection | Genomic branch | REPAIR_REQUIRED |
| 97 | section | P0 predictive branch and FINAL_HOLDOUT | REPAIR_REQUIRED |
| 98 | subsection | Eligibility limitation retained rather than repaired | REPAIR_REQUIRED |
| 103 | subsection | D3/D4 result | REPAIR_REQUIRED |
| 108 | subsection | P3-v2 FINAL_HOLDOUT | REPAIR_REQUIRED |
| 127 | paragraph | Release visualization note | REPAIR_REQUIRED |
| 129 | section | C0/C0.1/C1A methylation gates | REPAIR_REQUIRED |
| 134 | section | Stage C1 frozen contract | REPAIR_REQUIRED |
| 135 | subsection | Analysis universes | REPAIR_REQUIRED |
| 138 | subsection | H1 | REPAIR_REQUIRED |
| 143 | subsection | Round-1 stronger H1 confound-preserving nulls | REPAIR_REQUIRED |
| 203 | subsection | H2 | REPAIR_REQUIRED |
| 206 | subsection | H3 | REPAIR_REQUIRED |
| 209 | subsection | Purity/leukocyte projection | REPAIR_REQUIRED |
| 212 | section | C1 missingness amendments and mathematical status | REPAIR_REQUIRED |
| 213 | subsection | v2.1 | REPAIR_REQUIRED |
| 216 | subsection | v2.2 | REPAIR_REQUIRED |
| 225 | section | C1 global inference | REPAIR_REQUIRED |
| 246 | subsection | Observed versus canonical null magnitude | REPAIR_REQUIRED |
| 264 | subsection | Mathematical origin of the nonzero H2 permutation floor | REPAIR_REQUIRED |
| 301 | section | Named deviations and support | REPAIR_REQUIRED |
| 306 | paragraph | Named-deviation release table | REPAIR_REQUIRED |
| 310 | section | Descriptive Hallmark-level biology | REPAIR_REQUIRED |
| 313 | section | Post-C1 cohort-size and draw-overlap audit | REPAIR_REQUIRED |
| 331 | paragraph | Release visualization note | REPAIR_REQUIRED |
| 333 | section | Principal-angle diagnostics | REPAIR_REQUIRED |
| 348 | section | Technical-mask scope | REPAIR_REQUIRED |
| 351 | section | Retired H3b cancer-mechanism hypotheses and remaining subtype limitation | REPAIR_REQUIRED |
| 356 | section | P0/C1 semantic reconciliation | REPAIR_REQUIRED |
| 359 | section | Synthetic known-truth and baseline tool-development audits | REPAIR_REQUIRED |
| 386 | section | Post-C1 adversarial sensitivity v2.2 freeze and completed result | REPAIR_REQUIRED |
| 404 | section | Prospectively frozen tumor-normal control | REPAIR_REQUIRED |
| 411 | section | Independent prostate P1 transport result | REPAIR_REQUIRED |
| 438 | section | Scalar, modal, and system-level complementarity after null-floor correction | REPAIR_REQUIRED |
| 443 | section | Projection-conditioning audit and limitation | REPAIR_REQUIRED |
| 446 | section | Reproducibility map | REPAIR_REQUIRED |
| 463 | section | Failure ledger | REPAIR_REQUIRED |
| 487 | section | Residual platform and predictive-capacity limitations | REPAIR_REQUIRED |
| 492 | section | Exact current submission status | REPAIR_REQUIRED |

The lay map may be consolidated rather than inserted after every technical section, but it must preserve exact heading order and cannot create stronger claims than the technical record.

## GOM 0.4.8 reproducibility-guide format

**FAIL / BLOCKS FINALIZATION**

The current submission archive contains no canonical reproducibility guide.

The public `BIOSYSTEMS_ADVERSARIAL_R1_PUBLIC_REPRODUCIBILITY_INDEX_20260923.md` is a strong provenance index but does not satisfy 0.4.8 because it does not use numbered V-sections with:
- a visible `[CLAIM]`;
- executable verification or exact command sequence;
- declared input identity/path/version;
- expected output/tolerance/status;
- a final master smoke test.

A v18 guide must be created and tied to the current immutable scientific snapshot.

## GOM 0.4.9 combined pre-final audit

**FAIL because 0.4.7 and 0.4.8 fail.**

Additional open items:
1. current public reproducibility index still declares GOM v0.8.4 and binds the private v12 package, not v18/v15;
2. main Data and code availability still points to `biosystems-final-polish-20260923`, not the current immutable `biosystems-meat-bone-v18-20260923`;
3. bibliography has 18 entries, 15 cited, with `Ding2021`, `Gevaert2015`, and `Kim2020` unused after the meat/bone trim;
4. source-of-record ledger does not yet show FULL/ABSTRACT tier, exact source location, and retrieval date for every bibliographic item as required by 33.4;
5. R1/R2/R3 reproducibility levels are not explicitly declared for this v18 release.

## R1/R2/R3 current status

Until a canonical guide closes the record, the defensible status is:

- **R1 integrity verification: PASS for the shipped archive.** Fresh extraction of `BioSystems_Resubmission_MeatBone_v18_20260923.zip` and `sha256sum -c SHA256SUMS_BIOSYSTEMS_MEAT_BONE_20260923.txt` returns OK for every manifested payload.
- **R1 regeneration: PARTIAL/NOT CANONICALLY DOCUMENTED.** Main/supplement were previously rebuilt and visually QA'd, but the current archive lacks the canonical dependency/command guide and master smoke test needed for v0.8.6 release presentation.
- **R2 calculation reproducibility: PARTIAL.** Figure regeneration from audited aggregate source values is shipped; the complete heavy C1 parent result archive is not part of the submission package, so not every scientific quantity can be independently recomputed from the private archive alone.
- **R3 evidence reconstruction: PARTIAL.** TCGA/GDC/GEO/MSigDB source identities and many source hashes/lineage records are public, and external P1 source identity was audited, but the v18 release does not yet provide a single canonical R3 reconstruction map covering every decisive input and bibliographic source.

## Archive/library byte identity

The shipped archive itself is internally valid against its manifest.

The four current private-library PDFs materialized during this audit are **not byte-identical** to the PDF copies frozen inside the v18 archive. Page counts and extracted text hashes match the frozen archive copies for all four audited PDFs, so this is a byte-level release-state difference rather than an observed scientific-content difference.

Release rule:
- treat the archive payload as the authoritative v18 release bytes; or
- if standalone library PDFs are to be submitted instead, rebuild/freeze the manifest against those exact upload bytes before calling the package final.

Do not mix standalone PDFs from a different byte state with the frozen archive manifest.

## Citation and bibliography audit

Reviewer-requested oncology citations remain present and scientifically bounded. Reviewer 2 engineering-control citations remain appropriately declined because the control-theoretic cancer interpretation was withdrawn.

Open v0.8.6 provenance work:
- every bibliographic datum must trace to a retrieved FULL/ABSTRACT source with exact location and retrieval date under 33.4;
- three current bibliography entries are unused after the trim: `Ding2021`, `Gevaert2015`, `Kim2020`; cite them for an explicit live role or remove them.

## Experimental-opportunity disposition

**OBSERVATIONAL_ONLY for the current paper.**

A direct perturbation/recovery investigation is scientifically meaningful for the next oncology stability lineage but is not required to support the present static covariance/coupling claim. It must not be retroactively imported as though it were part of this submission.

## Final v0.8.6 disposition

| Area | Status |
|---|---|
| Scientific claim/evidence architecture | PASS |
| P0/P1/holdout/failure discipline | PASS |
| Static vs dynamic/recovery firewall | PASS |
| Domain-informed mediation/adversarial challenge | PASS |
| Claim compression | PASS |
| Joint chi/Chi scientific disposition | PASS, pointer needed |
| 0.4.2 voice/punctuation/scope | PASS |
| 0.4.3 default source setup | REPAIR_REQUIRED or venue override |
| 0.4.4 tables | PASS |
| 0.4.5 structural references | PASS |
| 0.4.6 validation language | PASS |
| 0.4.6 numeric provenance | REPAIR_REQUIRED |
| 0.4.7 lay explanations | FAIL / BLOCKING |
| 0.4.8 canonical reproducibility guide | FAIL / BLOCKING |
| 0.4.9 combined pre-final audit | FAIL until blockers close |
| Archive SHA-256 integrity | PASS |
| R1/R2/R3 explicit declaration | REPAIR_REQUIRED |
| v18 release-index synchronization | REPAIR_REQUIRED |
| citation source-of-record ledger | REPAIR_REQUIRED |
| bibliography hygiene | MINOR REPAIR_REQUIRED |

**Overall:** `SCIENCE_READY__PAPER_BUILDING_NOT_FINAL`

No new biological computation is indicated by this audit. The next work is mechanical/science-adjacent publication completion under GOM 0.4, beginning with the lay-explanation map and canonical v18 reproducibility guide.