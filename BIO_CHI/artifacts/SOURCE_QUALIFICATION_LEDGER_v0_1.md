# Bio Chi source qualification ledger v0.1

**Date:** 23 September 2026  
**Status:** ACTIVE / OUTCOME-BLIND SOURCE QUALIFICATION  
**Rule:** source qualification establishes identity and reproducibility only. It does not promote a biological result.

## Frozen public-source map

The generic external-source freeze is pinned in `BIO_CHI/config/EXTERNAL_SOURCE_FREEZE_PIN_v0_1.json`. That record preserves exact file-map identities and available hashes for GSE145356, GSE164716, GSE237228, GSE97682, and GSE255671 without interpreting molecular values. Large files that exceeded the frozen hash ceiling remain explicitly deferred rather than implicitly treated as hashed.

## Verified public source records

### Rehman et al. 2021 — colorectal diapause-like DTP

- GEO: **GSE145356**.
- Organism: Homo sapiens.
- Design includes vehicle, DTP-state, regrowth, and resistant samples.
- Samples: 25.
- BioProject: PRJNA606811.
- SRA study: **SRP249585**.
- Processed merged HTSeq read-count material and raw sequencing paths are public.
- WES accession reported by the paper: EGAS00001004773. Controlled-access handling remains separate.

**Source disposition:** PUBLIC RNA EXECUTION FEASIBLE. Barcode/WES components require separate source-path audit.

### Marsolier et al. 2022 — H3K27me3 chemotolerance

- GEO SuperSeries: **GSE164716**.
- Public subseries include GSE164385, GSE164409, GSE164715, GSE186965, GSE186966, and GSE196764.
- Public analysis code includes `vallotlab/ChemoPersistance` and `TeamPerie/lentiviral_barcode_detection_in10X_data`.
- Published code release v1.0.0 is archived on Zenodo, DOI 10.5281/zenodo.6010802.

**Source disposition:** STRONG PUBLIC MULTIOMIC/CARRIER CANDIDATE. Minimal executable subset remains to be selected under the frozen eligibility contract, not by target result.

### Harmange et al. 2023 — scMemorySeq

- GEO: **GSE237228**; BioProject **PRJNA994430**.
- Metadata-only lineage audit run **35863431965** passed without opening molecular values or cell-level metadata rows.
- The Series contains **22** GEO samples and each sample has an explicit SRA experiment link (SRX21003294 through SRX21003315).
- The frozen cell-metadata header explicitly contains lineage and condition fields, including `nCount_lineage`, `nFeature_lineage`, `conditions`, `Primed_UCell`, `clusterID`, `TGFB1`, `TGFBRi`, and `PI3Ki`.
- Frozen supplementary identities include barcodes, genes, matrix, metadata, and RAW archive paths.
- This closes the high-level source-lineage identity gap. It does **not** establish that a particular barcode/state is a causal Stability Inheritance carrier.

**Source disposition:** PUBLIC LINEAGE/MEMORY SOURCE MAP QUALIFIED. Biological carrier correspondence/intervention remains a separate scientific gate.

### Shaffer et al. 2017 — rare-cell priming and resistance

- GEO SuperSeries: **GSE97682**; BioProject **PRJNA382641**.
- Metadata-only lineage audit run **35863431965** passed without opening molecular values.
- GSE97682 is explicitly the SuperSeries of **GSE97679, GSE97680, and GSE97681**.
- The SuperSeries contains **155** samples, all with explicit SRA experiment links (SRX2733818 through SRX2733973).
- GEO metadata explicitly contains Drug, NoDrug, **48hrholiday**, and **7dayholiday** conditions; the audit recorded 76 Drug, 36 NoDrug, 5 48-hour-holiday, and 5 7-day-holiday sample labels. These are source labels only, not outcome adjudications.
- Raw/processed Series material remains captured by the external-source freeze.

**Source disposition:** PUBLIC RECOVERY/REORGANIZATION SOURCE LINEAGE QUALIFIED. Execution-subset selection remains prospective and outcome-blind.

### Srivatsan et al. 2020 — sci-Plex

- GEO: **GSE139944**; BioProject PRJNA587707; SRA SRP228591.
- Primary design is perturbation response without washout/recovery.

