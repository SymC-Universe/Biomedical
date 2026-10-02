# NSD ds004148 Eyes-Open MFR-14 v0.1 Failure / Root-Cause Record

Date: 25 September 2026
Status: CLOSED INCOMPLETE / NOT A SCIENTIFIC REPLICATION RESULT
Program authority: SymC General Operations Manual v0.8.6

## Failure lineage

### Attempt 1 — workflow run 36140613216

Artifact:
`nsd-ds004148-eyesopen-mfr14-replication-suite-v0-1`

Artifact digest:
`sha256:2bdbf2dc902ad5e0ccca59dedf3e6560c04215f1cc4e8f6b295767d1f2322ec4`

Result:
- 0/14 subjects completed;
- all 14 failed with the same `float(NoneType)` error before signal-derived subject outcomes;
- root cause: VHDR and VMRK are themselves git-annex symlinks in the pinned OpenNeuro repository, so the first runner incorrectly treated raw GitHub symlink content as the BrainVision header/marker payload.

Disposition:
`MECHANICAL_SOURCE_TRANSPORT_FAILURE`.

The correction generalized annex-key resolution to VHDR, VMRK and EEG and then verified all three downloaded NEMAR payloads against the pinned annex MD5/size identities.

### Attempt 2 — workflow run 36140957650

Artifact:
`nsd-ds004148-eyesopen-mfr14-replication-suite-v0-1`

Artifact digest:
`sha256:7b32f060ad04726f486cbcffd1ed2f1d860a06a39023b372f8d55f0ff7155a89`

Result:
- 5/14 subjects passed the source/D4 and 59-label gate;
- 9/14 subjects failed before cohort inference because eyes-open session3 lacked `CPz`;
- failed subjects: sub-02, sub-03, sub-04, sub-06, sub-08, sub-09, sub-10, sub-11, sub-12;
- failure string was identical in form: `ses-session3: missing matched labels ['CPz']`.

Disposition:
`REAL_SOURCE_CHANNEL_TOPOLOGY_VARIATION / REPLICATION DESIGN INVALIDATED`.

This is not a biological replication failure. It is a failure of the assumption that the sub-01 59-label cross-dataset intersection is stable across the independent ds004148 cohort.

## Scientific handling

The v0.1 replication remains incomplete. The five subjects that reached signal-derived computation do not rescue the frozen cohort, and their outputs are not promoted into a replication claim.

No subject replacement is performed within v0.1 because the freeze explicitly prohibited replacement after signal outcomes opened.

The next action is a header-only source audit across the full ds004148 eyes-open hierarchy. That audit may use channel labels and acquisition metadata only. It must not inspect EEG-derived spectral outcomes.

A later replication, if justified, must be separately versioned and freeze its common channel semantics from the header-only audit before any new cohort outcome is opened.

## Failure-as-evidence conclusion

The failure exposed an important Limit Map property of the source: channel topology is not safely inherited from one subject/session into the dataset-wide analysis.

This result therefore strengthens the project rule that cross-recording channel semantics must be audited at the cohort level before a common spatial feature space is frozen.
