# P0-D19 Closed-Loop Recovery Prediction Result

Date recorded: 2026-09-13
Execution date: 2026-09-11
Status: **P0-D exploratory; synthetic/known-construction evidence; not P0-Q or P1. No recovery threshold, chi target, or clinical claim frozen.**
Purpose: `FUNCTION_MAPPING`

## Source of record
- Run `34623913124`, job `103344273462`
- Source commit `f9ffcfd5a7ea20885230c19cea6a6320adffa9d7`
- Workflow conclusion: success; tests: `4 passed`
- Artifact `10273199733`
- Artifact ZIP SHA-256 `fce4fa3f02cd77eb364124d28144c2ee84428f0977a45d5c2efca47289e8ffcc`

## Question
With local subsystem generators fixed, does interaction architecture alone alter asymptotic recovery and finite-time perturbation amplification?

For each coupled generator, P0-D19 recorded spectral abscissa `alpha=max Re(lambda)`, local asymptotic return scale `tau=-1/alpha` when `alpha<0`, worst-case finite-time gain in the declared dimensionless state metric, and its peak time. These are recovery/resilience diagnostics, not chi values.

## Results

### One-way coupling `ONE_WAY_0_TO_1`
Across `g=0,4,8,12,14,18,22`, spectral abscissa remained about `-10.3672557568` and `tau` about `0.0964575413`. Worst-case gain increased from `1.0000` to `1.0467549735`.

Interpretation: in this block-triangular construction, one-way influence altered finite-time response modestly while preserving the autonomous asymptotic poles.

### Bidirectional closed loop `BIDIRECTIONAL_CLOSED_LOOP`
- `g=0`: alpha `-10.3672557568`, tau `0.0964575413`, gain `1.0000000000`
- `g=4`: alpha `-10.8323310527`, tau `0.0923162332`, gain `1.0004252297`
- `g=8`: alpha `-12.6359491198`, tau `0.0791392867`, gain `1.0038156139`
- `g=12`: alpha `-17.7036142711`, tau `0.0564856410`, gain `1.0126681235`
- `g=14`: alpha `-13.3555326318`, tau `0.0748753365`, gain `1.0205669058`
- `g=18`: alpha `-5.7509468924`, tau `0.1738844087`, gain `1.0519180866`
- `g=22`: alpha `-1.8186178478`, tau `0.5498681327`, gain `1.1312829849`

All scanned points remained asymptotically stable. Recovery was non-monotonic: reciprocal feedback first strengthened asymptotic return through `g=12`, then reversed direction and approached the stability boundary at stronger coupling while transient amplification increased.

## Supported P0-D interpretation
1. Local subsystem identity does not determine embedded recovery by itself.
2. One-way contribution and closed feedback are dynamically distinct.
3. More coupling is not monotonically more or less stabilizing.
4. Asymptotic return and finite-time resilience are separate.
5. Recovery erosion can appear before actual local instability in this synthetic surface.

## Nonclaims
No empirical neural result; no biological meaning assigned to `g`; no universal recovery threshold; no claim that chi alone predicts recovery; no claim that `chi=1` is a recovery-failure boundary; no evidence for the separately timestamped `chi~1.2-1.3` hypothesis; no nonlinear basin or clinical claim.

## Architectural consequence
`local/modal dynamics -> licensed local chi -> directed coupling/feedback -> emergent closed-loop dynamics -> recovery/resilience`

Conglomeration remains an interaction architecture, not an average over local chi values.

## Next safe P0-D work
Test recovery across feedback transformation geometry; test P0-D18 hierarchy-preserving recovery prediction; add a deliberate model-break/refusal case; and create the independent experimental-opportunity sketch required by General Protocol v0.7.4 before targeted prior-experiment searching for this recovery question.