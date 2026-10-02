# Bio Chi C-Interior Function Map Qualified Plan Freeze v1.1

**Freeze status:** QUALIFIED_FROZEN  
**Date:** 27 September 2026  
**APQ level:** APQ-2 SUBSTANTIAL, targeted runtime recheck complete  
**Qualified Plan Packet:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_PACKET_v0.3.md\`  
**Qualified Plan commit:** \`7ace5de0f6846f53b01f7cb46f09fcb0a55e9426\`  
**Runtime APQ recheck:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_RUNTIME_APQ_RECHECK_v0.1.md\`  
**Runtime Plan Delta:** \`NSD_vNext/docs/BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_DELTA_v0.2.md\`  
**Supersedes for future execution:** freeze v1.0 / Plan Packet v0.2

## Frozen execution

The 16-cell C-interior qualification envelope, three seeds, 60 s duration, 256 Hz fine sampling, exact factor-2 same-path decimation, C1Q estimator, generic covariance-recurrence diagnostic, output claim ceiling, refusal logic, and no-threshold rule are unchanged from v0.2.

The only scientific-plan execution change is removal of **new A0/A1/A2 refitting** from this Function Map. Earlier A0/A1/A2 comparative evidence remains part of the qualification history and is not overwritten.

## Frozen preflight

Cells 0, 5, 10, and 15 at seed 104729 must verify:

- exact truth construction and covariance validity;
- alias-safe factor-2 sampling;
- C1Q finite execution and recorded optimizer diagnostics;
- generic recurrence diagnostic execution/refusal;
- row/schema serialization;
- environment and repeatability metadata.

Poor recovery is preserved and does not retune the map.

## Claim ceiling

This remains P0-D correct-specification estimator Function Mapping. It does not validate C biologically, estimate biological prevalence, promote C1Q, define an admission threshold, or license real EEG local chi.

## Next gate

Run the revised mechanical preflight. If mechanically valid, execute the full 16-cell x 3-seed map without scientific retuning.
