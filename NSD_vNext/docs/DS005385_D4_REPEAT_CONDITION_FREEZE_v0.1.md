# NSD ds005385 D4 repeat-condition expansion freeze v0.1

Date: 22 September 2026  
Status: FROZEN BEFORE MULTI-RECORDING D4 EXECUTION  
Program authority: SymC General Operations Manual v0.8.3

## Purpose

The single ds005385 pilot established exact payload/header readability for one recording, but that is not enough to assume the same structural contract across task, pre/post condition, and the five-year repeat session.

This D4 expansion tests one prospectively chosen clean repeat subject, `sub-001`, across all eight recordings:

- ses-1 / ses-2;
- EyesClosed / EyesOpen;
- pre / post cognitive block.

`sub-001` was chosen because it is the first dataset subject, has both sessions, and the source reports zero late-trigger events for both sessions. No EEG-derived feature was inspected to choose it.

## Frozen checks

For every recording:
- exact git-annex SHA-256 and byte size;
- 65 total EDF signals;
- 64 EEG labels in the source order;
- one auxiliary `Status` signal;
- 1000 Hz sampling;
- exact duration implied by the pinned payload;
- EDF internal byte-count consistency.

## Physical-range firewall

The dataset README explicitly states that EDF physical min/max header values may be invalid and should be ignored.

Therefore this D4 task:
- parses with physical-range validation disabled;
- does not convert digital counts into physical units;
- does not compute amplitude, power, PSD, modal damping, local chi, capital Chi, or any cognitive/age effect.

Passing D4 is a payload-structure result only.

## Next gate after pass

If all eight recordings pass, the next scientific design must decide whether a legitimate ds005385 Function/Limit task can be constructed using a scale-invariant representation that does not rely on the invalid physical calibration, or whether ds005385 should be restricted to analyses for which an independently justified calibration can be recovered.

That decision must be frozen before any signal-derived outcome is opened.
