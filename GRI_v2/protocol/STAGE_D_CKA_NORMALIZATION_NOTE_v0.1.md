# Stage D CKA normalization note v0.1

Status: FROZEN MATHEMATICAL DEFINITIONS BEFORE STAGE-D BIOLOGICAL OUTCOME INSPECTION

For centered PSD sample-space kernels K_M and K_R of common dimension n, let eigenvalues lambda_i and mu_i be sorted descending.

## Random-permutation expectation

For a uniformly random patient permutation P,

E_P[<K_M, P K_R P^T>_F] = tr(K_M) tr(K_R)/(n-1).

The equality follows by splitting diagonal and off-diagonal terms. For centered K_R:
- E[(P K_R P^T)_{ii}] = tr(K_R)/n;
- for i != j, E[(P K_R P^T)_{ij}] = -tr(K_R)/(n(n-1)), because the total sum of all kernel entries is zero;
- summing diagonal and off-diagonal contributions against centered K_M gives the stated numerator expectation.

Because ||P K_R P^T||_F = ||K_R||_F for every permutation, the CKA denominator is permutation-invariant. Therefore the expected CKA is exactly the expected numerator divided by the fixed denominator:

E_P[CKA] = tr(K_M) tr(K_R)/((n-1)||K_M||_F ||K_R||_F).

Equivalently, with participation ratio r(K)=tr(K)^2/||K||_F^2,

E_P[CKA] = sqrt(r_M r_R)/(n-1).

## Fixed-spectrum alignment ceiling

By von Neumann's trace inequality, the largest Frobenius inner product obtainable by orthogonal alignment of two fixed PSD spectra is

max_Q tr(K_M Q K_R Q^T) = sum_i lambda_i mu_i

when eigenvectors are aligned in common descending spectral order. Hence

CKA_max = sum_i lambda_i mu_i/(||K_M||_F ||K_R||_F).

CKA_max <= 1, with equality only when the two eigenvalue sequences are proportional up to scale.

## Candidate realized-alignment fraction

Stage D permits the descriptive quantity

A_realized = (CKA_obs - E_P[CKA])/(CKA_max - E_P[CKA])

only when the denominator is numerically well resolved. This quantity is not called stability, resilience, rigidity, slack, inheritance, or a biological chi coordinate.

The empirical permutation distribution remains required for finite-sample uncertainty and inferential calibration. The analytic floor and spectral ceiling are bounds/expectations, not substitutes for the realized null distribution.
