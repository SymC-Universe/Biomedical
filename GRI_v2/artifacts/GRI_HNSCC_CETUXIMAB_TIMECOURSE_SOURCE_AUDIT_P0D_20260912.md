# GRI HNSCC cetuximab time-course source audit

**Date:** 2026-09-12  
**Status:** P0-D SOURCE / IDENTITY ARCHITECTURE AUDIT ONLY  
**Chi_bio status:** `NOT_ADMITTED`  
**GRI outcomes on this source:** `UNOPENED`  
**P1 status:** `NOT_SELECTED_NOT_FROZEN`

## 1. Source identity

**Study:** Stein-O'Brien G, Kagohara LT, Li S, et al. *Integrated time course omics analysis distinguishes immediate therapeutic response from acquired resistance.* Genome Medicine 10, 37 (2018).  
PMID: `29792227`  
PMCID: `PMC5966898`  
DOI: `10.1186/s13073-018-0545-2`

**Public deposits**

- RNA-seq: `GSE98812`
- DNA methylation: `GSE98813`
- SuperSeries: `GSE98815`
- methylation platform: `GPL13534`, Illumina HumanMethylation450 BeadChip
- RNA platform in SuperSeries: `GPL16791`, Illumina HiSeq 2500

## 2. Native experimental design

The model is the cetuximab-sensitive human HNSCC cell line SCC25.

Frozen source facts from the paper/GEO record:

```text
treatment = 100 nM cetuximab every 3 days
control = time-matched PBS
ordered duration = 11 weeks
ordered generations = G1 ... G11
harvest cadence = weekly / eighth-day harvest-replate cycle
main treated/control time-course states = 22
RNA = RNA-seq
DNA methylation = 450K array
phenotype = proliferation relative to PBS control
```

The paper states that genome-wide DNA methylation was performed on the **same samples as RNA-seq**.

At each generation, replicated culture flasks were harvested and pooled to produce enough material for molecular and proliferation assays. Therefore the weekly molecular profile is one pooled state per treatment arm rather than an independently replicated biological panel at each timepoint.

## 3. Exact ordered state structure

GEO exposes paired labels for each week:

```text
week 1   PBS / 100 nM cetuximab
week 2   PBS / 100 nM cetuximab
...
week 11  PBS / 100 nM cetuximab
```

For methylation, `GSE98813` lists the weekly state sequence as `GSM2612502` through `GSM2612523`, alternating PBS and cetuximab after the baseline entry. The SuperSeries lists the corresponding RNA weekly sequence as `GSM2612466` through `GSM2612487`.

The study also deposits parental/baseline samples and independent stable cetuximab-resistant clones. These are not silently merged into the 22-state longitudinal series.

## 4. Phenotypic state information

Resistance is not inferred from omics alone. The authors measured proliferation and compared cetuximab-treated cells with time-matched PBS controls.

The reported trajectory is:

- early treatment: growth inhibition through approximately G1-G3;
- around G4: treated/control absolute proliferation becomes similar;
- G4-G8: progressive acquired-resistance interval;
- G8-G11 / especially G9-G11: sustained growth advantage / later stabilized resistant behavior relative to control.

This phenotype is valuable because it can serve as an independently meaningful response axis rather than being algebraically built from a future Chi_bio candidate.

## 5. Representation relationship to current GRI

### Strong compatibility

- methylation platform is 450K, close to the current TCGA methylation representation;
- transcriptome is RNA-seq;
- the paper used an RNA normalization workflow modeled after the TCGA RSEM v2 pipeline;
- methylation and RNA were measured on the same ordered biological states;
- both treated and time-matched control trajectories exist.

### Non-equivalence that must remain visible

- cell-line model rather than bulk patient tumors;
- one biological lineage rather than a pan-cancer cohort;
- pooled culture replicates rather than independent biological replicates at each week;
- serial descendants/generations are ordered states, not independent samples;
- continued drug exposure rather than washout/recovery;
- resistance evolution may include clonal selection/outgrowth as well as regulatory change.

No adapter may erase these differences merely to make the source look more TCGA-like.

## 6. Chi_bio opportunity and limits

### What this source can potentially test

If a Chi_bio candidate is frozen independently first, this source may support:

- boundary-blind trajectory of the candidate across 11 ordered treated states;
- matched-control trajectory across 11 PBS states;
- relation of scalar movement to modal reorganization;
- relation of conglomerate methylation/RNA organization to resistance acquisition;
- whether a candidate changes before, near, or after the independently measured proliferation transition;
- whether a candidate refuses during states where a coherent scalar compression is not identifiable.

### What this source cannot establish by itself

- pan-cancer generality;
- patient-level clinical utility;
- recovery after drug removal;
- a causal methylation-to-RNA mechanism;
- a universal Chi_bio construction;
- a Chi_bio=1 boundary merely because a trajectory crosses 1;
- precise fast-time response parameters that weekly sampling cannot identify.

## 7. Independence / leakage disposition

Current source selection occurred because of **measurement architecture and temporal resolution**, after the Chi_bio experimental-opportunity design was frozen and before any GRI Chi_bio outcome on this source exists.

```text
selection_status = P0_D_SOURCE_DISCOVERY
selection_basis = DENSE_ORDERED_PAIRED_MULTIOMIC_ARCHITECTURE
selected_by_GRI_agreement = false
Chi_bio_outcomes_opened = false
p1_status = NOT_SELECTED_NOT_FROZEN
```

The source is not independent of the broader scientific literature used to define cancer resistance as a domain problem, but it is presently outcome-unopened with respect to Chi_bio.

## 8. Remaining mechanical/source gates before computation

1. export the complete RNA and methylation GSM state manifests;
2. verify the 36-vs-36 modality inventories and exact state correspondence rather than relying only on title symmetry;
3. hash downloaded source files;
4. define which baseline replicate belongs to which role without averaging after outcome inspection;
5. keep the 22-state main time course separate from stable resistant clones;
6. preserve treatment/control/week labels verbatim;
7. reconstruct the exact proliferation values or source table used as the independent phenotype axis;
8. freeze a representation adapter before Chi_bio values are inspected;
9. account for serial dependence and pooled-replicate structure in uncertainty;
10. preserve original published filtering as provenance but do not automatically inherit outcome-informed gene filters into a GRI confirmatory adapter.

## 9. Critical filtering firewall

The published paper selected RNA genes based partly on fold-change across timepoints and methylation loci based partly on switching across time-course samples before integrated CoGAPS analysis. Those filters are valid for the published study but are **outcome/data-structure informed with respect to this new Chi_bio question**.

Therefore a future GRI Chi_bio adapter must not blindly reuse that filtered 6,445-RNA / 4,703-methylation feature set as though it were prospectively independent. Prefer native/raw or independently frozen feature rules aligned with the Chi_bio System Model.

## 10. Current disposition

```text
source_priority = VERY_HIGH
research_role = PERTURBED_FUNCTION + BOUNDARY_OR_TRANSITION
representation_class = CLOSE_BULK_MULTIOMIC_MATCH_WITH_CELL_LINE_AND_SERIAL_DEPENDENCE_LIMITS
identity_status = SOURCE_LABEL_STRUCTURE_STRONG_EXACT_MANIFEST_EXPORT_PENDING
Chi_bio_status = NOT_ADMITTED
p1_status = NOT_SELECTED_NOT_FROZEN
```

This source materially reduces the likelihood that a new wet-lab experiment is required for the **first temporal Chi_bio falsification pass**. It does not remove the need for external transport beyond one cell-line system if a candidate survives.