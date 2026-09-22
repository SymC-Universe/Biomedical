# BioSystems tumor-normal biological closeout - 22 September 2026

**Status:** BIOLOGICAL CONTROL CLOSED  
**Program authority:** SymC General Operations Manual v0.8.3  
**Active protocol:** `BIOSYSTEMS_TUMOR_NORMAL_CONTROL_FREEZE_20260922.md` + `BIOSYSTEMS_TN_A1_TN_C1_EXECUTION_CONTRACT_20260922.md`  
**Protocol-lineage audit:** `BIOSYSTEMS_TUMOR_NORMAL_PROTOCOL_LINEAGE_AUDIT_20260922.md`

## Evidence returned

### TN-A1 RNA primary
Run `35796888899`, commit `72232b72415fb7579da09a4711448166772f4712`.  
Artifact `GRI_BIOSYSTEMS_TN_RNA_RESULTS_V01`, ID `10724424893`, digest `sha256:b2a72fd5483ab47b61369df5f082188bcc9a2d4caca494d032e51e3f5e48029e`.

12 frozen cancers, n=30 tumor and n=30 TCGA Solid Tissue Normal, 100 deterministic draws.

Primary results:
- `C_in,pair`: tumor lower in 12/12; median tumor-minus-normal -0.0560717; exact two-sided p=0.00048828125; BH q=0.00048828125.
- `C_in,PC1`: tumor lower in 12/12; median -0.0730223; p=0.00048828125; q=0.00048828125.
- `C_out`: tumor lower in 12/12; median -0.1085434; p=0.00048828125; q=0.00048828125.

All three frozen RNA coordinates therefore show a reproducible tumor-associated downward shift.

### TN-P20 paired RNA sensitivity
Same completed run and source identities. 13 frozen cancers, paired participant n=20, 100 deterministic paired draws.

- `C_in,pair`: tumor lower in 13/13; median -0.0657291; p=0.000244140625; BH q=0.0003662109375.
- `C_in,PC1`: tumor lower in 13/13; median -0.0719590; p=0.000244140625; q=0.0003662109375.
- `C_out`: tumor lower in 12/13; median -0.0964471; p=0.00341796875; q=0.00341796875.

The paired sensitivity independently preserves the primary RNA direction under same-participant tumor-normal comparison.

### TN-C1 multiomic primary
Run `35797400570`, commit `d02b94c43ec1c943d1137a4b1d1da1e690ca06fe`.  
Artifact `GRI_BIOSYSTEMS_TN_C1_RESULTS_V01`, ID `10725150891`, digest `sha256:17c23bc3e5d49d2c7936f6ac5357526fa8a3ed95933dd1d0257f028bf764cf3d`.

5 frozen cancers, n=30 per tissue state, 100 deterministic draws.

Primary-publication tumor-minus-normal results:
- H1 `delta_s`: lower in tumor 5/5; median -0.150234; p=0.0625; BH q=0.125. Every cancer's deterministic q05-q95 effect interval remains below zero.
- H2 `delta_cka`: 2 higher / 3 lower; median -0.0620062; p=1.0; q=1.0.
- H3a `delta_a_patient`: 1 higher / 4 lower; median -0.0286986; p=0.375; q=0.5.
- H3b `delta_a_label`: higher in tumor 5/5; median +0.0115684; p=0.0625; q=0.125. Magnitude is small and cancer-level construction intervals cross zero.

The masked-technical track preserves the main interpretation.

## Biological interpretation

The combined control rejects a simple tumor-only architecture model.

Adjacent normal tissue already carries strong RNA and methylation/RNA organization. Relative to that reference, tumors show a highly reproducible **loss of local/modular organization**:
- lower RNA internal pairwise coherence;
- lower RNA PC1 concentration;
- lower RNA external module coupling;
- lower methylation spectral organization.

At the same time, cross-layer organization is not uniformly erased:
- global methylation-RNA patient geometry remains present but its tumor-normal direction is cancer-dependent;
- patient-specific Hallmark coupling remains present and is mostly lower in tumor;
- same-label semantic advantage shows a small upward tumor tendency without frozen inferential resolution.

The supported statement is therefore **tumor-associated reorganization of pre-existing tissue architecture, dominated by loss of within-layer/modular coherence rather than wholesale disappearance of organization**.

This interpretation is narrower than causal regulatory collapse. It does not establish temporal progression, irreversible substrate capture, a biological damping coordinate, exceptional-point behavior, treatment response, or a scalar biological chi.

## Native-domain reality check

The direction is compatible with established cancer observations that tightly co-regulated expression modules in normal tissue change in tumors, while tumor-adjacent normal tissue is itself biologically distinct from non-cancer healthy tissue. This makes the present TCGA Solid Tissue Normal comparison an appropriate same-program specificity control but not a universal healthy baseline or independent external validation.

## GOM joint chi / capital-Chi disposition

The present result does not admit a biological scalar `chi`. No licensed dynamical rate pair or native scalar boundary is present.

The broader system-level result is nevertheless informative without scalar admission: local/module organization weakens reproducibly while some cross-layer organization persists and reorganizes. Under GOM v0.8.3 this is a valid narrower multirepresentational result, not permission to manufacture a master scalar.

The joint chi/capital-Chi relation therefore remains **UNRESOLVED / NOT IDENTIFIED for this static tumor-normal control**. The missing evidence is an ordered or perturbational representation capable of relating a licensed local stability coordinate to realized whole-system reorganization.

## Reviewer disposition

The reviewer request for normal controls is now **CLOSED**.

What can be claimed:
- prospective same-program tumor-versus-normal specificity/control;
- significant and directionally universal RNA architecture shifts across 12 primary cancers;
- replication of that direction in a 13-cancer same-participant sensitivity;
- consistent multiomic H1 weakening across all five eligible cancers;
- heterogeneous persistence/reorganization of cross-layer geometry.

What cannot be claimed:
- healthy-population specificity;
- independent external validation;
- causal methylation-to-RNA regulation;
- temporal collapse/recovery;
- clinical utility;
- biological chi or universal critical boundary.

The separate external-confirmation reviewer gate remains open and must not be relabeled as satisfied by this control.
