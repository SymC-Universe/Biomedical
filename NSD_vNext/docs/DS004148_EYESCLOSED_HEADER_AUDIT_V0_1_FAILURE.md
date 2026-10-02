# NSD ds004148 Eyes-Closed Header Audit v0.1 Failure Checkpoint

Date: 25 September 2026
Status: MECHANICAL/SOURCE-RETRIEVAL FAILURE UNDER INVESTIGATION
Program authority: SymC General Operations Manual v0.8.6
Workflow run: `36173622893`

The first eyes-closed source/header audit inspected 26/180 expected records and recorded 154 failures before exiting under the frozen incomplete-audit rule.

Independent source-tree verification at pinned OpenNeuro commit `0c740d838a2c33feeec0b6e514aea323d0e65ca4` confirms that all 180 expected `task-eyesclosed_eeg.vhdr` paths exist. Therefore the failure is not currently classified as absent source recordings.

A second mechanical packaging fault was also identified: the upload-artifact path used a literal `$RUNNER_TEMP` expression in YAML and therefore failed to preserve the diagnostic files after the main audit exited.

No EEG signal-derived value was opened. No scientific threshold, source cohort, label rule, or interpretation is changed.

Next action: add failure-class diagnostics to stdout, correct the artifact path expression only, and rerun the identical frozen 180-header source audit.