**Source disposition:** PUBLIC RESPONSE-SURFACE NEGATIVE CONTROL. Recovery claims must be refused by design.

### Lee et al. 2014 — paclitaxel tolerance

- Paper-reported SRA accession **SRP040309** now resolves cleanly under BioProject **PRJNA241034**.
- Metadata-only source-map run **35863794417** passed and froze the exact NCBI RunInfo response (SHA-256 `79a96a4b70a4dcafab26f253cfa57fc53038008993085bf957e2285502fde2cd`).
- The study contains **19 public RNA-seq runs**, 19 experiments, 19 SRA samples, and 19 BioSamples; all runs are paired-end Illumina RNA-seq.
- Sequence reads were not downloaded and no expression values were opened.
- The second metadata-only gate, run **35863951516**, also passed. It maps 5 untreated, 5 stressed, and 5 drug-tolerant single-cell RNA-seq samples plus 1 untreated, 1 stressed, and 2 drug-tolerant bulk RNA-seq samples.
- The exact SRA metadata XML is frozen at SHA-256 `33a2445f81ad0b21bde062aebefdd5c89b2bb0031f306edc95764d6d3eda6834`.
- **No explicitly labeled reconverted or post-withdrawal RNA sample is present in SRP040309.** This is a source-design limitation, not a negative biological result.

**Source disposition:** PUBLIC RESPONSE/STATE-TRANSITION RNA SOURCE QUALIFIED. SRP040309 IS NOT A DIRECT TRANSCRIPTOMIC RECOVERY TRAJECTORY; retain Lee 2014 only as secondary recovery literature/phenotypic context unless an independent public recovery source is identified.

## Scalar/model-track and known-truth source qualification

### Jaruszewicz-Błońska et al. 2023 — identifiable NF-κB model

- DOI: 10.1371/journal.pone.0286416.
- Reduced six-variable ODE source is supplied as S1 Code and is hash-pinned in the Bio Chi source freeze.
- Native source reproduction, Figure-8 execution, local-stability work, all-mode inventory, and full-state coordinate control are tracked separately in machine-readable pins.
- This executable model remains a model-identifiability candidate; it is not by itself a biological `chi_bio` admission.

**Source disposition:** EXECUTABLE MODEL QUALIFICATION PATH ACTIVE. Primary biological observability/identifiability remains a separate Q2/Q3 gate.

### Son et al. 2021 — dynamic NF-κB

- DOI: 10.1126/scisignal.aaz4382.
- Full-text source audit confirms dense single-cell stimulation/recovery timing, but the primary single-cell trace data are stated to be available **upon request**.
- Custom MATLAB control/analysis software is described; no stable public repository was established by the targeted audit.

**Source disposition:** SCIENTIFICALLY STRONG / REPRODUCIBILITY ACCESS RISK. Do not treat the trajectories as public-downloadable.

### Jiang et al. 2020 — yeast stress memory

- DOI: 10.1126/scisignal.aay3585; PMCID: PMC7302112.
- Article and supplementary material are public; the paper states data needed for its conclusions are in the article/supplement.
- The targeted full-text audit did not establish a standalone public raw single-cell trajectory repository or accession.
- Custom MATLAB code is stated to be available upon request.

**Source disposition:** STRONG KNOWN-TRUTH DESIGN / RAW-TRACE EXECUTION ACCESS NOT YET CLOSED. Public article/supplement is not equivalent to a frozen raw trajectory package.

### Blum et al. 2019 — temporal ERK/MAPK perturbation

