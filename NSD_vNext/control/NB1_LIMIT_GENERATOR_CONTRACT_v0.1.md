# N-B1 Non-C Limit Generator Contract v0.1

**Status:** packet-level APQ revision candidate; not frozen; no execution authority. All definitions are prospective and outcome-blind.

All limits are first generated at 240 Hz for 96 s under the exact replicate seed, then the same realized path is decimated by two for 120 Hz.

## L05 colored-memory truth

Let T be the exact 2D damped-rotation transition for fn=10 Hz and chi=.30 at 240 Hz, with decay factor rho. Let phi=.70 and beta=sqrt(1-rho^2). Define the 4D augmented state z=[s1,s2,c1,c2]^T:
s_(t+1)=T*s_t + beta*c_t,
c_(t+1)=phi*c_t + sqrt(1-phi^2)*epsilon_t.
The joint initial state is drawn from the unique stationary zero-mean Gaussian covariance solving the discrete Lyapunov equation for this augmented linear system. Observation is y_t=s1_t/sqrt(Var_stationary(s1)); there is no additional measurement noise. This truth is time-stationary but violates the white-innovation/memory-closure requirement of the one-mode C generator.

## L06 genuine two-mode truth

Create two independent unit-variance latent continuous-time oscillators using the C latent state equations with g=0 and no individual measurement noise:
mode 1: fn=10 Hz, chi=.25;
mode 2: fn=20 Hz, chi=.35.
Each begins in its stationary Gaussian state and uses independent process innovations derived deterministically from the replicate seed through domain-separated child streams L06|mode1, L06|mode2, and L06|obs.
Observation is
y=sqrt(.4)*x1_mode1 + sqrt(.4)*x1_mode2 + sqrt(.2)*epsilon,
so the intended stationary observation variance is one. This truth contains two distinct oscillatory pole pairs and is not a one-mode C truth.

## L07 piecewise C reorganization

Segment 1 occupies 0<=t<48 s with A=.72, fn=9 Hz, chi=.28, g=.20.
Segment 2 occupies 48<=t<96 s with A=.72, fn=17 Hz, chi=.52, g=-.35.
Segment 1 begins from its own stationary C distribution. At exactly t=48 s the latent state is carried forward without reset, while K/F/Qd change to the segment-2 values. Observation variance remains 1-A=.28. One domain-separated RNG stream supplies process innovations and one supplies observation noise across the full record. The full record is explicitly nonstationary; no segmentwise result may be substituted for the full-row T decision.

## L08 nonoscillatory AR(1)

y_0 is drawn from N(0,1). For t>=1,
y_t=.86*y_(t-1)+sqrt(1-.86^2)*epsilon_t,
with iid standard-normal epsilon. This is stationary, unit variance, and contains no oscillatory pole pair.

## L09 reference-mixture two-mode truth

Create the same independent unit-variance latent modes as L06. Let
m=(x1_mode1 + .35*x1_mode2)/sqrt(1+.35^2).
Observation is y=sqrt(.8)*m+sqrt(.2)*epsilon, using domain-separated child streams L09|mode1, L09|mode2, L09|obs. The reference transform is therefore exactly the declared 1:.35 modal mixture. It is a non-preserving observation for one-scalar local attribution.

## Domain-separated child streams

For any child label, derive its seed from SHA-256 of the exact UTF-8 bytes <decimal_parent_seed>|<truth_id>|<child_label>, first eight digest bytes interpreted unsigned big-endian and reduced modulo 2^63-1, with the same deterministic nonzero/collision retry rule as the parent seed contract. Child seeds are generator identity and must be serialized as decimal strings.

These definitions supersede any underspecified Draft-B generator labels for packet-level review. No limit count is interpreted as biological prevalence.
