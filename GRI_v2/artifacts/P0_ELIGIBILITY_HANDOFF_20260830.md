# GRI v2 P0 sample-eligibility handoff record

Date: 2026-08-30

## Current gate

P0 pre-eligibility split audit is PASS. The next frozen operation is the per-sample PRIMARY_PUBLICATION missingness screen before any discovery-only feature fitting.

Frozen rules inherited without modification from the P0 holdout protocol:

- exact participant split remains fixed;
- 22,601 PRIMARY_PUBLICATION methylation probes;
- a participant is eligible only when at least 95% of those probes are finite;
- a cancer is fully evaluable only when at least 30 eligible participants remain independently in DISCOVERY, REPLICATION, and FINAL_HOLDOUT;
- pan-cancer promotion requires at least 24 fully evaluable cancers;
- no partition reassignment/rebalancing;
- no RNA Hallmark predictive target values or other predictive outcomes are read in this gate;
- no biological association, biological chi, survival, treatment, subtype, or preferred-pattern selection is allowed.

The pre-eligibility fixed split already makes the 24-cancer promotion floor unreachable. That consequence is retained prospectively: individual cancer P0 evaluation may proceed where eligible, while P0 pan-cancer aggregates remain descriptive.

## Tested Windows handoff

Local handoff archive built and independently extracted/tested:

- archive: `GRI_V2_P0_ELIGIBILITY_WINDOWS_20260830.zip`
- SHA-256: `1dd433b6c50fa80329820c05d5f0bd2abce2e4ba55be8b4c26abc760d6b91876`
- package contract tests: 3 passed
- internal SHA256SUMS verification: all payload files PASS

The Windows runner asks for exactly two local files:

1. the same C0-audited 5.02 GB methylation TSV;
2. `p0_preeligibility_split_manifest.csv` from the completed split run.

The Hallmark/RNA cache is not selected again at this gate because its participant identities are already bound into the frozen, hash-verified P0 manifest. RNA Hallmark target values remain unopened.

## Expected compact return files

- `P0_ELIGIBILITY_SUMMARY.json`
- `p0_sample_eligibility.csv`
- `p0_partition_eligibility_counts.csv`

After those files are returned and audited, the next allowed gate is DISCOVERY-only probe eligibility/imputation and cross-omic feature construction for fully evaluable cancers only.