- DOI: 10.15252/msb.20198947.
- Publication date: 19 November 2019; article is open access under CC BY 4.0.
- The article's data-availability section states that CellProfiler pipelines are supplied as Code EV1 and that the inference source, model files, and inference results are public at `Mijan/LFNS_MSB`.
- Article supplementary resources include source-data ZIPs for Figures 1–5, Code EV1, and CP pipelines.
- Public model/inference repository `Mijan/LFNS_MSB` is pinned outcome-blind at branch `MSB_version`, commit `5c917abda0618d75c00c9cab45f24ed893dd71f1`, tree `cbb79d66f79a84bc8af28ca85f1678295348da83` in `BIO_CHI/config/BLUM2019_PUBLIC_SOURCE_PIN_v0_1.json`.
- Mendeley Data DOI **10.17632/ccnxn84w8z.2**, Version 2, is now frozen through its supported public-files API. Exact `data.zip` UUID: `b8e7b821-d59b-4b42-b34e-1d679ace693d`; exact archive size: **8,352,835 bytes**; SHA-256: `8bbd1ead46b5bb6b676bd47a5f415fdd790840a9c726321dc5c209b9c527bc62`.
- Outcome-blind schema inventory found **103** ZIP members without reading member payloads; the scientific payload is organized under `data/` with source-data folders for Figures 1–5 and Appendix plus CellProfiler pipelines.
- A prospectively frozen documentation/header-only audit mapped the Figure-1 source fields without reading data rows: EKAR trajectories use `intensity_ekar,realtime,group.idx,id,fov`; grouping uses `group,group.idx`; pulse-channel records use `fov,intensity_pulse,realtime,group.idx`.
- The publication defines the native Jeffries-Matusita distance and integrated population distance, but a full-text method audit did **not** establish the histogram bin count, bin edges/range, common-bin rule, smoothing/pseudocount rule, missing-value handling, exact alignment/interpolation rule, or the original Figure-1H implementation code.
- Therefore exact Figure-1H native-metric reproduction is **method-underspecified** under the current public record. No binning convention will be inferred from common practice.
- Raw microscopy public-download status remains unclaimed.

**Source disposition:** PUBLIC SOURCE/SCHEMA QUALIFIED; EXACT PUBLISHED JM REPRODUCTION BLOCKED BY METHOD UNDER-SPECIFICATION. This is a preserved Limit-Map/source-method finding, not a reason to invent a replacement metric.

### Geva-Zatorsky et al. 2006 — p53/Mdm2

- DOI: 10.1038/msb4100068.
- Supplementary movies/data support long single-cell time series.
- Modern machine-readable raw-data availability remains to be audited.
- Sustained single-cell oscillations make this an important anti-damping / representation-limit case.

**Source disposition:** LIMIT-CASE CANDIDATE, NOT PRIMARY RECOVERY.

## Verified hysteresis/reorganization source

### Su et al. 2026 — sequential transcriptional waves and NF-κB-driven chromatin remodeling

- Nature Communications 17, 3228 (2026), DOI **10.1038/s41467-026-71349-4**.
- GEO **GSE255671**; BioProject **PRJNA1076128**; additional longitudinal sources GSE65186, EGAS00001000992, and E-MTAB-5493.
- The 15-point M397 RNA trajectory was frozen prospectively from metadata only: D0, D3, D8, D13, D21, D29, D33, D38, D59 and post-D29-removal DR4, DR10, DR15, DR17, DR30, DR35.
- Native-source metadata run **35865443566** completed **PASS_SU_NATIVE_SOURCE_METADATA** with all 15 expected GSMs present and no expression values opened; artifact **10751772307**, digest `sha256:056a11a25b783d880b69da7c1e68a8a80f3ba9e33d9d7f44eb376fdebd944237`.
- GEO metadata explicitly reports hg19, htseq-count v0.6.0, TxDb.Hsapiens.UCSC.hg19.knownGene, RPKM/FPKM-related processed expression and read-count processing. This qualifies source/method identity only.
- Public analysis/modeling code `jihoonlee0/melanoma_reversible_transition` is pinned at commit `a2b2119f6d69d49e33ff4b57fb04b2b1eaf5fe68`, tree `a0d9cd0dcf25cda1a53cc8670f77490c0395764c`; `surprisal.m` blob `2dac24e398f30451388c2acbe1406e23afcdad50` implements log-transform + SVD structure. Archived release DOI: **10.5281/zenodo.17751601**.
- The publication defines forward/reverse module coordinates and an ODE/MCMC analysis, but it does **not** provide a single scalar hysteresis-area/distance statistic. No new hysteresis scalar will be invented at source qualification.
- GSE255671_RAW.tar was traversed remotely at TAR-header level with **zero ordinary member-payload bytes read**. It contains 50 ChIP/ATAC BigWig/bedGraph members and no M397 RNA expression matrix. This source-design fact is pinned in `SU2026_GSE255671_REMOTE_TAR_INVENTORY_V01_RESULT_PIN.json`.
- The M397 samples also belong to **GSE134459**, whose Series record supplies `GSE134459_Reversible_RPKM_values.txt.gz`. That exact compressed file is now frozen at **2,071,888 bytes**, SHA-256 `1ec204f02187289fdc0d718fe2291d34f2e3e6b943dcdf8fe627718d75a42d8c`, before decompression/value inspection.
- A header-only audit read zero data rows and confirmed exactly the 15 frozen trajectory columns: Control, D3, D8, D13, D21, D29, D33, D38, D59, dr29.D4, dr29.D10, dr29.D15, dr29.D17, dr29.D30, dr29.D35.
- This source closure exposed a **native-method collision** that is now preserved, not repaired: the publication describes FPKM/whole-transcriptome/15-timepoint surprisal, the exact public trajectory object is annotated RPKM, and public `surprisal.m` assumes a preloaded `all` matrix while commenting `400*17`. The public materials do not resolve RPKM-vs-FPKM, 15-vs-17, 400-vs-whole-transcriptome, exact input loading/filtering, or zero/pseudocount handling.
- Exact native surprisal reproduction is therefore pinned as `EXACT_NATIVE_SURPRISAL_REPRODUCTION_BLOCKED_INPUT_METHOD_COLLISION`. No choice among these alternatives will be made after viewing expression outcomes.

