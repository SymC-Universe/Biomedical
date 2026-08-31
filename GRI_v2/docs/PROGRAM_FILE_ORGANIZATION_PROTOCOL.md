# Program file organization protocol

Status: active workflow protocol
Scope: all future user-facing SymC/GRI handoffs and, by standing practice, all future program handoffs produced through this project workflow.

## Purpose

Keep technical provenance rigorous without forcing the user to decode long filenames, version tails, dates, hashes, or internal stage codes during routine execution.

## User-facing naming rules

1. User-facing downloads use short descriptive names. Dates, commit SHAs, hashes, and internal version strings belong inside manifests, not in the filename unless they are scientifically necessary to distinguish incompatible artifacts.
2. Every executable handoff exposes a plainly named `START_HERE.bat` at the package root whenever Windows execution is required.
3. Every handoff includes `README_FIRST.txt` containing only: what this package does, which files the user must select, what successful completion looks like, and exactly which output(s) to return.
4. Reusable frozen inputs use stable human-readable names such as `Hallmark_Genes.gmt`, `Patient_Split.csv`, `Sample_Eligibility.csv`, or similarly descriptive names. Original technical filenames and hashes remain recorded in the manifest.
5. A filename may be renamed for usability when content identity is protected by SHA-256 and the workflow validates content rather than relying on the old filename.

## Access tiers

- `NOW`: only the files required for the current step.
- `REUSE`: small frozen inputs expected to be needed again soon.
- `RETURN_TO_CHAT`: outputs the user must upload after the current step.
- `ARCHIVE`: completed handoffs, superseded launchers, historical versions, and provenance-only artifacts.

New packages should mirror these roles internally when practical and should never require the user to infer which file matters from a crowded directory.

## Handoff construction rules

- Bundle small frozen dependencies directly whenever licensing and size allow.
- If a required dependency cannot be bundled, identify its exact human-readable name and the prior package/folder where it was created or last used.
- Do not ask the user to search a large archive without first identifying the exact target filename.
- Never make the user choose among multiple similarly named technical versions without a hash-gated selector or an explicit single-file instruction.
- A current-step package should contain no unnecessary historical outputs.
- Completed results move conceptually to ARCHIVE; they are not presented as active inputs unless reused.

## Provenance preservation

Simpler filenames do not relax scientific provenance. Each package must retain an internal manifest recording, as applicable: canonical/original filename, SHA-256, source identity, commit SHA, workflow/run ID, frozen config version, generation date, and supersession status.

## Communication rule

Whenever user action is required, instructions state the exact file(s) to touch in plain language first. Internal stage IDs and hashes may follow for verification, but they do not replace the plain-language instruction.
