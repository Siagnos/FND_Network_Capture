"""Figure 5: Noise, escape and the two directions of a barrier.
(A) F(s;I) at I=0.5 for Pi_p=3 (solid) and Pi_p=1.3 (dashed): lowering prior precision lowers both barriers.
(B) Pi_p=3, I=0.5 (solid) versus I=0.42 (dashed): evidence tilts the landscape; symptomatic barrier falls,
    asymptomatic barrier rises.
(C) Euler-Maruyama simulations of tau ds/dt = -dF/ds + sqrt(2D) xi(t), D=0.006, starting in the symptomatic well:
    tilt only (I -> 0.42), flatten only (Pi_p -> 1.3 temporarily),
    and concurrent flatten-plus-tilt; no clinical treatment assignment is assumed."""
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
                     'xtick.labelsize': 9.5, 'ytick.labelsize': 9.5, 'legend.fontsize': 9.0,
                     'legend.frameon': False, 'mathtext.default': 'it'})
TEAL, DARK, RUST, CYAN, GREY, INK = '#20808D', '#1B474D', '#A84B2F', '#9ED4DC', '#8A8A8A', '#222222'
GOLD = '#B8860B'

PE = 1.0
PP0, PP1 = 3.0, 1.3      # baseline and temporarily flattened quartic weight
I0, I1 = 0.5, 0.42       # baseline and tilted drive
D = 0.006


def F(s, I, Pp):
    return PE / 2 * (s - I) ** 2 + Pp * s ** 2 * (1 - s) ** 2


def dF(s, I, Pp):
    return PE * (s - I) + 2 * Pp * s * (1 - s) * (1 - 2 * s)


fig = plt.figure(figsize=(9.6, 8.8), dpi=300)
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.35], hspace=0.42, wspace=0.30,
                      left=0.075, right=0.985, top=0.95, bottom=0.07)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])
gsC = gs[1, :].subgridspec(3, 1, hspace=0.12)
axC = [fig.add_subplot(gsC[i, 0]) for i in range(3)]


def title(ax, letter, text):
    ax.set_title(f'{letter}  {text}', loc='left', fontweight='bold', fontsize=12.5, pad=10)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)


s = np.linspace(-0.15, 1.15, 800)


def annotate_barrier(ax, I, Pp, col, dy=0.0, side='both', lw=1.0):
    """Mark barrier heights from each well with vertical bars."""
    ss = np.linspace(-0.3, 1.3, 20001)
    f = F(ss, I, Pp)
    d = np.diff(np.sign(np.diff(f)))
    mins = ss[1:-1][d > 0]
    maxs = ss[1:-1][d < 0]
    if len(maxs) == 0:
        return
    top = F(maxs[0], I, Pp)
    for k, m in enumerate(mins):
        if side == 'low' and k == 1:
            continue
        if side == 'high' and k == 0:
            continue
        x = m + (0.06 if k == 0 else -0.06)
        ax.plot([x, x], [F(m, I, Pp), top], color=col, lw=lw, ls=':')
        ax.plot([x - 0.015, x + 0.015], [top, top], color=col, lw=lw)
        ax.plot([x - 0.015, x + 0.015], [F(m, I, Pp), F(m, I, Pp)], color=col, lw=lw)


# ---------------------------------------------------------------- A
title(axA, 'A', 'Lower quartic weight lowers both barriers')
axA.plot(s, F(s, I0, PP0), color=DARK, lw=2.0, label=r'$\Pi_p$ = 3 (before)')
axA.plot(s, F(s, I0, PP1), color=TEAL, lw=2.0, ls='--', label=r'$\Pi_p$ = 1.3 (flatten)')
annotate_barrier(axA, I0, PP0, DARK)
annotate_barrier(axA, I0, PP1, TEAL)
axA.set_xlabel('symptom representation  s')
axA.set_ylabel('free energy  F(s; I)')
axA.set_xlim(-0.15, 1.15); axA.set_ylim(0, 0.32)
axA.legend(loc='upper center')
axA.text(0.09, 0.005, 'asymptomatic', ha='center', va='bottom', fontsize=8.5, color=GREY)
axA.text(0.91, 0.005, 'symptomatic', ha='center', va='bottom', fontsize=8.5, color=GREY)
axA.text(0.5, 0.225, 'I = 0.5', ha='center', va='top', fontsize=9, color=INK)