**Source disposition:** STRONG PUBLIC HYSTERESIS/REORGANIZATION SOURCE QUALIFIED; EXACT NATIVE SURPRISAL REPRODUCTION CURRENTLY BLOCKED BY PRESERVED INPUT/METHOD COLLISION. OUTCOME VALUES REMAIN SEALED.

## Preserved unresolved/source-limited cases

1. **Sharma et al. 2010 PC9 DTP/DTEP**
   - DOI 10.1016/j.cell.2010.02.027; PMCID PMC2851638.
   - Public original article documents drug-free reversal/resensitization.
   - Reproducibility Project: Cancer Biology registered a detailed replication protocol, DOI 10.7554/eLife.09462.
   - No modern standalone machine-readable raw dataset for the original 2010 study was established by targeted search.
   - **Disposition: STRONG BIOLOGICAL RECOVERY REFERENCE / ORIGINAL RAW DATA UNVERIFIED.**
2. **Harmange lineage-barcode mapping**
   - Exact lineage-barcode files and their mapping to GEO sample records remain to be closed.
3. **Jiang raw single-cell trajectories**
   - Public paper/supplement confirmed; standalone raw trace package remains unverified.
4. **Son NF-κB primary trajectories**
   - Explicitly upon request; not a public-download execution path at present.

## Next mechanical source tasks

- complete the already-frozen Lee SRP040309 experiment/sample metadata map so treatment/state labels are source-derived rather than inferred;
- continue Harmange lineage/carrier mapping from the now-qualified 22-sample/SRX source map, without treating metadata presence as inherited-carrier proof;
- freeze a Shaffer execution subset only after its SuperSeries/subseries role and recovery-return target are stated prospectively;
- treat Blum exact JM reproduction as blocked unless an original implementation resolves the histogram construction; do not fabricate a binning rule;
- qualify candidate testbeds against the frozen P0-D eligibility contract without using expected SymC agreement as a selection criterion;
- keep `chi_bio`, `Chi_bio`, and Bio Chi admission closed until their respective prospective gates are satisfied.

## Autorun provenance — 23 September 2026 source-gate closure

