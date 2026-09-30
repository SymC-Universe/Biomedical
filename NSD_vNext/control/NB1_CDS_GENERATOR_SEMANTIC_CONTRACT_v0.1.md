# N-B1 C / D / S Generator and Semantic Contract v0.1

**Status:** packet-level APQ revision candidate; not frozen; no execution authority.

For every fine-rate truth, t0=0 is the first reported observation and dt=1/240 s. Gaussian draws are independent standard normals unless an equation explicitly couples them. Each replicate uses the exact PCG64DXSM seed in NB1_PACKET_SEEDS_v0.2.json. A coarse record is never regenerated: y120[j]=y240[2j].

## Continuous C truth

Given 0<A<1, fn>0, 0<chi<1, and |g|<=1, define omega_n=2*pi*fn, alpha=chi*omega_n, nu=omega_n*sqrt(1-chi^2), G=g*A*alpha, D=A*(2*alpha^2+nu^2),
K=[[-alpha,-1],[nu^2,-alpha]], P=[[A,-G],[-G,D]].
The continuous process is dx=Kx dt+L dW with L L^T=Qc=-(K P+P K^T), initialized x(0)~N(0,P). Observation is y(t_j)=x1(t_j)+sqrt(1-A)*epsilon_j. Exact discretization uses F=exp(K dt), Qd=P-F P F^T. The first observation is emitted from the stationary initial state before the first transition.

A truth is generator-defined C iff these parameter-domain conditions hold and independently checked P,Qc,Qd are positive semidefinite within frozen numerical tolerance. C membership never depends on fit, likelihood, profile, BIC, or estimated chi.

For sampled covariance coordinates define Lc=alpha/fs, rho=exp(-Lc), theta=nu/fs, xi=cos(theta), H_C=A*Lc*sin(theta)/theta. C membership implies -H_C<=H<=H_C with H=g*H_C.

## D and S predicates

For fixed A,rho,xi,H define:
q2=rho^2*(1-A)
q1=rho*((1+rho^2)*H + xi*(A*(1+3*rho^2)-2*(1+rho^2)))
q0=1+rho^4+4*rho^2*xi^2-2*A*rho^4-4*A*rho^2*xi^2-4*H*rho^2*xi.
Let p(x)=4*q2*x^2+2*q1*x+q0-2*q2 on x in [-1,1], and mS=min p(x) over endpoints plus the quadratic vertex when it lies in the interval. S means mS>0 before numerical tolerance. mS=0 defines S_minus and S_plus.

Let H_D=A*sinh(Lc). D means -H_D<=H<=H_D. C is the narrower continuous-embeddable interval -H_C<=H<=H_C. The designed semantic regions are C subset D subset S for this frozen coordinate family.

For NB1B01-L01/L02 use A=.77, fn=11.5 Hz, chi=.34 and H_DNC_pos=H_C+0.5*(H_D-H_C), H_DNC_neg=-H_DNC_pos. For L03/L04 use H_SND_pos=0.5*(H_D+S_plus), H_SND_neg=0.5*(-H_D+S_minus).

D/S rows are generated as the exact ARMA(2,2) spectral factor of the palindromic polynomial. Innovation variance and MA coefficients use the frozen inside-unit-circle root-selection rule in source blob df27fb931dcc17e7dc3fc1e62eb8a8a028601e0c. A five-second burn is discarded; innovations are iid Gaussian; no fitted result enters generation.

## Observation transform

F09 generates one C path and returns additional observations 0.7*y and 1.4*y. Positive scalar gain is a preserving transform for poles and the local damping-ratio coordinate.

All semantic membership labels are fixed from these generator equations before fitting.
