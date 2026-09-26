# Meneses 2026 depth-conditioned path closeout

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-depth-conditioned-p0q-20260925`  
**Status:** CLOSED FOR THIS ITERATION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q post-result conditional transport qualification

## Status

The frozen depth-conditioned transport attack executed successfully on 143 valid single-cell motor traces with zero source-fit failures.

The parent path-transport result remains valid: matched-dose four-coordinate response organization differs across sorbitol, sodium-buffer, and clockwise-motor paths relative to canonical sucrose. This follow-up asks the narrower question of whether path identity improves held-out prediction after collapse depth itself is included.

## Primary result

The depth-only model achieved held-out standardized MSE 1.38665. Adding path intercepts and path-by-depth interactions produced MSE 1.39921, a fractional change of -0.00906 rather than the frozen >=0.25 improvement required for path-context admission.

Across 2,000 frozen block-bootstrap resamples, median improvement was -0.0932 with 95% interval [-0.4202, 0.1103]. The interval spans zero and does not meet either the strong path-context rule or the strict depth-mediated rule.

Primary disposition:

`DEPTH_CONDITIONING_UNRESOLVED_P0Q`.

## Coordinate decomposition

The aggregate null does not mean every component behaved identically.

- collapse timing, `log(tau_dec)`: path terms improved held-out MSE by 25.3%;
- post-removal recovery timing, `log(|tau_inc|)`: path terms worsened MSE by 8.8%;
- recovery fraction: path terms worsened MSE by 26.0%.

These coordinate-specific results are descriptive under the freeze and cannot override the aggregate primary disposition.

## Interpretation

The prior path dependence cannot presently be promoted to the stronger claim that path context contributes predictive information independently of collapse depth across the complete recovery vector.

Equally, the data do not satisfy the frozen criterion for concluding that collapse depth fully mediates the observed reorganization. The bootstrap uncertainty is too broad for that statement.

The correct result is therefore narrower:

- path-dependent multicoordinate differences are established at matched nominal concentration;
- after explicit depth conditioning, the independent path contribution is unresolved;
- collapse timing remains a plausible context-sensitive component for future independent testing;
- scalar `chi_bio` remains unlicensed.

## Why this matters

This is a useful failure of the stronger interpretation. The path-transport result does not automatically imply a new hidden contextual state once response depth is considered. The current evidence supports multicoordinate organization but does not yet identify which coordinates are primary versus depth-mediated.

## Workflow identity

Run: `36218707913`  
Head SHA: `953e9f065fd8604ed8d370bf13b38369b5fe85e2`  
Artifact: `10898495701`  
Artifact digest: `sha256:3e403e16c8107117a38b6a688d44e2e2df762622836512a61654bc99cd44a620`

## What happens next and why

The strongest remaining lead from this source is collapse timing, because it was the only coordinate for which adding path information improved held-out prediction by the frozen 25% effect-size threshold. That signal is exploratory within this follow-up and cannot be promoted here.

A useful next step should therefore leave this dataset rather than repeatedly mine it. The next independent biological system should contain a directly measured perturbation magnitude plus at least one separable recovery-rate coordinate so that a depth-versus-rate distinction can be frozen before outcomes are known.

No user intervention is required to close this Meneses sequence.
