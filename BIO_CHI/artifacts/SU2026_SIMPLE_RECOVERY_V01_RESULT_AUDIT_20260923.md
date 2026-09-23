# Su 2026 M397 simple recovery v0.1 result audit

**Date:** 23 September 2026  
**Status:** `RECOVERY_DYNAMIC_SUPPORTED` at P0-D  
**Workflow run:** `35891335924`  
**Workflow head:** `559e759a75ee02a3fcb530eb54f1f7dcfabd77e8`  
**Artifact:** `10765031675`  
**Artifact digest:** `sha256:67b35d6f9b002e539bd059f2ac3e24b0a8fac7e3fe0814ed63146c2c16181253`

## Frozen source

- GEO processed object: `GSE134459_Reversible_RPKM_values.txt.gz`
- SHA-256: `1ec204f02187289fdc0d718fe2291d34f2e3e6b943dcdf8fe627718d75a42d8c`
- retained genes: 22,843 / 22,843 source rows

The recovery metric and success conditions were frozen before expression values were opened for this analysis in:
`BIO_CHI/config/SU2026_SIMPLE_RECOVERY_V01_FREEZE.json`.

## Frozen metric

- transform all finite nonnegative trajectory rows with `log2(RPKM + 1)`;
- baseline = Control / Day 0;
- displacement = median across retained genes of absolute transformed-expression difference from Day 0;
- primary recovery statistic = Spearman correlation between days after drug removal and displacement across days 4, 10, 15, 17, 30, and 35;
- exact one-sided p-value from all 6! = 720 permutations.

## Result

Post-removal displacement:

| Days after removal | Displacement from Day 0 |
|---:|---:|
| 4 | 0.1288303337 |
| 10 | 0.1378024594 |
| 15 | 0.0869401792 |
| 17 | 0.0808418989 |
| 30 | 0.0513451883 |
| 35 | 0.0514658739 |

Late drug-on Day 59 displacement: `0.1620056079`.

Primary statistic:
- Spearman rho = `-0.8857142857`;
- exact one-sided permutation p = `0.0166666667`.

Frozen support conditions:
- rho < 0: PASS;
- exact p <= 0.05: PASS;
- Day35 < Day4: PASS;
- Day35 < late drug-on Day59: PASS.

Descriptive recovery fraction:
`1 - Day35/Day59 = 0.6823204170`, approximately 68.2%.

## Interpretation

This supports **realized transcriptomic recovery toward the pre-treatment expression state after drug withdrawal in this M397 melanoma trajectory under the frozen simple distance**.

It does not establish:
- universal cancer recovery behavior;
- recovery of every molecular layer;
- return to exact baseline;
- a causal methylation mechanism;
- a biological `chi_bio`, `Chi_bio`, or Bio Chi construction;
- a universal dynamical boundary;
- that the TCGA tumor-normal state difference itself is a failed-recovery phenomenon.

The first post-removal point is not monotonic relative to day 10, so the evidence is a strong overall return trend, not smooth exponential relaxation.

## Epistemic status

`P0_D_POSTRESULT_EXTENSION__RECOVERY_DYNAMIC_SUPPORTED`

This result may narrow a blanket nonclaim in a later manuscript revision but must remain explicitly separate from the original frozen C1/P1 confirmatory spine until independently confirmed or prospectively promoted.
