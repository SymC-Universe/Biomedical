# E. coli sensory P0-Q transport failure checkpoint

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-sensory-p0q-20260925`  
**Status:** SOURCE TRANSPORT BLOCKED, SCIENTIFIC TEST NOT OPENED

Two execution attempts were preserved.

1. Run `36212606329` failed before source parsing because Dryad returned HTTP 403 for the first frozen file.
2. After a mechanical session/header repair that did not alter the scientific freeze, run `36212678770` passed the HTTP gate but the first returned payload failed MATLAB parsing with `ValueError: Unknown mat file type, version 105, 110`.

The second run therefore narrowed the root cause from access denial to an invalid or substituted payload on the automated file-stream route. No cell, FOV, distribution, representation, scalar, modal, or Bio Chi result was inspected. The frozen scientific test remains intact but unexecuted.

**Disposition:** `SOURCE_TRANSPORT_BLOCKED`.

This is not evidence for or against Bio Chi, `Chi_bio`, or `chi_bio`. The failure is retained as provenance and may be reopened only with a source route that returns bytes matching the frozen Dryad file identities.
