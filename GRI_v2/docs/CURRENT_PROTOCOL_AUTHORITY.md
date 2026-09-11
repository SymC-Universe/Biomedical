# Current GRI protocol authority

**Effective date:** 2026-09-10  
**Last GRI verification:** 2026-09-11

The current governing cross-project protocol package for prospective GRI work is:

`General_Cross_Project_Research_Protocol_v0.7.1_FINAL_plus_v0.7.1A_Addendum.pdf`

This package contains Final v0.7.1 plus the v0.7.1A Functional Mapping and Natural Limit-Testbed Addendum.

Where older migration documents on this branch name only `v0.7.1 FINAL`, read them as the pre-addendum baseline and use these newer integration records for current prospective control:

- `docs/GRI_V071A_PROTOCOL_AUDIT_20260910.md` — canonical detailed v0.7.1A migration audit;
- `docs/GRI_V071A_FUNCTION_LIMIT_INTEGRATION_20260910.md` — canonical Function/Limit operational integration;
- `docs/GRI_V071A_FULL_AUDIT_20260911.md` — current verification/delta audit, not a duplicate procedure set;
- `notes/CURRENT_STATUS_20260910_V071A.md` — current operational project state, content refreshed 2026-09-11;
- `notes/BUILD_STATUS.md` — current build/scientific status;
- `docs/GRI_CONTROL_DOCUMENT_SUPERSESSION_MAP_20260910.md` — precedence and historical-control interpretation.

The addendum does not retroactively alter the epistemic status of existing GRI results. It prospectively adds P0-D/P0-Q separation, coequal Function/Limit mapping, qualified rare-natural-limit use, research-role coverage, pathway-specific independence, and Function/Limit output requirements.

## Current implementation note

Machine-readable protocol-facing output semantics are represented by:

- `config/gri_v071a_tool_output_schema_draft.json`;
- `src/protocol_contracts.py`.

They are draft control-plane artifacts, not a frozen scientific Engine. CI now cross-checks the JSON schema against the executable protocol contract so required groups, research modes, Function/Limit states, coverage roles, pathway-independence dimensions, and prohibited rare-testbed selection bases cannot silently drift apart.
