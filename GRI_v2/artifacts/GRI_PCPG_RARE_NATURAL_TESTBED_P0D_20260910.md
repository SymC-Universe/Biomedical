# GRI PCPG rare-natural-testbed qualification record

**Date:** 2026-09-10  
**Status:** `RARE_NATURAL_TESTBED` FOR P0-D DISCOVERY/LIMIT MAPPING ONLY  
**Selection status:** POST-RESULT / GRI-STRESS-CASE SELECTED  
**Confirmatory status:** NOT CONFIRMATORY; PROMOTION DEBT PRESENT  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## 1. Why this record exists

PCPG (TCGA pheochromocytoma/paraganglioma) repeatedly emerged as a stress case for the current GRI global transport/prediction representation. That alone is **not** a rarity criterion.

v0.7.1A permits a rare natural occurrence/state/phenotype to be used as a high-information limit testbed when rarity is established independently by domain-native evidence and the selection status is preserved honestly.

This record therefore asks two separate questions:

1. Is pheochromocytoma/paraganglioma genuinely rare by oncology-native evidence independent of GRI?
2. If yes, what epistemic role may the already-observed PCPG stress case play?

## 2. Domain-native rarity evidence

### NCI PDQ

Source:

- National Cancer Institute, `Pheochromocytoma and Paraganglioma Treatment (PDQ®)–Health Professional Version`
- https://www.cancer.gov/types/pheochromocytoma/hp/pheochromocytoma-treatment-pdq
- retrieved 2026-09-10

NCI states that pheochromocytoma incidence is approximately **2 to 8 per million persons per year**.

### NCI TCGA studied-cancer page

Source:

- National Cancer Institute, `Paraganglioma & Pheochromocytoma Study`
- https://www.cancer.gov/ccg/research/genome-sequencing/tcga/studied-cancers/paraganglioma-pheochromocytoma-study
- retrieved 2026-09-10

NCI describes paraganglioma/pheochromocytoma as rare and reports approximately **2 to 8 diagnoses per million people worldwide each year**.

### Systematic-review context

Source:

- `Systematic Review: Incidence of Pheochromocytoma and Paraganglioma Over 70 Years`
- PMCID PMC9334688 / PMID 35919261
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9334688/
- retrieved 2026-09-10

The systematic review found incidence estimates ranging **0.04 to 0.95 per 100,000 per year**, with more recent studies around 0.6 per 100,000/year after 2010.

### Rarity disposition

`DOMAIN_NATIVE_RARITY = SUPPORTED`

Rarity is therefore not inferred from GRI behavior.

## 3. Authenticity and biological-context gate

Source:

- Fishbein et al., `Comprehensive molecular characterization of pheochromocytoma and paraganglioma`, Cancer Cell 2017, PMCID PMC5643159.
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5643159/
- retrieved 2026-09-10

The TCGA study describes a cohort of **173 PCC/PGL patients** analyzed across multiple genomic assays, including mRNA sequencing, DNA methylation arrays, and RPPA, and identifies multiple molecularly defined groups.

This supports that the TCGA PCPG cohort represents a genuine, independently characterized tumor type rather than a GRI-generated or mislabeled category.

`AUTHENTICITY_GATE = PASS_FOR_TUMOR_TYPE_IDENTITY`

This does not prove that GRI's PCPG stress behavior is biological rather than methodological. That causal interpretation remains unresolved.

## 4. Selection firewall

PCPG was not selected for investigation because an epidemiological survey prospectively nominated it before GRI results were viewed. It became scientifically prominent because it repeatedly stressed the GRI representation.

Therefore:

- `selection_status = POST_RESULT`
- `reason_selected = RECURRENT_GRI_REPRESENTATION_STRESS`
- `rarity_basis = INDEPENDENT_ONCOLOGY_EPIDEMIOLOGY`
- `confirmation_eligible_on_current_evidence = NO`
- `promotion_debt = REQUIRED`

The independent rarity evidence allows **P0-D rare-natural-testbed use**. It does not erase the post-result selection path.

## 5. Allowed current uses

PCPG may now be used in P0-D to investigate:

- why the global all-methylation transport/prediction representation is less adequate there;
- whether same-Hallmark structure versus global structure is organized differently;
- whether subtype heterogeneity, molecular driver classes, tissue biology, composition, or another native feature explains the stress behavior;
- whether the production Engine can learn a principled refusal/routing boundary without using downstream outcome values to define that boundary;
- whether PCPG exposes a reduction that works in common tumors but loses information in this rare tumor context.

PCPG may also be used in P0-Q as a **previously observed stress fixture** for a revised Engine version, provided its use is labeled qualification rather than confirmation.

## 6. Prohibited current uses

This case cannot currently establish:

- that GRI generalizes to rare cancers;
- that rare cancers systematically behave differently;
- that the observed PCPG stress is caused by rarity;
- that a PCPG-specific routing rule is prospectively valid;
- that a biological transition has been found;
- that a rare-limit prediction has been confirmed;
- that a future Engine version is externally validated.

No prevalence or incidence claim about other tumor classes is inferred from PCPG.

## 7. Molecular heterogeneity warning

The TCGA molecular characterization reports multiple molecular groups within PCC/PGL. Therefore the rare tumor type must not be treated as internally homogeneous simply because it is rare.

This strengthens, rather than weakens, the value of PCPG as a P0-D limit testbed: a rare system can expose whether a global representation breaks because of internal heterogeneity, different regulatory organization, or another unmodeled structure.

It also means that any future PCPG-specific rule should be tested against molecular subtype structure rather than treating all PCPG samples as one mechanistic state by default.

## 8. Future promotion route

A future confirmatory rare-limit claim would require:

1. extract a measurable candidate boundary/routing rule from P0-D without hiding failed alternatives;
2. complete P0-Q known-truth/internal qualification;
3. freeze MFR-14, System Model/Engine/Atlas versions, comparator, decision rule, uncertainty, and falsifier;
4. define rare-case/cohort eligibility independently of the future Engine result;
5. preserve the eligible candidate universe/search route;
6. test on untouched external/future evidence;
7. report survival/failure without retuning the same evidence.

## 9. Current classification

```text
research_role = RARE_NATURAL_LIMIT
mode = P0_D
rare_natural_testbed_status = ADMITTED_FOR_EXPLORATION
rarity_source = DOMAIN_NATIVE_ONCOLOGY_EVIDENCE
selection_status = POST_RESULT
confirmation_status = NOT_CONFIRMATORY
promotion_debt = OPEN
limit_type = REPRESENTATION_STRESS_CAUSE_UNRESOLVED
```

**Conclusion:** PCPG is a legitimately rare natural oncology context and may be retained as a high-information P0-D limit testbed. Its GRI-specific scientific interpretation remains post-result and unconfirmed.