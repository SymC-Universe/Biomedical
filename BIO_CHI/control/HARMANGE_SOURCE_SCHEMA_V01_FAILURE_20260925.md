# Harmange bridge source-schema failure checkpoint

**Date:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Workflow run:** 36100750619  
**Status:** MECHANICAL FAILURE / SCIENTIFIC GATE NOT REACHED

## Failure

The first source-schema audit stopped before any source object was analyzed because the Python result dictionary used JSON literals `false` instead of Python `False`.

Observed exception:

`NameError: name 'false' is not defined`

## Root-cause classification

- implementation/transport defect: **yes**
- source-access failure: **no evidence**
- source-schema failure: **not tested**
- scientific failure: **no**
- molecular values opened: **no**
- target outcomes computed: **no**

The failure is preserved as evidence and does not alter the frozen Harmange source contract.

## Repair

Change only the two invalid Python Boolean literals from `false` to `False`, then rerun the same frozen audit with no scientific or source-selection changes.
