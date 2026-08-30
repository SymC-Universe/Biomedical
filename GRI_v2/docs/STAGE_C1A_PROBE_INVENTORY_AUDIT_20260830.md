# Stage C1A exact-probe annotation inventory audit

Date: 2026-08-30

Status: **STAGE_C1A_PROBE_INVENTORY_PASS**

## Scope

This audit closes the frozen local Stage C1A source/probe annotation gate. It verifies only exact source identity, exact probe identity, frozen annotation coverage, frozen probe-to-gene/region mapping integrity, and prespecified technical-mask overlap. It does not inspect methylation beta values for biological association and does not support any methylation mechanism, cross-assay coupling, substrate-inheritance, dynamic, optimum, treatment, or biological-chi claim.

## Canonical compact outputs

- `development_outputs/stage_c1a_probe_inventory/STAGE_C1A_PROBE_INVENTORY_SUMMARY.json`
  - submitted-file SHA-256: `04632061a28570f5eefcd41bd4abca230cd42e63538e02a9ab941b3cecf88168`
- `development_outputs/stage_c1a_probe_inventory/stage_c1a_regulatory_stratum_counts.csv`
  - SHA-256: `603b96ac879c4c58517479bc5dbee10bf89a0f47c374abd653c492d928de1cbc`

Larger local mapping/flag outputs remain outside Git history and are identified by hashes in the compact summary:

- probe-gene-region map SHA-256: `78f38d420a486427d67d88f67f5da83d1811003bf578b3c673f1dcbee5912296`
- probe flags SHA-256: `5777ff7331c4bae750ed1c87bb6eb93136c56ade6dbf8522829db1f5659ac455`

## Exact source and annotation checks

The local gate independently rehashed the already-audited PanCanAtlas methylation source and recovered the frozen source identity:

- methylation source SHA-256: `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`
- header columns: 12,040 total, consistent with one probe-ID field plus 12,039 methylation sample columns
- source probe rows: 22,601
- unique source probe IDs: 22,601
- annotation overlap: **22,601 / 22,601**
- missing annotation probes: **0**

The portable frozen annotation and Chen exports also matched their source-gate hashes:

- annotation export SHA-256: `a7f83233f97c3933752d74b8042e967de88df20eba2cf477a536136631a8da17`
- Chen ID export SHA-256: `078e95716af2b20c3515f59d09310d20c43deb5ed8ba8d1b70885810acde2179`
- portable source summary SHA-256: `b19297c4855ec12bc1fe4dd473742a72bef23db0b1b446258aa6a51b3679205b`

## Frozen gene/region mapping result

- RefGene-mapped source probes: 22,469
- RefGene-unmapped source probes: 132
- distinct preserved probe-gene-accession-region tuples: 46,287
- positional tuple-length mismatch probes: **0**
- mapped probes lacking a frozen regulatory stratum: **0**

The 132 unmapped probes remain admissible in all-probe modal space if otherwise eligible, but they are not assigned to invented nearest genes or Hallmark modules.

Regulatory-stratum unique-probe counts are:

- `PROMOTER_CORE` (`TSS200`): 3,999
- `PROMOTER_PROXIMAL` (`TSS1500`): 8,157
- `PROMOTER_TRANSCRIBED_EDGE` (`5'UTR` / `1stExon`): 9,455
- `GENE_BODY` (`Body`): 4,983
- `THREE_PRIME_UTR` (`3'UTR`): 152
- `BROAD_PROMOTER_SECONDARY`: 19,362

These strata are overlapping annotation views, not a partition of the 22,601 probes. A probe may map to more than one gene/region tuple and therefore contribute to more than one reported stratum where the frozen annotation supports it.

## Prespecified technical-mask robustness track

The primary publication-faithful track remains all exact 22,601 probes. The robustness-only technical mask is fixed independently of biological results.

Observed overlap with the exact PanCanAtlas probe set:

- Chen cross-reactive probes: 524
- common-SNP-at-CpG-or-SBE probes: 59
- union technical mask: 579
- robustness track remaining probes: **22,022**

No favorable-mask selection is permitted. Primary and masked tracks must both be reported in Stage C1, and a result cannot be promoted solely because one track is favorable.

## Gate decision

**PASS. Stage C1A is scientifically closed.**

Reasons:

1. the exact methylation source hash matches the frozen C0 source;
2. all 22,601 source probe IDs are unique;
3. all 22,601 source probes have exact frozen annotation rows;
4. no probe-gene-accession-region tuple-length mismatch was found;
5. the annotation and technical-mask artifacts match the frozen external-source gate;
6. the technical robustness set is completely determined before any beta-value biological analysis;
7. the run explicitly reports that methylation beta values were not parsed for biological association and no biological association was performed.

## Claim ceiling after C1A

C1A supports a reproducible, publication-era methylation probe/annotation/mask representation suitable for a prospectively frozen biological test. It does **not** establish methylation regulation of RNA, protein coupling, genomic control, causal structure, substrate inheritance, dynamics, damping, an exceptional point, a transition boundary, an optimum, treatment response, or biological chi.

## Next scientific gate

Before any Stage C1 beta-value biological computation, the program must freeze the exact C1 formulas and inferential rules for the complementary architecture:

- modal structure;
- scalar compression derived from and traceable to the modal carrier;
- conglomeration/module organization using the frozen probe-gene-region map;
- missing-data and eligibility rules;
- fixed-n resampling and deterministic seed construction;
- construction nulls;
- cross-assay patient-alignment and module-label nulls;
- primary versus secondary regulatory strata;
- promotion criteria and multiple-testing families.

This is a scientific specification gate. No C1 biological result may be inspected before that freeze is explicitly approved.
