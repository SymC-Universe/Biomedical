# GSE342354 U2OS CCCP recovery analysis preflight

**Date:** 25 September 2026  
**Branch:** `bio-chi-u2os-cccp-recovery-p0q-20260925`  
**Status:** ANALYSIS FROZEN BEFORE EXPRESSION VALUES OPENED  
**Authority:** SymC GOM v0.8.6

## Source gate

GSE342354 passed source qualification before this contract was opened. All 12 frozen GSM identities resolve. The primary processed source is `GSE342354_Processed_data.txt.gz`, SHA-256 `fd088eb4e50e9a2ab6bb428b2566029d0177c7f4a596f0effc8f846161e472af`. The source contains 12 raw-count columns matching three biological replicates each for WT, CCCP, 1 h washout, and 6 h washout.

The first source-enumerator run failed because an NCBI directory parser followed an external HHS footer link. That implementation failure is preserved separately. The repaired source run qualified successfully without opening expression values.

## Whole event first

The frozen biological question is whether the CCCP-displaced transcriptomic state moves back toward untreated organization after perturbation removal, and whether that recovery can be represented adequately along one state axis.

The analysis does not begin from a pathway, DE gene list, or source-reported stress signature. The primary gene space is fixed label-blind from source protein-coding counts.

## Primary state geometry

The untreated and CCCP centroids define the damage vector. Washout states are assessed by:

- Euclidean distance back to the untreated centroid;
- recovery fraction relative to the acute damage distance;
- position along the frozen WT-to-CCCP perturbation axis;
- orthogonal displacement away from that axis.

Biological-replicate bootstrap uncertainty, not genes-as-replicates, determines the recovery interval.

## Representation attack

The four condition centroids are jointly tested for one-dimensional adequacy. Passing requires at least 95% PC1 variance, maximum rank-1 reconstruction residual no greater than 10% of the acute damage distance, and the same two criteria in at least 95% of replicate-bootstrap realizations.

Failure means the recovery path requires multicoordinate `Chi_bio` representation at this source scope. Passing would establish only a one-dimensional state path, not scalar `chi_bio`.

## Scalar gate

Scalar `chi_bio` is not opened. Bulk RNA-seq replicate means/variances, PCA positions, and recovery fractions are not treated as a mechanical damping carrier.

## Next action

Verify the pinned file hash, parse the frozen count columns, execute the primary and prespecified sensitivity geometries without retuning, and preserve positive, negative, unresolved, or multicoordinate outcomes unchanged.
