# NSD Local Workspace Standard

Effective 2026-09-08.

All future local Neural Stability Dynamics packages, extracted runners, and result bundles should be organized under one canonical Windows root:

`C:\Users\CCGTi\Documents\NSD_WORKSPACE`

Subfolders:
- `packages` - downloaded ZIP packages exactly as provided
- `runs` - extracted runnable packages, one named folder per phase/version
- `results` - copied/preserved completed result folders, one named folder per phase/version

Operational rule:
1. Do not use Downloads as the working location except as a temporary browser download landing point.
2. Move each new package into `packages` before extraction.
3. Extract into `runs\<phase_version>`.
4. After a run completes, preserve its output under `results\<phase_version>`.
5. Scientific code/config/rules hashes remain authoritative; moving or copying files does not change their contents.
6. Frozen scientific packages remain immutable. This standard changes only filesystem organization, not scientific assumptions, thresholds, or conclusions.

Assistant workflow rule:
- Future local instructions must target this canonical root unless the user explicitly asks otherwise.
- Give one command at a time during troubleshooting.
