"""Figure 2: From Bayesian inference to dynamical system.
Model: free energy F(s; I) = (Pi_e/2)(s - I)^2 + Pi_p * s^2 (1-s)^2, Pi_e = 1.
Gradient flow: tau ds/dt = -dF/ds. Bistable iff Pi_p > Pi_e (at I = 0.5).
Panels: (A) landscape at three drives, (B) fixed points vs drive for three prior precisions with hysteresis,
(C) curvature (local posterior precision) and relaxation time along both branches, (D) same precipitant, two outcomes."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

for f in ['Liberation Sans', 'Arial', 'DejaVu Sans']:
    if any(f == x.name for x in font_manager.fontManager.ttflist):
        plt.rcParams['font.family'] = f
        break
plt.rcParams.update({'font.size': 10, 'axes.linewidth': 0.9, 'axes.labelsize': 11,
                     'xtick.labelsize': 9.5, 'ytick.labelsize': 9.5, 'legend.fontsize': 9.2,
                     'legend.frameon': False, 'mathtext.default': 'it'})
TEAL, DARK, RUST, CYAN, GREY = '#20808D', '#1B474D', '#A84B2F', '#9ED4DC', '#8A8A8A'

def F(s, I, Pp):
    return 0.5 * (s - I) ** 2 + Pp * s ** 2 * (1 - s) ** 2

def dF(s, I, Pp):
    return (s - I) + Pp * 2 * s * (1 - s) * (1 - 2 * s)

def d2F(s, Pp):
    return 1 + Pp * 2 * ((1 - 2 * s) ** 2 - 2 * s * (1 - s))

def I_of_s(s, Pp):  # steady-state curve, parametrised by s
    return s + Pp * 2 * s * (1 - s) * (1 - 2 * s)

def folds(Pp):
    """Two analytically located folds; no spurious roots from grid sign changes."""
    if Pp <= 1:
        return np.array([]), np.array([])
    half_width = np.sqrt((Pp - 1) / (12 * Pp))
    state = np.array([0.5 - half_width, 0.5 + half_width])
    return state, I_of_s(state, Pp)

PP_MAIN = 2.0
fig, axs = plt.subplots(2, 2, figsize=(9.6, 8.3), dpi=300)
fig.subplots_adjust(left=0.08, right=0.985, top=0.95, bottom=0.075, wspace=0.34, hspace=0.42)

def title(ax, letter, text):
    ax.set_title(f'{letter}  {text}', loc='left', fontweight='bold', fontsize=12.5, pad=10)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)

# ---------------------------------------------------------------- A: landscape
ax = axs[0, 0]
s = np.linspace(-0.25, 1.25, 800)
for I, col, lab in [(0.2, TEAL, 'I = 0.2 (low drive)'),
                    (0.5, DARK, 'I = 0.5 (bistable)'),
                    (0.8, RUST, 'I = 0.8 (high drive)')]:
    y = F(s, I, PP_MAIN)
    y = y - y.min()
    ax.plot(s, y, color=col, lw=2.2, label=lab)
    # minima / maximum inside [0,1]
    ss = np.linspace(0, 1, 20001)
    g = dF(ss, I, PP_MAIN)
    roots = ss[np.where(np.diff(np.sign(g)) != 0)[0]]
    for r in roots:
        stable = d2F(r, PP_MAIN) > 0
        ax.plot(r, F(r, I, PP_MAIN) - F(s, I, PP_MAIN).min(), 'o', ms=7,
                mfc=col if stable else 'white', mec=col, mew=1.6, zorder=5)
title(ax, 'A', f'Landscape reshaped by drive  (Π$_p$ = {PP_MAIN:g})')
ax.set_xlabel('symptom-related representation  s')
ax.set_ylabel('free energy  F(s; I)  (shifted)')
ax.set_ylim(-0.02, 0.7)
ax.set_xlim(-0.25, 1.25)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.02), handlelength=1.6, ncol=1)

# ---------------------------------------------------------------- B: bistability and hysteresis
ax = axs[0, 1]
ss = np.linspace(-0.15, 1.15, 4000)
for Pp, col, lab, lw in [(0.5, CYAN, 'Π$_p$ = 0.5 (monostable)', 2.4), (2.0, DARK, 'Π$_p$ = 2', 2.4), (3.0, RUST, 'Π$_p$ = 3', 2.4)]:
    ax.plot(I_of_s(ss, Pp), ss, color=col, lw=lw, label=lab)
sf, If = folds(PP_MAIN)
# onset arrow at upper fold (I high) : from low branch to high branch
I_on = If.max(); s_low = sf[np.argmax(If)]
ss2 = np.linspace(0.5, 1.15, 5000); s_hi = ss2[np.argmin(np.abs(I_of_s(ss2, PP_MAIN) - I_on))]
ax.annotate('', xy=(I_on, s_hi - 0.02), xytext=(I_on, s_low + 0.02),
            arrowprops=dict(arrowstyle='-|>', color=DARK, lw=1.6, mutation_scale=14))
ax.text(I_on + 0.03, (s_low + s_hi) / 2, 'onset', color=DARK, fontsize=10.5, va='center')
I_off = If.min(); s_top = sf[np.argmin(If)]
ss3 = np.linspace(-0.15, 0.5, 5000); s_lo2 = ss3[np.argmin(np.abs(I_of_s(ss3, PP_MAIN) - I_off))]
ax.annotate('', xy=(I_off, s_lo2 + 0.02), xytext=(I_off, s_top - 0.02),
            arrowprops=dict(arrowstyle='-|>', color=DARK, lw=1.6, mutation_scale=14))
ax.text(I_off - 0.03, (s_top + s_lo2) / 2, 'remission', color=DARK, fontsize=10.5, va='center', ha='right')
ax.axvline(0.2, color=GREY, ls=':', lw=1.2)
ax.text(0.22, -0.13, 'precipitant removed (I = 0.2)', color=GREY, fontsize=9, ha='left', va='bottom')
title(ax, 'B', 'Bistability and hysteresis')
ax.set_xlabel('external drive  I')
ax.set_ylabel('fixed points  s*')
ax.set_xlim(-0.15, 1.15); ax.set_ylim(-0.15, 1.2)
ax.legend(loc='upper left', handlelength=1.6)

# ---------------------------------------------------------------- C: curvature and critical slowing
ax = axs[1, 0]
ax2 = ax.twinx()
# asymptomatic branch: s from 0 to lower fold s_low (I increasing to I_on)
s_a = np.linspace(0.0, s_low, 600)
I_a = I_of_s(s_a, PP_MAIN)
k_a = d2F(s_a, PP_MAIN)
# symptomatic branch: s from 1.1 down to upper fold s_top (I decreasing to I_off)
s_b = np.linspace(1.0, s_top, 600)
I_b = I_of_s(s_b, PP_MAIN)
k_b = d2F(s_b, PP_MAIN)
ax.plot(I_a, k_a, color=TEAL, lw=2.2, label='asymptomatic branch (drive rising)')
ax.plot(I_b, k_b, color=RUST, lw=2.2, label='symptomatic branch (drive falling)')
ra = np.full_like(k_a, np.nan); rb = np.full_like(k_b, np.nan)
mask_a = k_a > 1 / 7.5; mask_b = k_b > 1 / 7.5
ra[mask_a] = 1 / k_a[mask_a]; rb[mask_b] = 1 / k_b[mask_b]
ax2.plot(I_a, ra, color=TEAL, lw=1.4, ls='--')
ax2.plot(I_b, rb, color=RUST, lw=1.4, ls='--')
ax.axvline(I_on, color=TEAL, ls=':', lw=1, ymax=0.55); ax.axvline(I_off, color=RUST, ls=':', lw=1, ymax=0.55)
ax.text(I_on + 0.02, 0.15, 'upper fold', color=TEAL, fontsize=9, ha='left')
ax.text(I_off - 0.02, 0.15, 'lower fold', color=RUST, fontsize=9, ha='right')
title(ax, 'C', f'Curvature and critical slowing  (Π$_p$ = {PP_MAIN:g})')
ax.set_xlabel('external drive  I')
ax.set_ylabel("Local Laplace precision F''(s*)")
ax2.set_ylabel("relaxation time  τ / F''(s*)  (dashed)", color=GREY)
ax2.tick_params(axis='y', colors=GREY)
ax2.spines['top'].set_visible(False)
ax.set_xlim(-0.05, 1.05); ax.set_ylim(0, 6.8); ax2.set_ylim(0, 14)
ax.legend(loc='upper right', handlelength=1.6)

# ---------------------------------------------------------------- D: same precipitant, two outcomes
ax = axs[1, 1]
rng = np.random.default_rng(3)
T, dt, tau = 600.0, 0.05, 4.0
t = np.arange(0, T, dt)
I_t = np.interp(t, [0, 120, 240, 300, 480, 600], [0.2, 0.2, 0.85, 0.85, 0.2, 0.2])
def simulate(Pp, sigma=0.012):   # sigma = sqrt(2D) = 0.012 is the noise coefficient of the Euler-Maruyama update
    s = np.empty_like(t); s[0] = 0.05
    for i in range(1, len(t)):
        s[i] = s[i-1] + dt / tau * (-dF(s[i-1], I_t[i-1], Pp)) + sigma * np.sqrt(dt) * rng.standard_normal()
    return s
for Pp, col, lab in [(2.0, DARK, 'Π$_p$ = 2: onset, then remission'), (3.0, RUST, 'Π$_p$ = 3: onset, no remission')]:
    ax.plot(t, simulate(Pp), color=col, lw=1.3, label=lab)
ax.plot(t, I_t, color=GREY, ls=':', lw=1.6, label='drive I (swept 0.2 → 0.85 → 0.2)')
title(ax, 'D', 'Same precipitant, two outcomes')
ax.set_xlabel('time (arbitrary units)')
ax.set_ylabel('symptom-related representation  s(t)')
ax.set_ylim(-0.1, 1.55); ax.set_xlim(0, 600)
ax.legend(loc='upper left', handlelength=1.8)

out = './Figure2'
fig.savefig(out + '.png', dpi=300)
fig.savefig(out + '.tiff', dpi=300, pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig(out + '.pdf')
print('F(s;I)=0.5*(s-I)^2+Pi_p*s^2*(1-s)^2 with Pi_e=1; gradient flow tau*ds/dt=-dF/ds')
print('Panel D: Euler-Maruyama, tau=%g, dt=%g, s0=%g, noise coefficient sqrt(2D)=0.012, seed 3' % (tau, dt, 0.05))
print('Panel B folds Pi_p=2: fold states s =', sf.round(3), '; fold drives I =', If.round(3))
for Pp in (3.0, 4.0):
    print('folds Pp=%g:' % Pp, folds(Pp)[1].round(3))
