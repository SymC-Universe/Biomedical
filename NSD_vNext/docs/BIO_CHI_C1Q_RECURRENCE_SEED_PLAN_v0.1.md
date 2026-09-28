# Bio Chi C1Q Recurrence-Seed Rescue Plan v0.1

**Status:** APQ-1 EXPLORATORY DRAFT  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0, Section 15.4  
**Lifecycle stage:** Stage 3, P0-Q optimizer root-cause / discriminating test  
**Parent root-cause:** \`BIO_CHI_C1Q_LIKELIHOOD_BASIN_POSTRESULT_v1.0.md\`

## Objective

Test whether a truth-blind initialization derived only from the observed positive-lag covariance can recover the lower C1Q likelihood basin that was reached by truth-seeded local optimization.

This is a discriminating initialization test, not an estimator change. The current C1Q search remains unchanged.

## Frozen source rows

Use the same 48 rate-level rows from cells

\[
\{0,5,7,8,9,11,12,15\}
\]

used in the completed likelihood-basin diagnostic.

Source-of-record artifacts:

- Function Map artifact \`10948327278\`, digest \`sha256:cb4ceade9271c80a5b002f0b9f6ba791ae3e0ae049b64ede0a3fdb0aee2b5a0c\`;
- likelihood-basin artifact \`10948127976\`, digest \`sha256:f8d5c1eae3a38d8b8751190767e78e264c91c44a1edacaf85619a781e9e1a105\`.

## Data-derived recurrence seed

For each realized signal, standardize exactly as C1Q does and compute normalized positive-lag sample covariances through lag 12.

Fit

\[
\gamma_{k+2}=a\gamma_{k+1}-b\gamma_k
\]

by least squares. If the fitted recurrence does not imply a stable underdamped pair with

\[
0<b<1,\qquad
\rho=\sqrt b,\qquad
-1<\xi=\frac{a}{2\rho}<1,
\]

the recurrence seed refuses for that row.

For an admissible recurrence,

\[
\theta=\arccos\xi,\qquad
L=-\ln\rho.
\]

At fixed \(\rho,\theta\), fit the C covariance amplitudes using

\[
\gamma_k
=
\rho^k A
\left[
\cos(k\theta)
+
g\frac{L}{\theta}\sin(k\theta)
\right],
\qquad k=1,\ldots,12.
\]

This is linear in the coefficients \(A\) and \(Ag\). Solve by least squares, then recover the unprojected \(A\) and \(g\).

For initialization only, project the fitted seed into the numerical C1Q domain:

- \(A\) is clipped only to the current C1Q reachable fraction interval;
- \(g\) is clipped only to the open numerical interval corresponding to the C family, \([-1+10^{-6},1-10^{-6}]\);
- \(\rho\) and \(f_d=\theta f_s/(2\pi)\) must already lie inside the C1Q model domain or the seed refuses.

The unprojected values and every projection/refusal are preserved.

## Execution

For each row with an admissible seed:

1. convert the recurrence/covariance seed to C1Q raw coordinates;
2. evaluate its starting NLL;
3. run one L-BFGS-B local optimization with the same C1Q likelihood and raw parameter box;
4. compare the resulting NLL continuously with:
   - the immutable source-selected NLL;
   - the completed truth-seeded local-basin NLL;
5. record physical/raw coordinates, condition number, covariance-fit residual, projection status, optimizer status, NLL differences, and parameter distances.

Rows with a refused recurrence seed remain in the result with the refusal reason.

## Numerical comparison tolerance

Use the same mechanical relative NLL tolerance as the parent root-cause diagnostic:

\[
10^{-6}\max(1,|\mathrm{NLL}_{reference}|).
\]

This tolerance is for numerical equivalence only and is not a scientific admission threshold.

## Outcome architecture

**Direct search-route support:** the data-derived seed repeatedly reaches a lower NLL than the existing selected solution and approaches or exceeds the truth-seeded basin within numerical comparison tolerance.

**Partial rescue:** the seed improves the existing solution but remains above the truth-seeded basin in a structured subset.

**Information/seed refusal:** recurrence or covariance amplitude estimation cannot produce an admissible C seed in some rows.

**Failure of this route:** the seed is usually admissible but does not improve the existing solution or does not approach the lower basin.

No outcome modifies C1Q automatically. A successful result only justifies a separately versioned C1Q search-route candidate followed by full Function/Limit requalification.

## Claim ceiling

P0-Q optimizer/search qualification only. No real-EEG admission, estimator promotion, biological prevalence claim, or scientific threshold.
