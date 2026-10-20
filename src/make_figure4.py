"""Figure 4: The defensive layer — a subcortical variable that fails to reset.
(A) Vertical architecture of capture: cortical representation s, subcortical defensive circuit d
    (amygdala -> hypothalamus -> PAG, with the neuromodulatory arousal loop h), striatal habit
    consolidation raising g, and body-environment b.
(B) Fixed points of the defensive variable d against threat T for sub- and supracritical arousal-loop gain h:
    reset versus failure to reset (hysteresis of d).
(C) Time course after a threat pulse for the two values of h: d resets or stays engaged; s follows.
(D) Arousal-directed intervention early versus late while striatal consolidation raises g."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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
K, THETA = 4.0, 0.75

def sig(u):
    return 1 / (1 + np.exp(-K * (u - THETA)))

fig, axs = plt.subplots(2, 2, figsize=(9.6, 8.6), dpi=300)
fig.subplots_adjust(left=0.075, right=0.985, top=0.95, bottom=0.07, wspace=0.32, hspace=0.42)

def title(ax, letter, text):
    ax.set_title(f'{letter}  {text}', loc='left', fontweight='bold', fontsize=12.5, pad=10)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)

# ---------------------------------------------------------------- A: vertical architecture
ax = axs[0, 0]
title(ax, 'A', 'The vertical architecture of capture')
ax.set_xlim(-0.2, 10); ax.set_ylim(0, 10); ax.axis('off')
def box(x, y, w, h, ec, lw, fc='white', z=1, ls='-'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.3', fc=fc, ec=ec, lw=lw, zorder=z, ls=ls))
def arrow(p, q, col, lw=1.6, z=5, style='-|>', cs=None, ls='-'):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=12, lw=lw, color=col, zorder=z,
                                 connectionstyle=cs or 'arc3,rad=0', ls=ls))
# cortex
box(0.4, 7.3, 6.9, 2.3, DARK, 1.8, fc='white', z=3)
ax.text(0.7, 9.25, 'Cortex   s', ha='left', va='center', fontsize=10.5, fontweight='bold', color=DARK, zorder=4)
ax.text(0.7, 8.35, 'salience gain (anterior insula, cingulate);\nsymptom prediction (SMA, somatomotor);\nrecurrent gain  g', ha='left', va='center', fontsize=8.2, color=INK, zorder=4, linespacing=1.25)
# striatum
box(7.8, 7.3, 2.0, 2.3, GOLD, 1.6, fc='#FBF7EA', z=3)
ax.text(8.8, 9.2, 'Striatum', ha='center', va='center', fontsize=9.5, fontweight='bold', color=GOLD, zorder=4)
ax.text(8.8, 8.2, 'candidate learning\nprocesses may\nmodify g', ha='center', va='center', fontsize=7.6, color=INK, zorder=4, linespacing=1.2)
arrow((7.75, 8.45), (7.35, 8.45), GOLD, lw=1.5)
# subcortical defensive circuit
box(1.9, 3.35, 5.6, 3.3, RUST, 1.8, fc='#FBF1EC', z=3)
ax.text(2.15, 6.3, 'Defensive survival circuit   d', ha='left', va='center', fontsize=10.5, fontweight='bold', color=RUST, zorder=4)
ax.text(2.15, 5.55, 'amygdala  →  hypothalamus  →  PAG', ha='left', va='center', fontsize=8.6, color=INK, zorder=4)
ax.text(2.15, 4.75, 'PAG pathways: defensive / autonomic output\n(no FND phenotype assignment)', ha='left', va='center', fontsize=7.6, color=INK, zorder=4, linespacing=1.2)
ax.text(2.15, 3.85, 'column-specific contributions not resolved\nby scalar state d', ha='left', va='center', fontsize=7.6, color=INK, zorder=4, linespacing=1.2)
# arousal loop h (self-loop on the right edge of the defensive box)
arrow((7.55, 4.6), (7.55, 6.0), RUST, lw=1.6, cs='arc3,rad=0.9')
ax.text(9.95, 5.55, 'neuromodulatory\narousal loop  h\n(LeDoux)', ha='right', va='center', fontsize=7.9, color=RUST, zorder=6, linespacing=1.2)
# threat input
arrow((9.7, 3.75), (7.6, 3.75), RUST, lw=1.6, z=6)
ax.text(8.65, 3.95, 'threat  T', ha='center', va='bottom', fontsize=8.8, color=RUST, zorder=6)
# body-environment
box(0.4, 0.35, 9.4, 2.2, TEAL, 1.6, fc='#E9F4F5', z=3)
ax.text(0.7, 2.2, 'Body and environment   b', ha='left', va='center', fontsize=10.5, fontweight='bold', color=TEAL, zorder=4)
ax.text(0.7, 1.3, 'guarding, disuse, altered afferents (c);   autonomic output;\navoidance, aids, social response', ha='left', va='center', fontsize=8.2, color=INK, zorder=4, linespacing=1.25)
# arrows: d -> s (w) and s -> d (u)
arrow((3.0, 6.7), (3.0, 7.25), RUST, lw=1.8)
ax.text(3.15, 6.98, 'w', ha='left', va='center', fontsize=9.5, color=RUST, style='italic', zorder=6)
arrow((4.8, 7.25), (4.8, 6.7), DARK, lw=1.8)
ax.text(4.95, 6.98, 'u  (symptom appraised as threat)', ha='left', va='center', fontsize=7.6, color=DARK, zorder=6)
# arrows: s <-> b down the left side, outside the defensive box
arrow((0.8, 7.25), (0.8, 2.6), DARK, lw=1.5)
arrow((1.4, 2.6), (1.4, 7.25), TEAL, lw=1.5)
ax.text(0.62, 5.0, 'motor output', ha='right', va='center', fontsize=7.8, color=DARK, rotation=90, zorder=6)
ax.text(1.58, 5.0, 'afferents  c', ha='left', va='center', fontsize=7.8, color=TEAL, rotation=90, zorder=6)
# d -> body autonomic
arrow((2.6, 3.3), (2.6, 2.6), RUST, lw=1.4)
ax.text(2.75, 2.95, 'autonomic output', ha='left', va='center', fontsize=7.8, color=RUST, zorder=6)
ax.text(4.9, -0.45, 'Potential persistence routes: intrinsic gain (g), body feedback (c),\nand defensive feedback (h, u, w); all conditional',
        ha='center', va='center', fontsize=8.2, color=INK, style='italic', clip_on=False, linespacing=1.2)

# ---------------------------------------------------------------- C/D simulation helpers
dt = 0.02
tau_s, tau_d, tau_b = 1.0, 2.0, 3.0
g0, c, w, u = 0.45, 0.3, 0.7, 0.15
T_base = 0.10

def simulate(t, T_t, h, g_eps=0.0, g_max=1.6, d_cut=None, noise=0.0, seed=1):
    rng = np.random.default_rng(seed)
    s = np.zeros_like(t); d = np.zeros_like(t); b = np.zeros_like(t); g = np.full_like(t, g0)
    s[0], d[0], b[0] = 0.03, 0.05, 0.03
    for i in range(1, len(t)):
        Ti = T_t[i-1]
        hi = h if (d_cut is None or t[i-1] < d_cut) else 0.0   # illustrative intervention jointly changes h and T, not an isolated causal effect
        if d_cut is not None and t[i-1] >= d_cut:
            Ti = -0.2                                           # and lower threat below baseline
        s[i] = s[i-1] + dt / tau_s * (-s[i-1] + sig(g[i-1] * s[i-1] + c * b[i-1] + w * d[i-1] - 0.05)) + noise * rng.normal() * np.sqrt(dt)
        d[i] = d[i-1] + dt / tau_d * (-d[i-1] + sig(hi * d[i-1] + u * s[i-1] + Ti)) + noise * rng.normal() * np.sqrt(dt)
        b[i] = b[i-1] + dt / tau_b * (-b[i-1] + s[i-1])
        g[i] = min(g_max, g[i-1] + dt * g_eps * max(s[i-1] - 0.3, 0.0))
    return s, d, b, g

# ---------------------------------------------------------------- B: fixed points of d against T
ax = axs[0, 1]
title(ax, 'B', 'Defensive-state equilibria depend on input')
dd = np.linspace(0.002, 0.998, 2000)
for h, col, lab in ((0.6, TEAL, 'h = 0.6: resets'), (1.3, RUST, 'h = 1.3: bistability for selected T')):
    T_of_d = THETA + np.log(dd / (1 - dd)) / K - h * dd        # T such that d is a fixed point (s = 0)
    slope = K * dd * (1 - dd) * h
    stable = slope < 1
    ax.plot(np.where(stable, T_of_d, np.nan), dd, color=col, lw=2.3, label=lab)
    ax.plot(np.where(~stable, T_of_d, np.nan), dd, color=col, lw=1.4, ls=':')
    if h > 1:
        disc = np.sqrt(0.25 - 1 / (K * h)); d1, d2 = 0.5 - disc, 0.5 + disc
        Tu = THETA + np.log(d1 / (1 - d1)) / K - h * d1
        Tl = THETA + np.log(d2 / (1 - d2)) / K - h * d2
        ax.annotate('', xy=(Tu, d2 + 0.05), xytext=(Tu, d1), arrowprops=dict(arrowstyle='-|>', color=col, lw=1.6))
        ax.annotate('', xy=(Tl, d1 - 0.05), xytext=(Tl, d2), arrowprops=dict(arrowstyle='-|>', color=col, lw=1.6))
        ax.text(Tu + 0.03, 0.5, 'threat\nengages\nthe circuit', fontsize=8.4, color=col, ha='left', va='center')
        ax.text(-0.29, 0.8, 'reset needs\nthreat far\nbelow onset', fontsize=8.4, color=col, ha='left', va='center')
        ax.axvspan(Tl, Tu, color=CYAN, alpha=0.25, lw=0)
        print('folds of d for h=1.3:', round(Tu, 3), round(Tl, 3))
ax.axvline(T_base, color=GREY, ls='--', lw=1.0)
ax.text(0.19, 0.03, 'residual threat\nafter the event', fontsize=8.2, color=GREY, ha='left', va='bottom')
ax.set_xlabel('threat  T')
ax.set_ylabel('defensive engagement  d*')
ax.set_xlim(-0.3, 1.3); ax.set_ylim(-0.02, 1.02)
ax.legend(loc='center right', bbox_to_anchor=(1.0, 0.36))

# ---------------------------------------------------------------- C: threat pulse, two values of h
ax = axs[1, 0]
title(ax, 'C', 'Pulse followed by residual threat T = 0.10')
Tend = 300.0
t = np.arange(0, Tend, dt)
T_t = np.where((t >= 40) & (t < 70), 0.9, T_base)
ax.axvspan(40, 70, color=RUST, alpha=0.12, lw=0)
ax.text(55, 1.13, 'threat', color=RUST, fontsize=9, ha='center')
for h, col, ls_d, lab in ((0.6, TEAL, '-', 'h = 0.6'), (1.3, RUST, '-', 'h = 1.3')):
    s, d, b, g = simulate(t, T_t, h)
    ax.plot(t, d, color=col, lw=1.6, ls='--', label=f'defensive state d ({lab})')
    ax.plot(t, s, color=col, lw=2.2, label=f'symptom s ({lab})')
    print(f'C h={h}: final d={d[-1]:.3f} s={s[-1]:.3f}')
ax.set_xlabel('time (arbitrary units)')
ax.set_ylabel('state')
ax.set_xlim(0, Tend); ax.set_ylim(-0.05, 1.75)
ax.legend(loc='upper left', ncol=2, handlelength=1.8, columnspacing=1.2)
ax.text(Tend - 3, 0.62, f'cortical gain g = {g0} and body coupling c = {c}:\nsubcritical together (g + c < 1); symptom is held by d', fontsize=8.2, color=INK, ha='right', va='center')

# ---------------------------------------------------------------- D: arousal-directed treatment early vs late
ax = axs[1, 1]
title(ax, 'D', 'Joint h/T reduction at two times (g evolves)')
Tend = 420.0
t = np.arange(0, Tend, dt)
T_t = np.where((t >= 40) & (t < 70), 0.9, T_base)
ax.axvspan(40, 70, color=RUST, alpha=0.12, lw=0)
ax.text(55, 1.13, 'threat', color=RUST, fontsize=9, ha='center')
s_e, d_e, _, g_e = simulate(t, T_t, 1.3, g_eps=0.006, d_cut=120)
s_l, d_l, _, g_l = simulate(t, T_t, 1.3, g_eps=0.006, d_cut=300)
ax.plot(t, s_e, color=TEAL, lw=2.2, label='joint h/T change at t = 120')
ax.plot(t, s_l, color=DARK, lw=2.2, label='joint h/T change at t = 300')
ax.plot(t, d_l, color=RUST, lw=1.4, ls='--', label='defensive state d (late case)')
ax.plot(t, g_l, color=GREY, ls=':', lw=1.6, label='effective intrinsic gain g (assumed adaptation)')
for tc, col in ((120, TEAL), (300, DARK)):
    ax.axvline(tc, color=col, ls='--', lw=1.0)
ax.text(122, 0.02, 'd ↓', color=TEAL, fontsize=8.5, ha='left')
ax.text(302, 0.02, 'd ↓', color=DARK, fontsize=8.5, ha='left')
ax.axhline(1.0, color=GREY, lw=0.6, alpha=0.5)
ax.text(306, 1.035, 'threshold\n(g = 1)', color=GREY, fontsize=7.4, ha='left', va='bottom', linespacing=1.15)
ax.set_xlabel('time (arbitrary units)')
ax.set_ylabel('state  /  gain')
ax.set_xlim(0, Tend); ax.set_ylim(-0.05, 2.3)
ax.legend(loc='upper left', handlelength=1.8)
print(f'D early: final s={s_e[-1]:.3f} g={g_e[-1]:.2f}; late: final s={s_l[-1]:.3f} g={g_l[-1]:.2f}, d={d_l[-1]:.3f}')

out = './Figure4'
fig.savefig(out + '.png', dpi=300)
fig.savefig(out + '.tiff', dpi=300, pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig(out + '.pdf')
print('saved')
