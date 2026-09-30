# N-B1 Exact Packet v0.3 Independent Review Handoff

**Status:** prospective exact-packet authority; NOT FROZEN; no execution or result access
**Packet:** \`NB1-B01-EXACT-PREQ-V03\`
**Design baseline:** \`NSD-V02-B01-PREQ\`

This handoff contains the operative scientific specification needed for independent packet review. Historical exploratory implementation is not normative when it conflicts with this handoff.

## 1. Case identities and recording contract

There are 18 truth classes, 16 fixed parent replicates, and two reported rates.

Fine record: 240 Hz for 96 s, exactly 23,040 samples, indexed j=0..23039, t_j=j/240 s, covering [0,96). The j=0 observation is emitted from the initial state before the first transition.

Coarse record: 120 Hz, exactly 11,520 samples, y120[j]=y240[2j], j=0..11519. No regeneration, interpolation, or filtering is permitted.

Case ID is <truth_id>-<R00..R15>-S<rate>; expected row count is 18*16*2=576. The independent replicate unit is the generated fine path / parent seed.

### Function truths

| ID | Generator | Parameters / role |
|---|---|---|
| NB1B01-F01 | CONTINUOUS_C | A=.80, natural fn=8 Hz, chi=.24, g=.05; ordinary retention |
| NB1B01-F02 | CONTINUOUS_C | A=.62, fn=13, chi=.42, g=-.50; nonzero-g retention |
| NB1B01-F03 | CONTINUOUS_C | A=.33, fn=18.5, chi=.57, g=.60 |
| NB1B01-F04 | CONTINUOUS_C | A=.76, fn=10, chi=.88, g=.20 |
| NB1B01-F05 | CONTINUOUS_C | A=.70, fn=31, chi=.30, g=-.75 |
| NB1B01-F06 | CONTINUOUS_C | A=.73, fn=6.5, chi=.16, g=.30 |
| NB1B01-F07 | CONTINUOUS_C | A=.58, fn=15.5, chi=.36, g=.72 |
| NB1B01-F08 | CONTINUOUS_C | A=.67, fn=22, chi=.48, g=-.68 |
| NB1B01-F09 | CONTINUOUS_C_GAIN_CONTROL | A=.75, fn=11, chi=.32, g=.25; deterministic observation gains .7 and 1.4 |

### Limit truths

NB1B01-L01/L02 are D-not-C positive/negative cases from base A=.77, natural fn=11.5 Hz, chi=.34.
NB1B01-L03/L04 are S-not-D positive/negative cases from the same base.
NB1B01-L05 is colored-memory truth with phi=.70, base fn=10 Hz, chi=.30.
NB1B01-L06 is genuine two-mode truth with modes (10 Hz,.25) and (20 Hz,.35).
NB1B01-L07 is piecewise C reorganization: 0<=t<48 s uses A=.72, fn=9, chi=.28, g=.20; 48<=t<96 s uses A=.72, fn=17, chi=.52, g=-.35; no latent reset.
NB1B01-L08 is stationary unit-variance AR(1), phi=.86.
NB1B01-L09 is a two-mode reference mixture using the L06 modes and normalized 1:.35 mixing.

## 2. Continuous-C and D/S semantic contracts

For C truth:
omega_n=2*pi*fn; alpha=chi*omega_n; nu=omega_n*sqrt(1-chi^2);
G=g*A*alpha; D=A*(2*alpha^2+nu^2);
K=[[-alpha,-1],[nu^2,-alpha]];
P=[[A,-G],[-G,D]].
Continuous process is dx=Kx dt+L dW with L L^T=Qc=-(K P+P K^T), and stationary x(0)~N(0,P). Observation is y(t_j)=x1(t_j)+sqrt(1-A)*epsilon_j. At 240 Hz, F=exp(K/240), Qd=P-F P F^T. Exact C membership is generator-defined and never inferred from fit/BIC/profile.

Numerical generator validation symmetrizes each required covariance/noise matrix M as (M+M^T)/2 and requires minimum eigenvalue >= -1e-9 for P, Qc, and Qd. This is numerical-only, not a family boundary. Exact C-domain predicates are 0<A<1, 0<chi<1, |g|<=1 and the prospectively declared generator-frequency domain. A violation is a frozen-contract failure before scientific evaluation.

For sampled D/S predicates let Lc=alpha/fs, rho=exp(-Lc), xi=cos(nu/fs), H_C=A*Lc*sin(nu/fs)/(nu/fs), H_D=A*sinh(Lc). Define
q2=rho^2*(1-A),
q1=rho*((1+rho^2)*H + xi*(A*(1+3*rho^2)-2*(1+rho^2))),
q0=1+rho^4+4*rho^2*xi^2-2*A*rho^4-4*A*rho^2*xi^2-4*H*rho^2*xi,
and p(x)=4*q2*x^2+2*q1*x+q0-2*q2 on [-1,1]. S requires the minimum over endpoints plus the quadratic vertex when in-domain to be positive. D is -H_D<=H<=H_D, and C is the narrower -H_C<=H<=H_C.

L01/L02 use H=+/-[H_C+.5*(H_D-H_C)]. L03/L04 use the midpoint between the D boundary and the corresponding S positivity boundary. D/S rows use the exact ARMA(2,2) spectral factor, iid Gaussian innovations, and an exact five-second burn.

## 3. Other Limit generators

L05 uses a 4D augmented stationary Gaussian state z=[s1,s2,c1,c2]. The signal oscillator has the exact damped-rotation transition for 10 Hz, chi=.30; c_(t+1)=.70*c_t+sqrt(1-.70^2)*epsilon_t; s_(t+1)=T*s_t+sqrt(1-rho^2)*c_t. Initial z is drawn from the unique stationary covariance. Observation is normalized s1, with no measurement noise.

L06 uses two independent unit-variance C latent oscillators, g=0, no individual measurement noise, at (10 Hz,.25) and (20 Hz,.35). Observation is y=sqrt(.4)*x1_mode1+sqrt(.4)*x1_mode2+sqrt(.2)*epsilon.

L07 carries the latent state continuously through the 48-s parameter change; process and observation RNG streams continue without reset.

L08: y0~N(0,1), y_t=.86*y_(t-1)+sqrt(1-.86^2)*epsilon_t.

L09 forms m=(x1_mode1+.35*x1_mode2)/sqrt(1+.35^2), then y=sqrt(.8)*m+sqrt(.2)*epsilon.

## 4. RNG identity

Parent generator is NumPy Generator(PCG64DXSM(seed)). For replicate i=0..15, hash exact UTF-8 bytes 'NSD-NB1-v0.2-B01|replicate|i' with SHA-256, interpret digest bytes 0..7 as unsigned big-endian, reduce modulo (2^63-1), retry deterministically only for zero/collision, and serialize as decimal strings.

Seeds R00..R15:
4012295144428264894, 734722767732809149, 4357778436359021462, 5424248785973095680, 5889269372358671117, 5492451934434697924, 633781396054923176, 2245695508485767439, 437839555414937764, 2354668980245810183, 1348743885252759305, 4146112300962661065, 6035756257014055845, 3924039236262827060, 2582629269499962595, 488137367194850018.

Child seed bytes are exact UTF-8 '<decimal_parent_seed>|<truth_id>|<child_label>', with the same digest rule. Child labels: L05 'augmented'; L06 'mode1','mode2','obs'; L07 'process','obs'; L09 'mode1','mode2','obs'.

C draw order: draw two standard normals for stationary x0; for each fine sample j draw one observation normal, emit y_j, then draw two process normals for the next transition. D/S ARMA draws the complete innovation vector in increasing index before recursion. L08 draws y0 then one innovation per subsequent point. Multistream limits use only their named child streams. F09 gains are deterministic transforms and consume no extra draws. Historical default_rng generators are explicitly non-normative.

## 5. Channel applicability and classification

For every truth, P,S,T,F,O,M,N,I are required. R is additionally required only for F09 and L09. U is NOT_APPLICABLE to admission; paired-rate sensitivity is descriptive.

P = frozen provenance/identity. S = same-path sampling plus alias certification. T = stationarity for stationary scalar claim. F = generator-defined C semantics. O = exactly one relevant eligible oscillatory mode. M = one-mode white-innovation closure. R = preserving observation/reference mapping where applicable. N = numerical/search integrity. I = profile numerical uniqueness/interiority only.

Top-level namespaces: DATA_CONTRACT_REFUSAL from P/S; SEMANTIC_REFUSAL from T/F/O/M/R; ESTIMATOR_ROUTE_REFUSAL from N/I. The full channel-state vector is retained. Every applicable refusal namespace is retained. Any required NEED_MORE_INFO is retained alongside other labels. QUALIFICATION_ELIGIBLE iff all required channels PASS. No precedence rule deletes another state. NOT_APPLICABLE is reported and never counted as PASS.

Every assigned row remains in accounting. Summaries are per truth ID x rate with denominator 16 and report eligibility, each refusal namespace, NEED_MORE_INFO, numerical/search events, multi-label combinations, and channel states separately. Two-sided 95% Wilson intervals are descriptive only. No success-only denominator, cross-truth score, or prevalence interpretation is permitted.

## 6. Sampling/alias certificate

The fitted C-lineage coordinate constrained to 1..45 Hz is damped frequency nu/(2*pi), not derived natural frequency. At 120 Hz, 0<theta=nu/fs<=3*pi/4<pi; at 240 Hz, 0<theta<=3*pi/8.

For the frozen nondegenerate C positive-lag covariance law, independent measurement noise contributes only at lag zero and the nonzero latent component preserves sampled conjugate poles z_+/-=rho*exp(+/-i*theta). The minimal second-order positive-lag recurrence therefore identifies rho and principal theta in (0,pi). Then alpha=-fs*log(rho), nu=fs*theta, omega_n=sqrt(alpha^2+nu^2), chi=alpha/omega_n. Natural frequency is derived and is not capped at 45 Hz.

Independent analytic/reference verification of the nondegenerate recurrence and this mapping is mandatory before S=PASS. A demonstrated distinct admissible C lineage with the same sampled law gives REFUSE; unresolved certificate gives NEED_MORE_INFO. No uniqueness claim is made outside the frozen C/preserving-observation class.

## 7. Profile-I contract

I is only resolution-bounded numerical uniqueness/interiority inside the imposed C family, not family membership, structural identifiability, precision, or a confidence threshold.

Input is standardized by sample mean and population SD. Frozen C likelihood uses fmin=1 Hz, fmax=45 Hz, burn-in=128. Raw transforms:
A=1e-5+(1-2e-5)*sigmoid(raw_A);
rho=1e-3+(.999-.001)*sigmoid(raw_rho);
damped_frequency=1+44*sigmoid(raw_fd);
g=tanh(raw_g).
At fixed chi, nuisance coordinates are raw_A, raw_fd, raw_g, all bounded [-8,8]. Alpha is determined by fixed chi and damped frequency; rho=exp(-alpha/fs), with raw_rho derived from rho.

Base grid is 61 equally spaced chi values on [.05,.98]. Fitted chi may be evaluated only to verify reproduction of the selected global fit. True chi is never added to the profile grid and never enters starts, bracketing, refinement, tie decisions, or labels.

At each chi use L-BFGS-B, maxiter=80, ftol=1e-8, maxls=30. Starts: continuation from neighbor; global fit projected to current chi; recurrence/covariance start when SEED_READY; and six fixed physical starts transformed at current chi:
(.25,max(1.2,.75*fn_fit),-.6),
(.25,fn_fit,.6),
(.55,max(1.2,.75*fn_fit),0),
(.55,min(44,1.25*fn_fit),-.6),
(.85,fn_fit,.6),
(.85,min(44,1.25*fn_fit),0).
Deduplicate at max-absolute raw difference <1e-10.

Refine every finite base-grid local-minimum bracket and endpoint-adjacent minimum with bounded scalar chi optimization; every scalar evaluation reoptimizes nuisance coordinates from the same frozen recipe. Scalar xatol=1e-6, maxiter=200. Fitted-profile reproduction tolerance is 1e-5*max(1,abs(NLL)); competing-global tie tolerance is 1e-8*max(1,abs(NLL)). Best candidate on a nuisance bound is NEED_MORE_INFO. Failed/nonregular/edge/tied refinement is NEED_MORE_INFO unless N already records a pure numerical/search refusal.

## 8. Framework and claim ceiling

FRAMEWORK_NOT_OPERATIONAL if a required channel needs post-result rule invention/retuning, semantic and estimator refusal namespaces cannot remain separate, any F01/F02 control-rate cell has zero eligible rows among its 16 fixed replicates, or a post-result scientific threshold is required for ordinary eligibility.

Historical v0.1 outputs remain P0-D exposed development and are not design inputs. No real-EEG local chi, biological prevalence, universal threshold, whole-system scalar, or production estimator is licensed. C1Q-RS remains qualification-only. Final code/dependency/environment identities and implementation tests are bound after packet APQ/freeze and before execution. Scientific result access is forbidden until then.
