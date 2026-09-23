# Response to Reviewers

**Round-1 adversarial synchronization:** 23 September 2026

**Manuscript:** BIOSYS-D-26-00267  
**Submitted title:** *Collapse of Regulatory Capacity Drives Convergent Phenotypes in Human Cancer*  
**Revised title:** *Recurrent Methylation Organization Across Human Cancers: Context-Dependent Methylation-RNA Coupling*

Dear Editor and Reviewers,

Thank you for the careful and technically substantive reviews. The manuscript was rebuilt around the evidence that survived direct testing rather than preserving the original interpretation by softer wording. The revised study no longer presents a biological damping ratio, a universal `chi = 1` cancer boundary, an ordered Warning/Confirmation/Collapse sequence, a causal substrate-capture mechanism, or a clinical treatment rule. The central claims are now static and explicitly layered: recurrent within-methylation organization in TCGA, TCGA-internal methylation-RNA correspondence, prospectively frozen tumor-versus-adjacent-normal controls, and a genuinely independent prostate transport test.

A substantial part of this reconstruction had already been frozen or executed before the reviewer-response closure. Dated GitHub commits, prospective freeze files, source hashes, workflow runs, result artifacts, failed branches, and post-result audits are retained so that author-initiated corrections can be distinguished from reviewer-driven additions. After the initial revision package was assembled, an additional adversarial verification round was performed. Those later tests are explicitly labeled **post-result sensitivities** and are not represented as part of the original preregistration.

The additional verification materially narrowed and strengthened the manuscript. In particular, the canonical H1 probe-permutation null is now described as an independence/construction floor rather than a comprehensive biological null; H1 was then challenged by stronger post-result nulls preserving measured purity/leukocyte structure and TCGA Tissue Source Site structure. H1 remained positive in 30/30 evaluable cancers in both attacks. The external prostate H1 result was also rerun only for Monte Carlo precision with the same deterministic null stream extended from B=999 to B=9,999, while the original external classification was left unchanged.

Below is the point-by-point response.

---

## Reviewer 1

### 1. Verify expression units and preprocessing

**Response:** Agreed. The Methods now states the exact source representation. Stage A uses the PanCanAtlas **EB++ batch-adjusted, already normalized RSEM** matrix; it is not treated as raw counts. Finite source values receive the downstream transform `log2(max(x,0)+1)`, while source non-finite values remain missing. The pseudocount is retained as part of the frozen representation and primarily affects the lowest-expression range. Historical CV/2 is not used as a biological damping coordinate or as evidence for the current claims.

**Revision:** Source identity, preprocessing, transformations, missingness rules, and exact source hashes are explicit in Methods and the reproducibility record.

### 2. Analyze cancers separately rather than relying on pooled pan-cancer behavior

**Response:** Agreed. Cancer is the inferential unit. Stage C1 uses the same fixed n=30 construction in 32 cancers and global inference is performed on cancer-level effects, not pooled patient rows. Exceptions, refusals, non-evaluable branches, and support limitations remain named.

**Revision:** Cancer-specific H1/H2/H3a/H3b results and support rules are retained in the main paper and Supplement.

### 3. Remove mean-variance dependence / show the signal is not merely CV-versus-mean structure

**Response:** Agreed. The historical CV-based scalar interpretation has been withdrawn. The current analyses use RNA network coordinates, methylation spectral concentration, centered-kernel patient geometry, and Hallmark-level correspondence with separately defined nulls. Post-C1 sensitivities include repeated patient-null construction, complete-case restrictions, TSS200 restriction, leading-mode ablation, composition-complete gating, and technical masking.

**Revision:** The revised manuscript no longer uses CV/2 to support a biological damping, stability, or mechanistic claim.

### 4. Replace toy Poisson logic with realistic nulls

**Response:** Agreed. The Poisson-style mechanistic interpretation was retired. H1 uses within-probe patient permutation, H2 uses patient-label shuffling, H3a uses patient shuffling of the Hallmark-score representation, and H3b uses Hallmark-label shuffling.

