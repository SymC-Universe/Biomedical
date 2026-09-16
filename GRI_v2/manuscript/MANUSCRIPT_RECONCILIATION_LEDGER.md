# GRI oncology manuscript reconciliation ledger

**Status:** LIVING EDITORIAL/PROVENANCE LEDGER — NOT A SUBMISSION FREEZE  
**Date opened:** 2026-09-16  
**Integrated draft:** `LIVING_MANUSCRIPT_DRAFT.md`  
**Current status:** `../notes/CURRENT_STATUS_20260916_GOM_V080.md`

## Purpose

This ledger keeps the manuscript attached to repository evidence while the paper is still changing. It is deliberately separate from the manuscript prose so that incomplete integrations, figure rebuilds, numerical sourcing, and claim-ceiling checks remain visible instead of being hidden in memory or old local copies.

A row marked `READY FOR DRAFT` means the scientific content is sufficiently settled to write or revise prose at the current claim ceiling. It does not mean final submission-ready. A row marked `WAITING ON SOURCE RECONCILIATION` does not authorize recomputation of frozen science merely to fill a manuscript blank.

## Section reconciliation

| Manuscript component | Current state | Evidence/source to reconcile | Editorial action | Blocker |
| --- | --- | --- | --- | --- |
| Working title | PROVISIONAL | Current program architecture | Keep broad architecture framing; do not promise admitted `Chi_bio` | Final paper emphasis may shift |
| Abstract | READY FOR ITERATIVE EDIT | Static Pan-Cancer + SCC25 G2 + B3 refusal + G1 restoration state | Keep layered architecture central; retain explicit no-`Chi_bio` claim | Final numerical selection |
| Introduction | READY FOR ITERATIVE EDIT | Historical `CV/2`, current GOM/GRI guardrails | Preserve proxy/mechanism distinction; explain why scalar/modal/system separation became necessary | Citation polishing |
| Conceptual architecture | READY | Function/Limit/Evidence map 2026-09-16 | Fold in current GOM v0.8.0 wording where useful without turning governance into the scientific result | None |
| Static RNA architecture | WAITING ON NUMERICAL RECONCILIATION | Frozen Stage A/A1 artifacts | Insert final values, uncertainty, figure references | Exact source-value extraction |
| Composition/genomic context | WAITING ON NUMERICAL RECONCILIATION | Frozen Stage B1/B2 artifacts | Insert values and bounded interpretation | Exact source-value extraction |
| Protein/phosphoprotein | WAITING ON NUMERICAL RECONCILIATION | Frozen RPPA/B2 artifacts | Insert matched-n, null, effect statistics | Exact source-value extraction |
| Methylation/substrate | WAITING ON NUMERICAL RECONCILIATION | Stage C1 + post-C1 frozen evidence | Integrate corrected H2/H3a/H3b ceilings and modal/context results | Read-only artifact reconciliation |
| SCC25 short-term G2 | READY | Frozen GSE114446 result | Keep prospective failure/refusal visible | None |
| SCC25 chronic G2 | READY | Frozen GSE98812 primary + bounded feature-gate audit | Keep mathematical unit-circle result separate from biological criticality | None |
| B3 state-identifiability | READY | Frozen matched-network holdout + topology audit | Report refusal as compression/identifiability boundary | None |
| G1 restoration | ACTIVE SECTION | `sections/06_G1_RESTORATION_IDENTIFIABILITY.md` + frozen G2 lineage | Integrate only results actually earned by R0/kinetic-identifiability work | Current restoration analysis state |
| `Chi_bio` admission | READY AT CURRENT CEILING | PR #4 freezes + B3 refusal + restoration block | Keep `NOT_ADMITTED`; do not insert cancer placements | New representation would require prospective freeze |
| Discussion | READY FOR ITERATIVE EDIT | Function/Limit/Evidence map | Lead with architecture + informative refusals; separate mechanistic aspirations from earned results | Final integrated evidence |
| Limitations | READY FOR ITERATIVE EDIT | Current status + independence map | Keep static/dynamic, dependence, representation, restoration, platform limits explicit | Final integrated evidence |
| Methods | NEEDS CONSOLIDATED BUILD | Frozen stage protocols, configs, code, amendments | Rebuild as exact versioned methods map; preserve prospective amendments | Large reconciliation task, no new science required |
| Supplement | NEEDS CONSOLIDATED BUILD | Frozen stage protocols, sensitivity tables, refusal ledger | Preserve full audit trail without drowning main text | Large reconciliation task |
| Reproducibility guide | NEEDS CONSOLIDATED BUILD | repo code/configs/artifacts/manifests | Build run/read-only distinction and exact source paths/hashes | Artifact inventory reconciliation |
| References | ACTIVE | primary literature + source audits | Verify all metadata against primary sources before submission freeze | Final bibliography check |

