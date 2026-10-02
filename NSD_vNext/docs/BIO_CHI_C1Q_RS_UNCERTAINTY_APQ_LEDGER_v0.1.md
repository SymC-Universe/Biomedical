# Bio Chi C1Q-RS Uncertainty Map APQ Ledger v0.1

**Plan reviewed:** `BIO_CHI_C1Q_RS_UNCERTAINTY_MAP_PLAN_v0.1.md`  
**APQ level:** APQ-2 SUBSTANTIAL  
**Review limitation:** two role-isolated passes from one cognition; not independent reviewers.

| ID | Severity | Issue | Disposition | Plan effect |
| --- | --- | --- | --- | --- |
| A1 | MATERIAL | eight truth cells cannot support causal regional claims | ACCEPTED_MODIFIED | cross-cell relationships remain visual/descriptive only; no causal or general envelope law |
| A2 | MATERIAL | repeated C-family truths measure estimator sampling uncertainty, not model uncertainty | ACCEPTED_MODIFIED | terminology changed to estimator sampling distribution under correct specification |
| A3 | MINOR | information context should remain visible | ACCEPTED_MODIFIED | retain A, observation-noise fraction (1-A), frequency, duration, and cycles observed in summaries |
| B1 | MATERIAL | 5th/95th quantiles with n=12 overstate tail precision | ACCEPTED_MODIFIED | use full row distribution plus median, quartiles, range, mean, SD, and MAD; no tail interval claim |
| B2 | MATERIAL | numerical-boundary count lacked frozen definition | ACCEPTED_MODIFIED | numerical raw-boundary flag = minimum distance to any ([-8,8]) raw box edge <= (10^{-6}) |
| B3 | MATERIAL | wide distributions may mix sampling variance and optimizer pathology | ACCEPTED_MODIFIED | boundary and optimizer states retained as separate row fields/counts; no row excluded from full distributions |
| B4 | MINOR | repeated-seed provenance must be explicit | ACCEPTED_MODIFIED | exact cell table, seed list, RNG class, environment, and commit captured in artifact |

## Resolution

No BLOCKER remains. All MATERIAL objections are resolved by claim limitation or pre-execution reporting changes. No scientific coordinate, seed, duration, sampling rate, or estimator implementation changed.

## Shared-premise challenge

Both passes inherit the assumption that correct-specification C truths are worth characterizing. That is intentional: the plan measures C1Q-RS sampling behavior conditional on the C model being correct. It cannot evaluate semantic model membership or model uncertainty, and those claims remain outside scope.

## APQ disposition

The revised v0.2 plan is eligible for freeze and execution as bounded P0-D/P0-Q uncertainty qualification.