The revision now states an important limit more clearly: the canonical H1 null preserves each CpG's sampled marginal values but destroys all cross-probe covariance, so it is an **independence/construction floor**, not a complete composition or batch null. During final adversarial verification, two stronger post-result H1 sensitivities were therefore added:

- preserving linear ABSOLUTE-purity and methylation-derived leukocyte structure: H1 remained positive in 30/30 composition-complete cancers, median raw-minus-null excess = 0.09998, exact two-sided sign-test p = 1.86×10^-9;
- preserving those same two composition axes **plus TCGA Tissue Source Site-associated CpG mean structure**: H1 again remained positive in 30/30 cancers, median excess = 0.08162, p = 1.86×10^-9.

A conventional PCA PC1-variance-fraction summary evaluated against the same composition+TSS-preserving null was also positive in 30/30 cancers (median raw-minus-null = 0.06858, p = 1.86×10^-9). These are post-result robustness tests and are not used to rewrite the original C1 preregistration.

**Revision:** H1 is now reported relative to both its canonical construction floor and these stronger measured-confound-preserving post-result attacks. Residual batch, plate/slide, subtype, nonlinear composition, and unmeasured technical structure remain explicit limitations.

### 5. Include normal controls / establish tumor specificity

**Response:** A prospectively frozen tumor-versus-adjacent-normal program was added before type-11 molecular outcomes were opened.

TN-A1 comprised BRCA, COAD, HNSC, KIRC, KIRP, LIHC, LUAD, LUSC, PRAD, STAD, THCA, and UCEC. All three RNA coordinates were lower in tumor in 12/12 cancers: median tumor-minus-normal effects were -0.0561 for internal pairwise coherence, -0.0730 for PC1 organization, and -0.1085 for external coupling; BH q=0.000488 for each.

TN-P20 comprised BRCA, COAD, HNSC, KICH, KIRC, KIRP, LIHC, LUAD, LUSC, PRAD, STAD, THCA, and UCEC. The same-participant sensitivity retained lower pairwise coherence and PC1 organization in 13/13 cancers and lower external coupling in 12/13, all q<=0.00342.

The five-cancer TN-C1 multiomic lane showed lower methylation H1 in tumor in 5/5 cancers. Because n=5 gives an exact two-sided sign-test resolution of p=0.0625 (BH q=0.125), this is now described as directional consistency/effect evidence rather than a statistically resolved pan-cancer specificity claim.

**Composition limit:** these RNA tumor-normal contrasts remain **unadjusted tissue-state associations**. ABSOLUTE purity is tumor-defined and is not symmetric in adjacent tissue. A source-only audit of the exact methylation-derived leukocyte resource found zero TN-A1 cancers with >=30 finite values in both states and zero TN-P20 cancers with >=20 same-participant finite values, so a symmetric adjustment could not be constructed from the frozen sources without inventing a new composition model. A post-hoc breadth audit showed that the RNA direction was not concentrated in a small immune subset: TN-A1 cancer-median effects were lower in tumor for 49/50, 47/50, and 50/50 Hallmarks across the three RNA coordinates; TN-P20 counts were 48/50, 48/50, and 50/50. This breadth does not eliminate broader tissue-composition confounding.

**Revision:** The manuscript now claims an unadjusted tumor-associated weakening/reorganization of the measured architecture, not tumor-cell-intrinsic loss and not a recovery mechanism. TCGA Solid Tissue Normal is described as an adjacent/non-tumor reference, not a universal healthy baseline.

### 6. Control purity / stromal / immune composition

**Response:** Agreed. ABSOLUTE purity and methylation-derived leukocyte fraction are modeled explicitly where those variables have a valid interpretation. The post-C1 projected branch compares real covariate projection with a permuted-covariate construction and preserves the limitation that two covariates do not equal complete deconvolution.

