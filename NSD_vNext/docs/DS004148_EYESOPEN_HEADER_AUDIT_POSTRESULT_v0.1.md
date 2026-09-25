# NSD ds004148 Eyes-Open Dataset-Wide Header Audit Post-Result v0.1

Date: 25 September 2026
Status: CLOSED / SOURCE TOPOLOGY RESOLVED
Program authority: SymC General Operations Manual v0.8.6
Workflow run: `36141741703`
Artifact: `nsd-ds004148-eyesopen-header-audit-suite-v0-1`
Artifact digest: `sha256:95100244d0c0f0030c3fc8158ac9c00220809b9cc06efe8a68669b1f106a778a`

## Status

The header-only root-cause audit closed successfully across all 60 ds004148 subjects and all three eyes-open sessions.

All **180/180 VHDR records** passed pinned git-annex identity, MD5/size verification and header parsing. No EEG samples or signal-derived outcomes were opened.

## What happened

The dataset contains three 61-channel header signatures:

- 140/180 records use `Fpz` and `CPz`;
- 36/180 use `Fpz` and `Cpz`;
- 4/180 use `FPz` and `CPz`.

The variable labels are therefore exactly:

- `CPz` / `Cpz`;
- `Fpz` / `FPz`.

No sampling-rate, binary-format or orientation anomaly was found.

The exact label intersection across all 180 ds004148 eyes-open headers contains 59 labels. Because that dataset-wide intersection contains `TP9` and `TP10`, while the prior ds003775/sub-01 matched reference instead contained `Fpz` and `CPz`, the exact **cross-dataset** stable intersection is 57 labels.

The two prior matched labels that are not dataset-stable under exact semantics are:

- `CPz`;
- `Fpz`.

## Why the MFR-14 v0.1 failed

The nine `CPz` failures were not missing-electrode events. They were a case-sensitive source-label variant: those records carried `Cpz`.

The v0.1 replication correctly refused to equate them because its prospective rule prohibited silent renaming. The failure therefore exposed a source-semantic assumption before it could become hidden preprocessing.

## Disposition

No case normalization is introduced after the fact.

The next replication uses the 57 labels that are simultaneously:
1. present under exact labels across every audited ds004148 eyes-open record; and
2. present in the previously frozen ds003775 matched reference.

This 57-label set is frozen in:

`docs/manifests/ds004148_eyesopen_dataset_stable57_v0.1.json`.

The source audit does not establish any EEG, modal, chi, capital-Chi, clinical or recovery result.

## Checkpoint continuation

The next untouched replication is automatically assigned to `sub-16` through `sub-29`.

Those subjects were not part of the incomplete v0.1 cohort and their signal-derived outcomes have not been opened in this chain. The representation, subject-level endpoints and inferential contrasts remain unchanged; only the prospectively audited exact common coordinate space changes from the invalid 59-label assumption to the source-supported 57-label set.
