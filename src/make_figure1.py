"""Figure 1: Self-stabilising network capture and the symptomatic attractor.
Three panels: (A) capture loop, (B) bistable steady states with hysteresis, (C) critical slowing down.
Colour-blind-safe palette (teal / orange / grey; no red-green contrast)."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager

# Fonts
for f in ['Liberation Sans', 'Arial', 'DejaVu Sans']:
    if any(f == x.name for x in font_manager.fontManager.ttflist):
        plt.rcParams['font.family'] = f
        break
plt.rcParams.update({'font.size': 8, 'axes.linewidth': 0.8, 'axes.labelsize': 8.5,
                     'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'mathtext.default': 'it'})

TEAL = '#1B6F78'      # loop / high gain
TEAL_L = '#7FB8BF'    # low gain
ORANGE = '#C8641E'    # corrective learning / transition
GREY = '#6E6E6E'
INK = '#222222'

fig = plt.figure(figsize=(7.3, 5.5), dpi=300)
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1.15],
                      left=0.07, right=0.98, top=0.97, bottom=0.08, wspace=0.32, hspace=0.30)
axA = fig.add_subplot(gs[0, :])
axB = fig.add_subplot(gs[1, 0])
axC = fig.add_subplot(gs[1, 1])

# ---------------------------------------------------------------- Panel A: capture loop (rectangular cycle)
axA.set_xlim(-1.95, 1.95); axA.set_ylim(-1.0, 1.0); axA.set_aspect('equal'); axA.axis('off')
labels = ['Local signal\n(sensation, motor error,\nalarm, medical threat)',
          'High-precision\nsymptom-related\nprediction',
          'Altered action\nand attention',
          'Confirming\nafferent feedback',
          'Self-monitoring\nand arousal',
          'Avoidance']
X, Y = 1.22, 0.55
pos = np.array([[-X, Y], [0, Y], [X, Y], [X, -Y], [0, -Y], [-X, -Y]])   # clockwise
bw, bh = 0.98, 0.52
for (x, y), lab in zip(pos, labels):
    box = FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh, boxstyle='round,pad=0.02,rounding_size=0.06',
                         fc='white', ec=TEAL, lw=1.1, zorder=3)
    axA.add_patch(box)
    axA.text(x, y, lab, ha='center', va='center', fontsize=6.6, color=INK, zorder=4, linespacing=1.15)

def edge_point(c, target, w=bw / 2 + 0.035, h=bh / 2 + 0.035):
    d = target - c
    tx = w / abs(d[0]) if d[0] else np.inf
    ty = h / abs(d[1]) if d[1] else np.inf
    return c + d * min(tx, ty)

n = len(labels)
for i in range(n):
    a, b = pos[i], pos[(i + 1) % n]
    p0 = edge_point(a, b); p1 = edge_point(b, a)
    axA.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=10, lw=1.4, color=TEAL, zorder=2,
                                  shrinkA=0, shrinkB=0))

axA.text(0, 0.09, 'gain  $G$ ↑', ha='center', va='center', fontsize=10, color=TEAL, fontweight='bold')
axA.text(0, -0.11, 'each cycle raises the\nprecision of the next', ha='center', va='center',
         fontsize=6.8, color=GREY, linespacing=1.15)

# corrective learning: inhibitory (flat-headed) dashed arrow onto the action -> feedback edge, from the right
ymid = 0.0
dst = np.array([X + 0.08, ymid])
src = np.array([1.92, ymid])
axA.plot([src[0], dst[0]], [src[1], dst[1]], color=ORANGE, lw=1.4, ls=(0, (4, 2)), zorder=5)
axA.plot([dst[0], dst[0]], [ymid - 0.10, ymid + 0.10], color=ORANGE, lw=1.8, zorder=5)
axA.text(1.36, ymid - 0.08, 'Corrective\nsensorimotor learning\n$reduces$ gain', ha='left', va='top', fontsize=6.6,
         color=ORANGE, linespacing=1.2, zorder=6)
axA.text(-1.92, 0.98, 'A', fontsize=12, fontweight='bold', ha='left', va='top', color=INK)

# ---------------------------------------------------------------- Panel B: steady states and hysteresis
# Panel B uses the UNSHIFTED logistic sigma(x) = 1/(1 + exp(-k x)) with k = 1, theta = 0.
# Equilibria of tau ds/dt = -s + sigma(G s + I) satisfy I_eq(s) = (1/k) ln(s/(1-s)) - G s.
k, theta = 1.0, 0.0
def I_of_s(s, G):
    return theta + np.log(s / (1 - s)) / k - G * s

s = np.linspace(0.005, 0.995, 2000)
G_low, G_high = 2.5, 8.0
DISPLAY_SHIFT = -(G_high - G_low) / 2   # = -2.75: DISPLAY-ONLY translation of the low-gain curve along the drive axis
                                       # so that both curves share the same midpoint. It has no dynamical meaning.
I_low = I_of_s(s, G_low) + DISPLAY_SHIFT
I_high = I_of_s(s, G_high)

# folds for high gain: s(1-s) = 1/(kG)
disc = np.sqrt(1 - 4 / (k * G_high))
s1, s2 = (1 - disc) / 2, (1 + disc) / 2      # s1 lower fold (onset), s2 upper fold (recovery)
I_up = I_of_s(s1, G_high)      # onset drive (local max of I on lower branch)
I_down = I_of_s(s2, G_high)    # recovery drive (local min of I on upper branch)

axB.plot(I_low, s, color=TEAL_L, lw=1.2, label=f'low gain ($G$ = {G_low:g})')
lower = s <= s1; mid = (s > s1) & (s < s2); upper = s >= s2
axB.plot(I_high[lower], s[lower], color=TEAL, lw=2.2, label=f'high gain ($G$ = {G_high:g}), stable')
axB.plot(I_high[upper], s[upper], color=TEAL, lw=2.2)
axB.plot(I_high[mid], s[mid], color=TEAL, lw=1.4, ls=(0, (3, 2)), label='unstable threshold')

# hysteresis arrows
s_up_land = s[upper][np.argmin(abs(I_high[upper] - I_up))]
s_down_land = s[lower][np.argmin(abs(I_high[lower] - I_down))]
axB.annotate('', xy=(I_up, s_up_land - 0.02), xytext=(I_up, s1 + 0.02),
             arrowprops=dict(arrowstyle='-|>', color=ORANGE, lw=1.6, mutation_scale=10))
axB.annotate('', xy=(I_down, s_down_land + 0.02), xytext=(I_down, s2 - 0.02),
             arrowprops=dict(arrowstyle='-|>', color=ORANGE, lw=1.6, mutation_scale=10))
axB.text(I_up + 0.10, (s1 + s_up_land) / 2 + 0.12, 'onset', color=ORANGE, fontsize=7.5, va='center', ha='left')
axB.text(I_down - 0.10, (s2 + s_down_land) / 2 - 0.12, 'recovery', color=ORANGE, fontsize=7.5, va='center', ha='right')
axB.axvline(I_up, color=ORANGE, lw=0.6, ls=':', alpha=0.7)
axB.axvline(I_down, color=ORANGE, lw=0.6, ls=':', alpha=0.7)
axB.annotate('', xy=(I_up, 0.5), xytext=(I_down, 0.5),
             arrowprops=dict(arrowstyle='<->', color=GREY, lw=0.8, mutation_scale=8))
axB.text((I_up + I_down) / 2, 0.545, 'hysteresis', color=GREY, fontsize=7, ha='center', va='bottom', bbox=dict(fc='white', ec='none', pad=1.0))
axB.text(-0.2, 0.93, 'symptomatic\nstate', fontsize=7, color=INK, ha='right', va='top')
axB.text(-7.9, 0.10, 'asymptomatic\nstate', fontsize=7, color=INK, ha='left', va='center')

axB.set_xlim(-8.1, 0.1); axB.set_ylim(0, 1.0)
axB.set_xlabel('external drive  $I$  (threat, perturbation, context)', labelpad=2)
axB.set_ylabel('symptom-state strength  $s$', labelpad=2)
axB.set_yticks([0, 0.5, 1.0]); axB.set_xticks([-8,-6,-4,-2,0])
for sp in ('top', 'right'): axB.spines[sp].set_visible(False)
axB.legend(loc='upper left', frameon=False, fontsize=6.4, handlelength=1.8, borderaxespad=0.2)
axB.text(-0.10, 1.10, 'B', transform=axB.transAxes, fontsize=12, fontweight='bold', ha='left', va='top', color=INK)

# ---------------------------------------------------------------- Panel C: critical slowing down
rng = np.random.default_rng(7)
T, dt = 1200, 1.0
t = np.arange(T)
t_trans = 900
r = np.clip(0.5 * (1 - t / t_trans), 0.015, None)   # recovery rate declining towards the fold
x = np.zeros(T); x[0] = 0
sigma = 0.09
for i in range(1, T):
    if t[i] < t_trans:
        x[i] = x[i - 1] + (-r[i] * x[i - 1]) * dt + sigma * np.sqrt(dt) * rng.standard_normal()
    else:
        # jump to symptomatic state and settle there
        target = 1.6
        x[i] = x[i - 1] + 0.12 * (target - x[i - 1]) + 0.04 * rng.standard_normal()

# rolling lag-1 autocorrelation and variance (window 150) on pre-transition series
win = 150
ac = np.full(T, np.nan); var = np.full(T, np.nan)
for i in range(win, t_trans):
    seg = x[i - win:i]
    a = seg[:-1] - seg[:-1].mean(); b = seg[1:] - seg[1:].mean()
    ac[i] = (a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum())
    var[i] = seg.var()

axC.plot(t[:t_trans], x[:t_trans], color=TEAL, lw=0.7)
axC.plot(t[t_trans - 1:], x[t_trans - 1:], color=ORANGE, lw=1.2)
axC.axvline(t_trans, color=ORANGE, lw=0.9, ls='--')
axC.text(t_trans + 12, 0.75, 'imposed\ntransition', color=ORANGE, fontsize=7, ha='left', va='center')
axC.set_xlim(0, T); axC.set_ylim(-0.7, 1.9)
axC.set_xlabel('time  →  approaching the fold', labelpad=2)
axC.set_ylabel('synthetic state (arbitrary units)', labelpad=2)
axC.set_xticks([]); axC.set_yticks([])
for sp in ('top', 'right'): axC.spines[sp].set_visible(False)
axC.text(15, -0.6, 'fluctuations grow larger and slower', fontsize=7, color=GREY, ha='left', va='bottom')

# inset: rising autocorrelation
ins = axC.inset_axes([0.05, 0.60, 0.44, 0.36])
ins.plot(t[win:t_trans], ac[win:t_trans], color=INK, lw=0.9)
ins.set_xlim(win, T); ins.set_ylim(0, 1)
ins.set_xticks([]); ins.set_yticks([0, 1]); ins.tick_params(labelsize=6, length=2, pad=1)
ins.set_title('lag-1 autocorrelation', fontsize=6.5, pad=2)
ins.axvline(t_trans, color=ORANGE, lw=0.7, ls='--')
for sp in ('top', 'right'): ins.spines[sp].set_visible(False)
ins.patch.set_alpha(0.85)
axC.text(-0.10, 1.10, 'C  Synthetic slowing with imposed transition', transform=axC.transAxes, fontsize=10.5,
         fontweight='bold', ha='left', va='top', color=INK)
# Panel C is a generic Ornstein-Uhlenbeck-type illustration of critical slowing (declining recovery rate r(t));
# it is NOT a simulation of the nonlinear FND model.

fig.savefig('./Figure1.png', dpi=300, facecolor='white')
fig.savefig('./Figure1.tiff', dpi=300, facecolor='white', pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig('./Figure1.pdf', facecolor='white')
print('Panel B: sigma(x)=1/(1+exp(-x)), k=%g, theta=%g; G_low=%g, G_high=%g' % (k, theta, G_low, G_high))
print('Panel B: G=8 fold states s=%.3f, %.3f; fold drives I_onset=%.2f, I_recovery=%.2f' % (s1, s2, I_up, I_down))
print('Panel B: both gain curves shown on their actual, unshifted drive axes')
print('Panel C: illustrative OU-type process, seed 7; lag-1 autocorrelation range %.2f-%.2f' % (np.nanmin(ac), np.nanmax(ac)))