The additional post-result H1 attacks described above now directly address the concern that the externally transported layer might simply reflect measured composition. H1 remains positive in 30/30 cancers after preserving purity/leukocyte-associated CpG structure and again after additionally preserving TCGA Tissue Source Site mean structure. The public external prostate metadata expose no additional age, sex, center/site, plate, Sentrix, array-position, or scan-batch variable satisfying the prespecified adjustment rules; this is reported as a **source limitation**, not evidence that those confounders are absent.

**Revision:** Claims are limited to organization above the specified construction and measured-confound-preserving nulls. Full composition/batch independence is not claimed.

### 7. Replace subjective zones with objective statistical rules

**Response:** Rather than re-thresholding the submitted Warning/Confirmation/Collapse zones, the sequence was withdrawn as a biological or diagnostic progression claim. Cross-sectional data do not establish temporal order.

**Revision:** The revised Results do not depend on those zones.

### 8. Validate in an independent dataset

**Response:** Completed under a freeze established before any external GRI molecular endpoint was opened. The external family is GSE237995 RNA-seq + GSE262522 450K + GSE262524 EPIC methylation from Ramakrishnan et al. (Genome Medicine, 2024).

The primary lane used 30 prospectively selected complete 450K tumor/adjacent participant pairs. **H1, H2, and H3a were computed on the 30 tumor samples only.** Adjacent samples were used for symmetric probe eligibility and the separately declared tumor-normal secondary analysis; tumor and adjacent tissue were not pooled into the primary architecture matrix.

Original frozen B=999 primary 450K result:
- H1: effect +0.303090, p=0.001, BH q=0.003, PASS;
- H2: effect +0.019724, q=0.4065, no detectable transport;
- H3a: effect -0.040489, q=0.813, no transport.

The full n=32 450K sensitivity was concordant. EPIC again reproduced H1 (effect +0.358394, q=0.003), while H2/H3a remained unresolved. Their small null-compatible point estimates changed sign across the two platform/cohort subsets. Because sign reversal was a prospectively frozen conflict criterion, the procedural final label remains `P1_REPRESENTATION_DEPENDENT`. The manuscript now states explicitly that this label records the frozen conflict rule; it is **not evidence that a real nonzero H2/H3a effect differs by platform**.

The external H2 effect is roughly an order of magnitude below the TCGA median internal effect. It is therefore described as **no detectable external H2 transport**, not as a simple power-limited replication.

The original B=999 H1 p/q values were at the Monte Carlo resolution floor. A post-result numerical-precision sensitivity extended the **same deterministic null stream** to B=9,999 without changing samples, features, endpoints, or null definitions. H1 remained at the finer floor on both 450K and EPIC (p=0.0001, BH q=0.0003), whereas H2/H3a remained unresolved. The original P1 classification was not changed.

The external H1 effect is substantially larger than the TCGA median H1 effect, so the manuscript does not describe it as effect-size replication. A source-declared AA/EA race sensitivity did not explain the large effect; however, unrecorded technical or latent biological covariance remains possible.

**Revision:** Independent cross-source support is claimed for H1 only. H2/H3a remain TCGA-internal/context-dependent findings.

### 9. Remove temporal language unsupported by cross-sectional data

**Response:** Agreed. Static TCGA and external analyses are separated from perturbation, recovery, hysteresis, inheritance, and treatment-response claims.

**Revision:** The paper reports tumor-associated weakening/reorganization, not failure to regain stability.

### 10. Keep therapeutic implications hypothetical

**Response:** Agreed. The revised manuscript makes no treatment-state rule or therapeutic recommendation.

### 11. Add direct methylation/chromatin/ATAC evidence and engage relevant literature

**Response:** DNA methylation is now a measured primary layer rather than an inferred chromatin surrogate. The paper does not equate DNA methylation with chromatin accessibility and does not claim causal methylation-to-RNA regulation.

