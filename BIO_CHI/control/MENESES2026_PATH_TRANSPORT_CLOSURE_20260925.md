# Meneses 2026 same-system perturbation-path transport closeout

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-path-transport-p0q-20260925`  
**Status:** CLOSED FOR THIS ITERATION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q, literature-open direct experimental transport qualification

## Status

The new path-transport gate executed successfully with zero source-fit failures across all 16 path-by-dose cells. It extends, rather than repeats, the closed Meneses direct-experimental Bio Chi result.

The parent result established that the sucrose osmotic perturbation/recovery event requires multicoordinate representation and does not license scalar `chi_bio`. The present experiment asks whether that same response organization transports when perturbation path or motor context changes.

## Frozen test result

All three alternate paths failed the prospectively frozen transport criterion relative to canonical sucrose/CCW.

| Alternate path | D_path | Raw permutation p | Holm p | Max absolute standardized median difference | Disposition |
| --- | ---: | ---: | ---: | ---: | --- |
| Sorbitol | 2.1032 | 0.000100 | 0.000300 | 1.6383 | PATH_DEPENDENT_REORGANIZATION_P0Q |
| Sodium-buffer assay | 1.4479 | 0.01950 | 0.01950 | 1.2524 | PATH_DEPENDENT_REORGANIZATION_P0Q |
| Clockwise-locked motor | 2.1805 | 0.000100 | 0.000300 | 1.4835 | PATH_DEPENDENT_REORGANIZATION_P0Q |

No comparison met the practical transport band of Holm-adjusted p >= 0.05 plus maximum standardized median difference <= 0.50.

## What changed

The source publication reports that the gross motor slowdown is qualitatively robust to osmolyte choice, buffer context, and rotation direction. The new result does not contradict that statement because the frozen object is finer grained.

The four-coordinate response organization was:
- collapse amplitude;
- collapse timescale;
- post-removal recovery timescale;
- recovery fraction.

At matched nominal shock strengths, these coordinates reorganized enough that the complete response vector did not transport unchanged.

Examples:
- sorbitol collapse was shallower and slower than canonical sucrose at 200 mM;
- sodium-buffer conditions were comparatively close in some amplitude/collapse coordinates at 200-300 mM but diverged in recovery timing and later conditions;
- clockwise-locked motors showed substantial amplitude and timing reorganization despite preserving the gross slowdown/recovery phenotype.

## Hierarchy consequence

**Biological chi:** admitted as a context-dependent perturbation/recovery relation at this source scope. The same broad biological function can be realized through measurably different internal response organization.

**Chi_bio:** retained as a multicoordinate motor-response organization. Its components are not interchangeable, and the vector itself is context conditioned.

**chi_bio:** remains `NOT_OPENED_NOT_LICENSED`. No identified oscillatory/modal carrier exists in these source fits, and a one-number compression is not rescued by the fact that all paths share a recognizable gross phenotype.

## Cross-project implication

This result is methodologically consonant with the wider Stability Inheritance program: preserving a gross system behavior does not require identical local coordinates. It therefore strengthens the need to distinguish:
1. phenotype/function preservation;
2. internal organizational transport;
3. scalar-coordinate transport.

It does not itself establish a universal substrate-inheritance law.

## Workflow identity

Run: `36218586127`  
Head SHA: `c9cd3afd4ebfd077d28ed825f414baa26cdb5f76`  
Artifact: `10897189701`  
Artifact digest: `sha256:3e127309661dd7e75aed175e3a63390a1c62e2760eec5e2220ac630108424d45`

## What happens next and why

The next high-value experiment is a **shape-only / matched-depth transport attack**. The present result shows path dependence, but some of that reorganization could arise simply because collapse depth differs. The next test should condition on or residualize collapse amplitude and ask whether recovery timing and recovery fraction still reorganize across paths.

If path dependence survives after depth matching, that would isolate a stronger statement: context changes recovery organization even when gross displacement magnitude is held comparable. If it disappears, then much of the apparent architectural difference is mediated by response depth rather than a separate contextual organization.

No user intervention is required before freezing that test.