## Figure reconciliation

### Figure 1 — overall regulatory stability architecture

**Status:** REBUILD REQUIRED.

Replace historical wording that implies a universal or already-established critical failure boundary. Show scalar, modal/vector, and conglomerate/system views as complementary entry points into the GRI architecture. Include epistemic labels or a concise legend distinguishing static structure, temporal qualification, and refusal/non-identifiability.

**Do not include:** `Critical Failure` as an established biological regime, historical unresolved `Energy Omega`, or a visual `Chi_bio = 1` cancer divider.

### Figure 2 — measurement layers and evidence firewall

**Status:** REBUILD REQUIRED.

Replace historical `Forensic Capture` framing and unresolved physicalized axes. Show measured layers: RNA, methylation/substrate, composition/context, genomic context, protein/phosphoprotein, and temporal/perturbational evidence. Show which links are measured, inferred, contextual, or not established.

### Figure 3 — static Pan-Cancer architecture

**Status:** SPECIFICATION READY; VALUES TO RECONCILE.

Target: RNA organization plus bounded composition/genomic context. Use only source-verified values from frozen artifacts. Figure caption must state static/cross-sectional scope.

### Figure 4 — methylation/RNA cross-layer architecture

**Status:** SPECIFICATION READY; VALUES TO RECONCILE.

Target: cross-layer geometry, modal behavior, patient-specific coupling, and robustness/limits from C1/post-C1. Do not use the historical proxy as if it were a dynamical coordinate.

### Figure 5 — SCC25 Function/Limit temporal comparison

**Status:** READY FOR DESIGN.

Pair short-term prospective refusal with chronic bounded functioning. Show rank and feature-gate dependence explicitly. If plotting spectral radius relative to 1, label it as the mathematical discrete-time unit circle, not biological `Chi_bio`.

### Figure 6 — `Chi_bio` admission/falsification architecture

**Status:** READY FOR DESIGN.

Show G1 theoretical route, G2 temporal comparator, B3 compact-identifiability refusal, G1 restoration gate, G4 alternative family, and the Independent Atlas firewall. End state should visibly permit `NOT_ADMITTED` and `NO_COHERENT_LOW_DIMENSIONAL_STATE` rather than implying that a scalar must emerge.

### Figure 7 — G1 restoration inverse problem

**Status:** CONDITIONAL.

Use only if restoration work becomes central enough for the main text. Candidate schematic:

`T -> admissible J_eff -> restoration family D -> normalized G1 family -> invariant conclusion OR NOT_IDENTIFIABLE`.

The figure must not visually steer the family toward unity.

## Numerical-source rule

Before a number enters final prose, table, or caption, record:

1. exact artifact/file path;
2. frozen version/run/commit where applicable;
3. field/table/row or deterministic derivation;
4. uncertainty/tolerance attached to the number;
5. evidence class;
6. whether the value has been independently reproduced or only read from the original frozen artifact.

No number is sourced from AI recall or an older manuscript merely because the value looks familiar.

## Claim-ceiling audit checklist

Before each manuscript milestone, verify:

- no historical `CV/2` language has silently become mechanistic `Chi`;
- no static result is described as recovery, damping, resilience, or temporal inheritance;
- no mathematical unit-circle statement is phrased as a biological unity boundary;
- no B3 refusal is erased by a later exploratory representation;
- no evidence reused from SCC25 or TCGA is labeled untouched P1;
- no local/embedded distinction is collapsed;
- no Atlas placement is used to define the state coordinate;
- no clinical, therapeutic, prognostic, or causal claim exceeds the evidence class;
- Function and Limit results receive comparable visibility;
- all figure labels agree with the main text and source artifacts.

## Planned manuscript workflow

The manuscript can be edited continuously on the active branch. Not every repository commit requires a prose change. Material evidence changes should trigger one of three actions:

- edit `LIVING_MANUSCRIPT_DRAFT.md` if the integrated narrative changes now;
- edit/create an indexed current section file if the section is under active evidence development;
- update this ledger if the evidence is real but prose integration should wait for a later consolidation pass.

Only the later explicit submission freeze will convert this workspace into a line-by-line authoritative release candidate.