The cancer-regulation references suggested by the reviewer were also evaluated and incorporated where they directly support context rather than the statistics themselves:
- Li et al., *Cancer Discovery* 2024, PMID 39485254, on noncoding cis-regulatory elements in the 3D genome;
- Malaymar Pinar et al., *Molecular & Cellular Proteomics* 2025, PMID 39617063, on Nuclear Factor I regulatory networks;
- Chen et al., *Nature Communications* 2024, PMID 38409266, on pan-cancer alternative-polyadenylation susceptibility architecture.

**Revision:** These papers are cited to motivate a layered regulatory view. They are not presented as validation of H1/H2/H3a.

---

## Reviewer 2

### 1. Independent cohort validation

**Response:** Completed prospectively as described above. The result is deliberately partial: H1 transports across 450K and EPIC; H2/H3a do not transport detectably. The final procedural label remains `P1_REPRESENTATION_DEPENDENT` under the frozen sensitivity rule.

### 2. Additional omics validation

**Response:** The revised paper centers on directly measured RNA and methylation, with genomic/context branches retained only where they constrain interpretation. Shared TCGA acquisition/processing prevents internal layers from being relabeled as independent external confirmation. The independent prostate study remains the distinct external layer.

**Revision:** The earlier response language implying that protein/phosphoprotein evidence was a central component of the revised manuscript has been removed because that analysis is not part of the present main-paper claim set.

### 3. Cancer-specific robustness

**Response:** Cancer-specific analysis is the default unit, with fixed finite-sample calibration, named exclusions, technical-track replication, exact denominator reporting, and explicit failure/refusal states.

### 4. Reproducibility / method detail

**Response:** The scientific chronology is now publicly inspectable in the GitHub repository `SymC-Universe/Biomedical` on the Round-1 branch `biosystems-adversarial-r1-20260923`. The public repository contains the prospective freeze contracts, configs, code, deterministic seeds, source hashes, workflows, outcome artifacts, post-result audits, reviewer-adjudication matrix, and a Round-1 reproducibility index. The pre-Round-1 release was snapshotted on an immutable branch before the additional adversarial sensitivities were added, so the chronology can be reconstructed independently rather than relying on local file timestamps.

The editable manuscript and supplement remain private authoring artifacts until journal submission; this does not conceal scientific decision rules, workflow identities, or result artifacts.

**Revision:** The final submission package will bind manuscript/supplement/figure/reviewer-response byte hashes to the public analysis snapshot while excluding third-party source data that cannot be redistributed as project-owned data.

### 5. Biological mechanism grounding

**Response:** Agreed that association is not mechanism. The revised paper distinguishes within-layer organization, cross-layer correspondence, measured composition/context, and future dynamic questions. CKA is described as correspondence, not regulatory direction. H1 is a spectral organization statistic, not proof of a tumor-cell-intrinsic mechanism.

### 6. Demonstrate clinical utility beyond existing predictors

**Response:** This claim is no longer made. The P0 held-out branch also had a capacity mismatch: approximately 45 methylation features plus two covariates were compared with two covariates alone, and only 19 cancers met the frozen all-partition eligibility rule, below the fixed 24-cancer pan-cancer promotion floor. The revised manuscript therefore removes P0 from the Abstract's central evidence and retains the 17/18 FINAL_HOLDOUT result only as a bounded internal observation that the methylation representation contained held-out information beyond two measured covariates. It is not used to claim Hallmark-specific superiority or clinical utility.

A fair equal-capacity post-FINAL comparator would require a new source-projection experiment because the exact participant-level FINAL feature matrices are not preserved in the public repository and an earlier referenced capacity-control freeze was not recoverable. Rather than inventing retrospective preregistration or rebuilding a new experiment solely to rescue a withdrawn claim, the stronger P0 interpretation was removed.

### 7. Explain failures / heterogeneity rather than presenting only favorable results

**Response:** This principle now governs the paper. PCPG remains the P0 held-out loss. Five Hallmarks remain source-mapping refusals. H3b remains small and support-sensitive. H2/H3a external transport is not established. The external prostate RNA tumor-normal comparison is not confirmed. The `P1_REPRESENTATION_DEPENDENT` label is preserved even though it is inconvenient because it was frozen before the external result.

---