# ---------------------------------------------------------------- B
title(axB, 'B', 'Evidence tilts the landscape')
axB.plot(s, F(s, I0, PP0), color=DARK, lw=2.0, label='I = 0.50 (before)')
axB.plot(s, F(s, I1, PP0), color=RUST, lw=2.0, ls='--', label='I = 0.42 (tilt)')
annotate_barrier(axB, I0, PP0, DARK)
annotate_barrier(axB, I1, PP0, RUST)
axB.set_xlabel('symptom representation  s')
axB.set_ylabel('free energy  F(s; I)')
axB.set_xlim(-0.15, 1.15); axB.set_ylim(0, 0.32)
axB.legend(loc='upper center')
axB.text(0.5, 0.225, r'$\Pi_p$ = 3', ha='center', va='top', fontsize=9, color=INK)
axB.text(0.66, 0.10, 'symptomatic\nbarrier falls ↓', ha='center', va='center', fontsize=8, color=RUST)
axB.text(0.33, 0.085, 'asymptomatic\nbarrier rises ↑', ha='center', va='center', fontsize=8, color=RUST)

# ---------------------------------------------------------------- C: simulations
dt = 0.01
T = 320.0
n = int(T / dt)
t = np.arange(n) * dt
t_on, t_off = 80.0, 160.0


def simulate(pp_of_t, I_of_t, seed, s0=0.9):
    rng = np.random.default_rng(seed)
    out = np.empty(n)
    x = s0
    noise = rng.standard_normal(n) * np.sqrt(2 * D * dt)
    for k in range(n):
        out[k] = x
        x = x + (-dF(x, I_of_t[k], pp_of_t[k])) * dt + noise[k]
    return out


window = (t >= t_on) & (t < t_off)
pp_base = np.full(n, PP0)
pp_hyp = np.where(window, PP1, PP0)
I_base = np.full(n, I0)
I_phys = np.where(t >= t_on, I1, I0)

runs = [
    ('Tilt only: I 0.50 → 0.42; fixed $\\Pi_p$', pp_base, I_phys, RUST, 11),
    ('Flatten only: $\\Pi_p$ 3 → 1.3 temporarily; I = 0.50', pp_hyp, I_base, TEAL, 23),
    (r'Concurrent flatten and maintained tilt: $\Pi_p$ window and I = 0.42', pp_hyp, I_phys, DARK, 5),
]

# Seeds are predeclared above; never select a seed conditional on its eventual outcome.
# These remain individual random paths and do not establish relative efficacy.

for i, (label, pp, I, col, seed) in enumerate(runs):
    ax = axC[i]
    y = simulate(pp, I, seed)
    ax.axvspan(t_on, t_off, color=CYAN, alpha=0.35, lw=0, zorder=0)
    ax.axhline(0.5, color=GREY, lw=0.7, ls=':')
    ax.plot(t, y, color=col, lw=1.1)
    ax.set_ylim(-0.1, 1.1); ax.set_xlim(0, T)
    ax.set_yticks([0, 0.5, 1])
    ax.set_ylabel('s', rotation=0, labelpad=10)
    ax.text(0.01, 0.95, label, transform=ax.transAxes, ha='left', va='top', fontsize=8.6, color=INK,
            bbox=dict(fc='white', ec='none', alpha=0.85, pad=1.5))
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    if i < 2:
        ax.set_xticklabels([])
    print(label[:22], 'seed', seed, 'final s', round(float(y[-1]), 3), 'min in window', round(float(y[window].min()), 3))

axC[0].set_title('C  Three predeclared-seed trajectories (illustrative only)',
                 loc='left', fontweight='bold', fontsize=12.5, pad=10)
axC[2].set_xlabel('time  (units of τ)')
axC[0].text(t_on + 2, -0.04, 'flattening window', fontsize=8, color=DARK, ha='left', va='bottom')

out = './Figure5'
fig.savefig(out + '.png', dpi=300)
fig.savefig(out + '.tiff', dpi=300, pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig(out + '.pdf')
print('saved', out)
