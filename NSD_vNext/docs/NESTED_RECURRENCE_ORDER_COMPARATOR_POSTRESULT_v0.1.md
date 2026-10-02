# NSD Nested Recurrence-Order Comparator Postresult v0.1

Status: QUALIFICATION-ONLY KNOWN-TRUTH RESULT  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Primary investigation: Bio Chi  
Branch: `nsd-rebuild-gom-v0.8.0`

## Provenance

Workflow: `NSD Nested Recurrence Order Comparator`  
Run: `36363576117`  
Conclusion: SUCCESS  
Source head: `7f677bf7f78309ac1c5cda8c1f0cef2c26c76778`

Artifact: `nsd-nested-recurrence-order`  
Artifact ID: `10946248867`  
Digest: `sha256:5ab65a9e9b6ab18d3e9fadd0ad937f17d8a6dd871302355195bc9988d397b8d3`

Output status: `PREDECISION_CALIBRATION_ONLY`  
`licenses_real_eeg_local_chi=false`  
`defines_order_threshold=false`  
`changes_production_estimator=false`

## Result

The nested recurrence-order comparator did not produce the intended finite-sample structural-order separation.

Against pooled C-interior controls, threshold-free rank AUC for colored-process truth was:

- fine order-2 to order-3 absolute improvement: 0.300;
- fine relative order-2 to order-3 improvement: 0.405;
- fine order-3 to order-4 absolute improvement: 0.638;
- fine relative order-3 to order-4 improvement: 0.642;
- coarse order-2 to order-3 absolute improvement: 0.323;
- coarse relative order-2 to order-3 improvement: 0.332;
- coarse order-3 to order-4 absolute improvement: 0.601;
- coarse relative order-3 to order-4 improvement: 0.575.

The expected signature was not recovered. Median fine relative order-2 to order-3 improvement was approximately 0.112 for colored truth, while the three valid C-interior controls were approximately 0.151, 0.126, and 0.183. Genuine two-mode truth also did not show the expected order-3 to order-4 gain; its median fine relative order-3 to order-4 improvement was approximately -0.120.

Higher-order recurrence fits were substantially more ill-conditioned than order two. At fine rate, median order-3 condition numbers were approximately 287 to 428 across C interiors, approximately 348 for colored truth, and approximately 88 for genuine two-mode truth. Order-4 condition numbers were commonly several hundred. This conditioning burden is part of the finite-sample failure mechanism and prevents a simple order-improvement rule from being interpreted as a clean structural detector.

## Scientific consequence

The recurrence-order route is retained as descriptive structural evidence but is not promoted into an N-B1 refusal gate.

The result closes the current sequence of increasingly elaborate covariance-order diagnostics as a primary near-term route. Exact order theory remains valid, but finite-sample covariance recurrence order is not sufficiently discriminating in the present qualification regime to justify further threshold tuning.

Under the GOM Function Map / Limit Map balance rule, this result is recorded as a Limit Map finding rather than used to justify another immediate failure-focused comparator. The next primary P0 lane returns to representative Function Map coverage of the intended C interior. A likelihood-based higher-order/memory comparator remains an available later Limit Map tool if a future claim specifically requires resolving that ambiguity.

## Threshold impact

No threshold is frozen, revised, or retired. The finite-data structural-order threshold remains unfrozen.

## Interpretation ceiling

This result does not:

- license real-EEG local chi;
- promote C1Q or D1Q;
- change production A0/A1/A2;
- prove that colored or multimode dynamics are rare or common in biology;
- erase the exact structural-order theorem;
- remove colored-process or multimode cases from the Limit Map;
- alter N-B2 or N-B3.
