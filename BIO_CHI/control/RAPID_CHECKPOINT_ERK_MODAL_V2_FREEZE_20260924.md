# Bio Chi ERK modal v2 rapid checkpoint

**Date:** 24 September 2026
**Branch:** `bio-chi-erk-modal-v2-p0q-20260924`
**Status:** ACTIVE P0-Q

## Parent limit preserved

`BIO_CHI/config/ERK_B3_LIMIT_MAP_V01.json`

v1 remains an established P0-Q Limit Map:
- all FRET-visible complex-pair scalar lanes passed;
- complete 8D fixed-stoichiometric-direction round-trip failed;
- ERK `Chi_bio` remained refused under v1;
- no v1 failing direction may be deleted or reclassified.

## v2 frozen question

Freeze:
`BIO_CHI/config/ERK_B3_INVARIANT_MODAL_V2_FREEZE_v0_1.json`

Test every native invariant modal carrier of the same qualified 8D ERK generator:
- every real eigenmode, both signs;
- every complex-pair real 2D invariant subspace, both signs of both frozen basis directions;
- same 1e-3 -> 1e-4 primary convergence rule as v1;
- 1e-5 sensitivity reported only;
- no carrier may be dropped after result.

## Next action

Implement and execute the frozen invariant-carrier nonlinear round-trip.

## Stop condition

No user intervention required unless execution reveals a scientific defect in the frozen carrier definition itself rather than a result.
