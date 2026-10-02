# NSD ds005385 D4 repeat-condition post-result audit v0.1

Date: 22 September 2026  
Status: COMPLETE D4 PAYLOAD-STRUCTURE RESULT FOR ONE CLEAN REPEAT SUBJECT  
Program authority: SymC General Operations Manual v0.8.3  
Workflow: `NSD ds005385 D4 Repeat-Condition Expansion`  
Run: `35768527802`  
Artifact: `ds005385-d4-sub001-repeat-condition-v0-1`  
Artifact ID: `10713391571`  
Artifact ZIP SHA-256: `6379200537f8c9409a53ebad60295f646add73d607f6dffcefd9eafcb9dad9d9`

## Frozen scope

The prospectively selected subject was `sub-001`, chosen before this multi-recording result because:
- it is the first dataset subject;
- both sessions are present;
- source late-trigger counts are 0 in both sessions.

Eight raw EDF recordings were tested:
- ses-1 and ses-2;
- EyesClosed and EyesOpen;
- pre and post cognitive block.

No EEG-derived scientific feature was opened.

## Result

**8/8 recordings passed every frozen D4 structural check.**

For every recording:
- exact source SHA-256 matched;
- exact byte count matched;
- 65 total EDF signals were present;
- first 64 EEG labels matched the frozen source ordering;
- the 65th auxiliary signal was `Status`;
- sampling was exactly 1000 Hz;
- source-specific duration matched;
- EDF internal expected-byte count matched the actual payload.

Durations varied across the eight raw recordings from 181 to 193 seconds, so the source's nominal three-minute language is approximate at the payload level. The exact duration is retained per recording.

## Physical calibration firewall

The dataset source explicitly warns that EDF physical min/max header values may be invalid.

This D4 execution therefore:
- parsed headers with physical-range validation disabled;
- did **not** use header physical min/max for scaling;
- did **not** convert digital counts into physical units;
- did **not** compute PSD, absolute power, amplitude, modal damping, local chi, capital Chi, or any age/state effect.

The successful result therefore means:

`DS005385_D4_SUB001_REPEAT_CONDITION_PAYLOAD_STRUCTURE = VERIFIED`

It does **not** mean:

`DS005385_PHYSICAL_AMPLITUDE_CALIBRATION = VERIFIED`.

## Scientific consequence

The dataset is structurally strong for adult Function/Limit work across:
- eyes-open versus eyes-closed;
- pre versus post cognitive block;
- five-year repeat session.

But any next analysis must first decide what can be inferred without trusting the source-declared unreliable physical calibration.

Scale-sensitive quantities such as absolute voltage or absolute power remain blocked unless an independent calibration route is recovered.

Scale-invariant or internally standardized representations are scientifically plausible candidates, but choosing them is a task-design decision and must be frozen prospectively before a signal-derived result is opened.

## Next gate

Create and approve/freeze a ds005385 Function/Limit task that explicitly specifies:
1. allowed scale-invariant representation;
2. prohibited scale-sensitive claims;
3. quality handling for source late-trigger records;
4. condition contrasts;
5. subject/session hierarchy;
6. native/simple comparators;
7. effect-size/uncertainty metrics;
8. whether the task is descriptive P0-D or qualification P0-Q.

No real-EEG modal damping or local chi is licensed by this D4 result.
