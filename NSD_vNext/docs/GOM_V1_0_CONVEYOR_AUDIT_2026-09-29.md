# NSD / Bio Chi GOM v1.0 Conveyor Audit — 29 September 2026

**Authority:** SymC General Operations Manual v1.0 (27 September 2026) plus the mandatory Continuity Hardening Addendum.  
**Scope:** N-B1 and N-B2/N-B3 planning, APQ authority, long-run conveyor, checkpoint/resume, failure preservation, and continuity machinery.

## Audit disposition

The conveyor concept is compatible with GOM continuous execution only when every task it executes already has scientific authority. GitHub may execute, checkpoint, resume, hash, merge, and package frozen work; it may not create scientific authority or adjudicate claims.

The current implementation had one science-critical governance failure and several continuity-hardening defects.

### Science-critical failure

The N-B1 v0.3 architecture, N-B2/N-B3 v0.3 architecture, and long-run packet were treated as APQ-closed after two role-isolated passes by the same cognition. Under APQ-2 those passes are internal adversarial prechecks, not independent adversarial reviews. Substantive execution therefore opened before the required independent APQ gate.

Correction:
- architecture plan/ledger statuses corrected to independent-APQ outstanding;
- `LONG_RUN_EXTERNAL_APQ_STATUS_v0.1.json` created with `NOT_QUALIFIED` / `execution_authorized=false`;
- workflow and runner hard-gated on `QUALIFIED` independent APQ;
- queue moved to explicit `SCIENTIFIC_GATE`;
- existing opened rows classified in `LONG_RUN_EXPOSURE_LEDGER_v0.1.json` as P0-D exposed development evidence with promotion debt.

The exposed packet cannot later be relabeled untouched qualification. A future untouched packet requires fresh identities after independent APQ and any resulting prospective revision.

### Continuity-hardening defects

1. `USER_ACTION_REQUIRED` was absent from the machine continuity state grammar. It is now added as a distinct allowed state.
2. The checkpoint carried stale run identity `36648443486` while successor run `36648523189` was active. This is a false-liveness/stale-ID fault and is preserved as such.
3. The continuity sentinel originally checked age/state only. It is being strengthened to detect stale/terminal run IDs, missing checkpoints, empty unfinished queues, and monitoring-without-execution.
4. The long-run checkpoint used one combined stage rather than explicit lane-specific liveness. Before substantive resume, N-B1 and N-B2/N-B3 need separate lane stage/checkpoint/next-action fields.
5. Completed-case resume was based primarily on case ID plus file existence. Before substantive resume, each completed case must be hash-bound and checked against frozen packet/config/code identity.
6. Scientific code identity must remain stable across checkpoint commits. `LONG_RUN_CODE_MANIFEST_v0.1.json` binds the analysis source blobs independently of mutable result/checkpoint commits.
7. Runtime pressure must cause checkpoint/resume, never scientific simplification. The 330-minute work window plus reserve is compliant in principle.
8. Duplicate computation must remain suppressed by scientific input/config identity, not merely workflow/run identity.

## Scientific-method checks

The current scientific design remains aligned with the GOM in the following respects: native-model-first comparators are retained; local scalar chi, modal/vector Chi, and system/conglomerate behavior remain distinct; Function and Limit cases are both represented; failure/outlier rows are preserved rather than deleted; perturbation, transient response, observation mapping, and recovery remain explicit in N-B2/N-B3; practical identifiability remains separate from semantic model admissibility; and real-EEG local chi remains unlicensed.

No scientific result from the exposed long-run packet is adjudicated by this audit.

## Required authority chain before substantive resume

1. Preserve current exposed rows as development only.
2. Obtain isolated independent APQ-2 review(s) of the exact N-B1 v0.3 plan, N-B2/N-B3 v0.3 plan, packet/config/ceiling, and implementation identity. Reviewers must not be seeded with one another's conclusions.
3. Resolve BLOCKER/MATERIAL objections by evidence, native-model reasoning, or a prospectively defined discriminating test. Reviewer agreement is not a vote.
4. If any material plan/config change occurs, reactivate APQ and create a new version.
5. Freeze a fresh untouched qualification packet with fresh identities after APQ closure.
6. Bind code/data/config/checkpoint identities and run mechanical preflight.
7. Then allow GitHub to execute continuously to `SCIENTIFIC_REVIEW_READY`, where researcher + ChatGPT scientific review begins.