## Reviewer-suggested engineering-control references

The suggested boost-converter, electric-vehicle-control, and drilling/control references were considered. Because the revised manuscript withdraws the prior **static transcriptomic damping mapping** (including the historical CV/2-as-damping interpretation, rank-as-time logic, and unsupported identification of ensemble mean/variance with oscillator frequency/dissipation), those engineering-control papers are not used as biological validation of the present static TCGA claims. The broader dynamic/control question is not declared false or abandoned: it is reserved for directly ordered perturbation-response data and native dynamical models, where oscillation, recovery, hysteresis, modal dominance, and reorganization can be tested without importing a mechanical oscillator into cross-sectional expression statistics. This is an explicit scope decision rather than an oversight.

---

## Author-initiated corrections and final adversarial verification

For transparency, major self-corrections identified during the rebuild include:

1. withdrawal of the historical CV/2 biological-damping interpretation;
2. retirement of energy/frequency and rank-as-time interpretations without a current derivation;
3. fixed-n correction of the Stage A sample-size construction artifact;
4. separation of internal TCGA holdout evidence from genuine external validation;
5. explicit failure of the stronger P0 semantic-sharing promotion rule;
6. retention of PCPG as the reproducible held-out loss;
7. C1 source-identity/missingness amendments and post-C1 adversarial sensitivities;
8. tumor-normal controls frozen before normal molecular outcomes were opened;
9. independent prostate transport frozen before external molecular outcomes were opened;
10. post-result Round-1 sensitivities explicitly separated from the original preregistered analyses rather than backdated into them.

The public GitHub history preserves these distinctions through dated freeze files, workflow commits, run IDs, artifact hashes, failed mechanical attempts, and post-result audits.

## Post-revision dynamic-lineage clarification

A separate P0-D Bio Chi investigation was intentionally kept outside the confirmatory TCGA spine while its native dynamic assumptions were tested. That work has now been reintegrated into the public reproducibility lineage without being relabeled as confirmation of the static manuscript. Two bounded findings matter for interpretation: (i) an executable six-state NF-kB model contains both real modes and a complex-conjugate pair, but the complex pair is not automatically the stability-setting mode in the nominal stable case; and (ii) a prospectively frozen M397 melanoma withdrawal analysis supports realized transcriptomic recovery toward the pre-treatment state in one ordered trajectory (Spearman rho = -0.8857, exact one-sided p = 0.0167) under its frozen simple-distance metric. These findings justify retaining dynamic-response questions as an active biological research line, but they do not restore the historical CV/2 damping construction, establish a universal oscillator model for cancer, or promote a general predictive cancer tool.

The manuscript-facing claim therefore remains narrower: static TCGA architecture is interpreted statically; direct temporal language is used only for genuinely ordered perturbation/recovery evidence; and predictive-tool promotion remains bounded by the external-transport results already reported.

## Summary of the revised claim

The revised manuscript supports a narrower conclusion than the submitted paper. Across TCGA cancers, methylation contains recurrent patient-resolved spectral organization that remains positive under stronger post-result nulls preserving measured composition and TCGA Tissue Source Site structure. TCGA-internal H2/H3a show recurrent methylation-RNA correspondence but do not transport detectably in the independent prostate study under its different RNA representation. Tumor-versus-adjacent-normal analyses show a broad, reproducible but composition-unadjusted RNA state contrast; the available frozen composition sources do not support a symmetric normal-tissue adjustment. Independent prostate data reproduce H1 on both 450K and EPIC, including at finer Monte Carlo resolution, but not the broader cross-layer or RNA tumor-normal claims.

The paper therefore reports **recurrent methylation organization with context-dependent methylation-RNA coupling and explicit composition/technical limits**. It does not claim a biological damping ratio, universal critical boundary, causal temporal collapse, failed recovery, clinical utility, or a treatment rule.

Thank you for the opportunity to revise the work. The reviewers' critiques materially improved the manuscript and helped concentrate the final claims on the portions that survived the strongest available tests.