- PR #6 head at verification before checkpoint writes: `f6d4cbc0026da3a0e2cadbb12b71bb4ee0163416`; PR remained **open, draft, mergeable**, on `chi-bio-recovery-p0d-20260922`.
- Blum Mendeley public-files resolution/source freeze: run **35862686108**, SUCCESS; artifact **10751061699**. Exact `data.zip` UUID `b8e7b821-d59b-4b42-b34e-1d679ace693d`, size **8,352,835 bytes**, archive SHA-256 `8bbd1ead46b5bb6b676bd47a5f415fdd790840a9c726321dc5c209b9c527bc62`.
- Blum metadata-only ZIP inventory revalidation: run **35863951277**, SUCCESS; artifact **10751880243**; **103 members**; member payloads not read.
- Blum documentation/header-only native-input mapping revalidation: run **35863951436**, SUCCESS; artifact **10751309038**; biological data rows not read and native metric not computed.
- Exact Blum Figure-1H Jeffries-Matusita reproduction remains **REFUSED / METHOD UNDERSPECIFIED** per `BIO_CHI/config/BLUM2019_NATIVE_METHOD_QUALIFICATION_PIN_v0_1.json`. No binning, smoothing, alignment, or missing-data convention was invented.
- Lee SRP040309 metadata source map: run **35863951560**, SUCCESS; artifact **10751845181**; 19 paired-end RNA-seq runs under SRP040309 / PRJNA241034.
- Harmange/Shaffer metadata-only lineage audit: run **35863952068**, SUCCESS; artifact **10751386783**. No molecular values were opened.
- Bio Chi governance/privacy guard at the same verified head: run **35863951732**, SUCCESS.
- Working manuscript scope remains **NOT OPEN / PRIVATE**; no manuscript text was introduced into the public investigation branch.

### Preserved BioProject hierarchy repair

- BioProject/SRA reconciliation v0.1 run **35864958524** failed because Shaffer's SuperSeries parent BioProject `PRJNA382641` was treated as though child-project accessions should equal the parent accession. The failure artifact is **10751561638**.
- v0.2 run **35864958490** repaired only that source-hierarchy logic by reconciling the explicit child projects `PRJNA382674`, `PRJNA382752`, and `PRJNA382753`; it recovered the full **155-run** union with zero missing and zero extra runs. Artifact **10752061357**.
- The repair changes source bookkeeping only. It does not alter sample biology, outcomes, cohorts, or interpretation rules.


### BioProject/SRA hierarchy reconciliation

- v0.1 is preserved as a source-hierarchy failure: it incorrectly required every Shaffer RunInfo BioProject to equal the umbrella query accession `PRJNA382641`. The failure is pinned in `BIO_CHI/config/P0D_BIOPROJECT_SRA_RECONCILIATION_V01_FAILURE_PIN.json`.
- Prospectively repaired v0.2 run **35864928756** passed; artifact **10752086226**, digest `sha256:b0fd3e0f3d02dd1dae92b6f86aa9a9736c51172e770fd9c2e7de0caf15ebe83b`.
- Harmange: query `PRJNA994430` resolves to **23 SRA runs** in **SRP449288**; the run union is exact. The 22 GEO samples versus 23 SRA runs are retained as distinct source facts rather than forced to one-to-one identity.
- Shaffer: umbrella query `PRJNA382641` resolves to **155 SRA runs** partitioned exactly across studies **SRP103825, SRP103827, SRP103828** and child BioProjects **PRJNA382674, PRJNA382752, PRJNA382753**; union has zero missing/extra runs.
- The previously unverified `SRP103406` label is retired prospectively for this lineage.

**Source disposition:** PARENT/CHILD SRA PROVENANCE QUALIFIED; no biological outcome or testbed promotion follows from this bookkeeping result.


### Rehman 2021 native RNA method qualification

- GSE145356 source identity remains qualified and public.
- The paper specifies STAR v2.4.2a, XenofilteR v0.99.0, HTSeq v0.6.1, R 3.5.0, edgeR 3.24.0, limma 3.38.3, `prcomp`, z-score normalization, and Figure-4 group counts of control n=7, DTP n=3, regrowth n=3.
- Exact Figure-4 RNA/PCA reproduction remains under-specified: the non-expression filter threshold, exact edgeR normalization, limma path, `prcomp` center/scale arguments, batch rule, variable-gene rule, and the custom R scripts are not established in the public resources.
- The paper's declared public computational resources cover Pairtree/Pairtree inputs and Gillespie simulations; targeted GitHub/source search did not establish the custom RNA/PCA R implementation.
- This is pinned as `EXACT_FIGURE4_RNA_PCA_REPRODUCTION_BLOCKED_METHOD_UNDERSPECIFIED`.

**Source disposition:** CANCER RECOVERY BIOLOGY REMAINS IMPORTANT, BUT EXACT PUBLIC RNA/PCA NATIVE REPRODUCTION IS A LIMIT-MAP HOLD. Any replacement RNA pipeline must be separately prospectively frozen and cannot be called the original Figure-4 implementation.
