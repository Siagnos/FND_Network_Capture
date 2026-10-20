# Model specification and reproducibility

## Underlying model

The effective potential is `F(s,I,p) = 0.5*(s-I)**2 + p*s**2*(1-s)**2`. Its first derivative is `(s-I)+2*p*s*(1-s)*(1-2*s)`; its second derivative is `1+2*p*(1-6*s+6*s**2)`. The quartic term is stipulated. The recurrent logistic model is `tau*ds/dt=-s+sigma(G*s+I)` and has two fold points only if `k*G>4` with `I` inside the fold interval.

The coupled states are `tau_s*ds/dt=-s+sigma(g*s+c*b+w*d+I)`, `tau_b*db/dt=-b+s`, `tau_d*dd/dt=-d+sigma(h*d+u*s+T)`. The third variable is an aggregate hypothetical defensive coordinate, not a measurement of PAG.

## Figure-specific caution

- Figure 1: panel B uses k = 1, θ = 0 with G = 2.5 and G = 8; the low-gain curve is translated by −2.75 along the drive axis for display only, so overlaid drive values are not comparable. The critical-slowing panel uses a separate Ornstein–Uhlenbeck-type trajectory with an externally imposed state switch.
- Figure 2: fold points use an analytic solver covering tangencies; Figure 2D defines stochastic diffusion amplitude at the level of the state equation and uses tau=4 drift.
- Figure 3: slowly increasing g is an assumed effective adaptation, not empirical striatal plasticity.
- Figure 4: a transient input pulse returns to `T_base=0.10`, not zero; a joint change in h and T is plotted while g adapts. These trajectories do not isolate a causal manipulation. Zero-threat and coupling controls are run by `src/validate_defensive_reset.py`; single-parameter and paired changes are tested in `src/validate_model.py` (the condition `original_both` denotes the joint h and T change plotted in Figure 4D).
- Figure 5: fixed seeds 11, 23 and 5 are specified before outcomes are calculated. Only an individual synthetic example is displayed for each parameter schedule. Labels are mathematical tilt/flatten rather than treatment brands.
- Figure 6: normalized Itô equation `ds = -Fprime(s,I,p)dt + sqrt(2D)dW`, tau=1, Euler–Maruyama `dt=0.05`, final time 300, 1000 paths per parameter schedule, seed 20261019, `D in {0.004,0.006,0.008}`. Outcome is `s<0.5` at endpoint and Wilson intervals show Monte Carlo uncertainty only. First and second sequential schedules differ in duration of sustained tilt; they are not a controlled order effect.

## Reference values

A correct reproduction yields the following values (see also `results/`).

- Figure 1 high-gain fold states: 0.14644661, 0.85355339; drives -2.9343 and -5.0657.
- Figure 2 fold drives: p=2 -> 0.3639/0.6361, p=3 -> 0.1857/0.8143.
- Figure 3 two stable equilibria and one saddle for chosen parameters.
- Figure 6 at D=0.006: control 0/1000, tilt 10/1000, flatten 499/1000, concurrent 992/1000, tilt-before-flatten 998/1000, flatten-before-tilt 541/1000 (calculated under unmatched schedules).

To cite a specific version of the code, use the corresponding Git release tag. The models are synthetic and no clinical validity is claimed.
