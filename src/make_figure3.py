"""Figure 3: Capture as a property of the coupled brain-body-environment system.
(A) Nested coupled systems after Chiel & Beer, annotated for FND.
(B) Phase portrait of a two-variable brain-body model: each subsystem is monostable alone; coupled, bistable.
(C) Uncoupling early versus late: feedback-dependent (reflexive-like) vs autonomous (consolidated) capture.
(D) Parameter chart of the recurrent-gain model: region of bistability in the (drive, gain) plane with a
    patient trajectory and the two treatment directions."""
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
                     'xtick.labelsize': 9.5, 'ytick.labelsize': 9.5, 'legend.fontsize': 9.2,
                     'legend.frameon': False, 'mathtext.default': 'it'})
TEAL, DARK, RUST, CYAN, GREY, INK = '#20808D', '#1B474D', '#A84B2F', '#9ED4DC', '#8A8A8A', '#222222'
K, THETA = 4.0, 0.75

def sig(u):
    return 1 / (1 + np.exp(-K * (u - THETA)))

fig, axs = plt.subplots(2, 2, figsize=(9.6, 8.5), dpi=300)
fig.subplots_adjust(left=0.075, right=0.985, top=0.95, bottom=0.07, wspace=0.32, hspace=0.42)

def title(ax, letter, text):
    ax.set_title(f'{letter}  {text}', loc='left', fontweight='bold', fontsize=12.5, pad=10)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)

# ---------------------------------------------------------------- A: nested coupled systems
ax = axs[0, 0]
title(ax, 'A', 'The brain has a body: three coupled systems')
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
def box(x, y, w, h, ec, lw, fc='white', z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.35', fc=fc, ec=ec, lw=lw, zorder=z))
box(0.3, 0.3, 9.4, 9.0, GREY, 1.4, fc='#F4F4F2')
box(1.6, 1.4, 6.8, 6.1, TEAL, 1.6, fc='#E9F4F5', z=2)
box(3.1, 3.6, 3.8, 3.0, DARK, 1.8, fc='white', z=3)
ax.text(5.0, 8.85, 'Environment', ha='center', va='center', fontsize=11, fontweight='bold', color=INK, zorder=4)
ax.text(0.75, 8.05, 'avoidance, aids, medical uncertainty, social response', ha='left', va='center', fontsize=8.8, color=INK, zorder=4)
ax.text(5.0, 7.0, 'Body', ha='center', va='center', fontsize=11, fontweight='bold', color=TEAL, zorder=4)
ax.text(5.0, 6.1, 'Nervous system', ha='center', va='center', fontsize=11, fontweight='bold', color=DARK, zorder=4)
ax.text(5.0, 4.85, 'high-precision prediction\nof impairment;\nsalience gain on it', ha='center', va='center',
        fontsize=8.8, color=INK, zorder=4, linespacing=1.2)
ax.text(2.0, 2.15, 'guarding, bracing, disuse,\nautonomic arousal', ha='left', va='center', fontsize=8.8, color=TEAL, zorder=4)
# arrows: nervous system <-> body
ax.add_patch(FancyArrowPatch((4.1, 3.55), (4.1, 2.75), arrowstyle='-|>', mutation_scale=13, lw=1.6, color=DARK, zorder=5))
ax.add_patch(FancyArrowPatch((5.9, 2.75), (5.9, 3.55), arrowstyle='-|>', mutation_scale=13, lw=1.6, color=TEAL, zorder=5))
ax.text(3.95, 3.15, 'motor\noutput', ha='right', va='center', fontsize=8.3, color=DARK, zorder=5)
ax.text(6.05, 3.15, 'altered\nafferents', ha='left', va='center', fontsize=8.3, color=TEAL, zorder=5)
# arrows: body <-> environment
ax.add_patch(FancyArrowPatch((7.0, 1.35), (7.0, 0.6), arrowstyle='-|>', mutation_scale=13, lw=1.6, color=TEAL, zorder=5))
ax.add_patch(FancyArrowPatch((8.6, 0.6), (8.6, 1.35), arrowstyle='-|>', mutation_scale=13, lw=1.6, color=GREY, zorder=5))
ax.text(7.15, 0.98, 'action', ha='left', va='center', fontsize=8.3, color=TEAL, zorder=5)
ax.text(8.75, 0.98, 'feedback', ha='left', va='center', fontsize=8.3, color=GREY, zorder=5)
# precipitant
ax.add_patch(FancyArrowPatch((10.4, 9.9), (9.5, 8.9), arrowstyle='-|>', mutation_scale=13, lw=1.6, color=RUST, zorder=6, clip_on=False))
ax.text(9.35, 9.75, 'precipitant\n(perturbation)', ha='right', va='center', fontsize=8.6, color=RUST, zorder=6, clip_on=False)
ax.text(5.0, -0.55, 'Symptom = trajectory of the coupled system, not a state of any one part', ha='center', va='center',
        fontsize=8.8, color=INK, style='italic', clip_on=False)

# ---------------------------------------------------------------- B: phase portrait of coupled model
ax = axs[0, 1]
gn, c, I0 = 0.5, 1.0, 0.0          # brain intrinsic gain (monostable alone), coupling, drive
tau_s, tau_b = 1.0, 3.0
def field(s, b):
    return (-s + sig(gn * s + c * b + I0)) / tau_s, (-b + s) / tau_b
B, S = np.meshgrid(np.linspace(-0.05, 1.05, 30), np.linspace(-0.05, 1.05, 30))
dS, dB = field(S, B)
ax.streamplot(B, S, dB, dS, color='#BDBDBD', density=1.0, linewidth=0.7, arrowsize=0.8)
bb = np.linspace(-0.05, 1.05, 400)
# s-nullcline: s = sig(gn s + c b + I0) -> solve for b given s: b = (sig^-1(s) - gn s - I0)/c
ss = np.linspace(0.005, 0.995, 400)
b_null = (THETA + np.log(ss / (1 - ss)) / K - gn * ss - I0) / c
ax.plot(b_null, ss, color=DARK, lw=2.2)
ax.plot(bb, bb, color=TEAL, lw=2.2)
ax.text(0.86, 0.66, 'brain nullcline\n(ds/dt = 0)', color=DARK, fontsize=8.8, ha='left', va='top')
ax.text(0.30, 0.235, 'body–environment\nnullcline (db/dt = 0)', color=TEAL, fontsize=8.8, ha='left', va='top')
# fixed points: s = b and s = sig((gn + c) s + I0)
g = np.linspace(0, 1, 100001); h = g - sig((gn + c) * g + I0)
fp_raw = g[np.where(np.diff(np.sign(h)) != 0)[0]]
# deduplicate numerically repeated roots (a root at exactly s = 0.5 can register twice)
fp = []
for p in fp_raw:
    if not fp or abs(p - fp[-1]) > 1e-3:
        fp.append(p)
fp = np.array(fp)
assert len(fp) == 3, fp
for p in fp:
    slope = K * sig((gn + c) * p + I0) * (1 - sig((gn + c) * p + I0)) * (gn + c)
    stable = slope < 1
    ax.plot(p, p, 'o', ms=9, mfc=RUST if stable else 'white', mec=RUST, mew=1.8, zorder=6)
# separatrix: integrate backwards from saddle along its stable direction
saddle = fp[1]
J = np.array([[(-1 + K * sig((gn + c) * saddle + I0) * (1 - sig((gn + c) * saddle + I0)) * gn) / tau_s,
               (K * sig((gn + c) * saddle + I0) * (1 - sig((gn + c) * saddle + I0)) * c) / tau_s],
              [1 / tau_b, -1 / tau_b]])
w, v = np.linalg.eig(J)
vs = v[:, np.argmin(w.real)].real
for sgn in (1, -1):
    x = np.array([saddle, saddle]) + sgn * 1e-3 * vs
    pts = [x.copy()]
    for _ in range(6000):
        ds_, db_ = field(x[0], x[1])
        x = x - 0.01 * np.array([ds_, db_])
        pts.append(x.copy())
        if not (-0.1 < x[0] < 1.1 and -0.1 < x[1] < 1.1):
            break
    pts = np.array(pts)
    ax.plot(pts[:, 1], pts[:, 0], color=RUST, ls='--', lw=1.4)
ax.text(fp[2] - 0.03, fp[2], 'Symptomatic attractor', color=RUST, fontsize=9, ha='right', va='center')
ax.text(fp[0] + 0.03, fp[0], 'Asymptomatic attractor', color=RUST, fontsize=9, ha='left', va='center')
ax.text(fp[1] + 0.03, fp[1] - 0.005, 'Saddle', color=RUST, fontsize=9, ha='left', va='top')
ax.text(0.56, 0.44, 'separatrix', color=RUST, fontsize=9, ha='left', va='top', rotation=-55)
title(ax, 'B', 'Capture is a property of the coupled system')
ax.set_xlabel('body–environment state  b')
ax.set_ylabel('brain state  s')
ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05)

# ---------------------------------------------------------------- C: uncoupling early vs late
ax = axs[1, 0]
T, dt = 400.0, 0.02
t = np.arange(0, T, dt)
I_base, I_pulse = -0.05, 0.40
I_t = np.where((t >= 50) & (t < 80), I_pulse, I_base)
def run(t_cut, eps=0.012, g_max=1.6):
    s = np.zeros_like(t); b = np.zeros_like(t); g = np.full_like(t, 0.5)
    s[0], b[0] = 0.03, 0.03
    for i in range(1, len(t)):
        cc = c if t[i-1] < t_cut else 0.0
        s[i] = s[i-1] + dt / tau_s * (-s[i-1] + sig(g[i-1] * s[i-1] + cc * b[i-1] + I_t[i-1]))
        b[i] = b[i-1] + dt / tau_b * (-b[i-1] + s[i-1])
        g[i] = min(g_max, g[i-1] + dt * eps * max(s[i-1] - 0.3, 0.0))
    return s, g
s_early, g_early = run(110)
s_late, g_late = run(260)
ax.axvspan(50, 80, color=RUST, alpha=0.12, lw=0)
ax.text(65, 1.13, 'precipitant', color=RUST, fontsize=9, ha='center')
ax.plot(t, s_early, color=TEAL, lw=2.0, label='feedback removed early (t = 110): symptom dissolves')
ax.plot(t, s_late, color=DARK, lw=2.0, label='feedback removed late (t = 260): symptom persists')
ax.plot(t, g_late, color=GREY, ls=':', lw=1.6, label='intrinsic gain g (consolidation)')
for tc, col in ((110, TEAL), (260, DARK)):
    ax.axvline(tc, color=col, ls='--', lw=1.0)
ax.text(112, 0.02, 'cut', color=TEAL, fontsize=8.5, ha='left')
ax.text(262, 0.02, 'cut', color=DARK, fontsize=8.5, ha='left')
ax.axhline(1.0, color=GREY, lw=0.6, ls='-', alpha=0.5)
ax.text(398, 1.03, 'Gain threshold permitting\nbistability at a suitable drive', color=GREY, fontsize=8, ha='right', va='bottom')
title(ax, 'C', 'Feedback-dependent, then autonomous')
ax.set_xlabel('time (arbitrary units)')
ax.set_ylabel('brain state  s(t)   /   gain  g(t)')
ax.set_xlim(0, 400); ax.set_ylim(-0.05, 1.9)
ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0), handlelength=1.8)

# ---------------------------------------------------------------- D: parameter chart of the recurrent-gain model
ax = axs[1, 1]
TH = 1.5  # threshold of sigma for this panel (drive expressed on a positive scale)
Gs = np.linspace(1.0001, 3.0, 400)
def fold_I(G):
    disc = np.sqrt(np.maximum(0, 0.25 - 1 / (K * G)))
    s1, s2 = 0.5 - disc, 0.5 + disc
    I1 = TH + np.log(s1 / (1 - s1)) / K - G * s1     # upper fold (onset), at low s
    I2 = TH + np.log(s2 / (1 - s2)) / K - G * s2     # lower fold (remission), at high s
    return I1, I2
Iu, Il = fold_I(Gs)
ax.fill_betweenx(Gs, Il, Iu, color=CYAN, alpha=0.55, lw=0)
ax.plot(Iu, Gs, color=DARK, lw=2.0); ax.plot(Il, Gs, color=DARK, lw=2.0)
ax.plot(TH - 0.5, 1.0, 'o', ms=6, color=DARK)
ax.text(0.98, 0.97, 'cusp (kG = 4)', fontsize=8.6, color=DARK, ha='right', va='top')
ax.text(0.1, 2.82, 'bistable (hysteresis)', fontsize=9.5, color=DARK, ha='center', va='center', fontweight='bold')
ax.text(-0.25, 1.45, 'asymptomatic only', fontsize=9.5, color=TEAL, ha='left', va='center')
ax.text(1.55, 2.6, 'symptomatic\nonly', fontsize=9.5, color=RUST, ha='right', va='center')
ax.text(1.5, 1.4, 'onset fold', fontsize=8.6, color=DARK, ha='right', rotation=-38)
ax.text(0.05, 1.55, 'remission fold', fontsize=8.6, color=DARK, ha='left', rotation=-60)
# patient trajectory: precipitant -> onset -> drive returns -> consolidation -> two treatment directions
path = [(0.3, 1.8), (0.95, 1.8), (0.95, 1.8), (0.6, 2.4)]
labels = ['1 precipitant', '2 drive\n   subsides', '3 consolidation\n   (gain rises)']
ax.add_patch(FancyArrowPatch((0.3, 1.85), (0.95, 1.85), arrowstyle='-|>', mutation_scale=13, lw=1.8, color=RUST, zorder=6))
ax.plot([0.95, 0.95], [1.85, 1.75], color=RUST, lw=1.8, zorder=6)
ax.add_patch(FancyArrowPatch((0.95, 1.75), (0.62, 1.75), arrowstyle='-|>', mutation_scale=13, lw=1.8, color=RUST, zorder=6))
ax.add_patch(FancyArrowPatch((0.6, 1.75), (0.6, 2.36), arrowstyle='-|>', mutation_scale=13, lw=1.8, color=RUST, zorder=6))
ax.plot(0.3, 1.85, 'o', ms=7, mfc='white', mec=RUST, mew=1.6, zorder=7)
ax.text(0.62, 1.9, '1 precipitant', fontsize=8.6, color=RUST, ha='center', va='bottom')
ax.text(-0.24, 1.04, 'Conceptual patient trajectory\n(not a simulated path)', fontsize=8, color=RUST, ha='left', va='center', style='italic')
ax.text(0.8, 1.7, '2 drive subsides', fontsize=8.6, color=RUST, ha='center', va='top')
ax.text(0.64, 2.12, '3 consolidation', fontsize=8.6, color=RUST, ha='left', va='center')
ax.plot(0.6, 2.4, 'o', ms=7, color=RUST, zorder=7)
ax.add_patch(FancyArrowPatch((0.6, 2.4), (-0.2, 2.4), arrowstyle='-|>', mutation_scale=13, lw=1.8, color=TEAL, zorder=6))
ax.add_patch(FancyArrowPatch((0.56, 2.4), (0.56, 1.3), arrowstyle='-|>', mutation_scale=13, lw=1.8, color=TEAL, zorder=6))
ax.text(0.15, 2.46, 'reduce drive I', fontsize=8.6, color=TEAL, ha='center', va='bottom')
ax.text(0.52, 1.2, 'reduce gain G', fontsize=8.6, color=TEAL, ha='right', va='center')
title(ax, 'D', 'Parameter chart and treatment directions')
ax.set_xlabel('Translated external-drive coordinate  I')
ax.set_ylabel('recurrent gain  G')
ax.set_xlim(-0.3, 1.8); ax.set_ylim(0.8, 3.0)

out = './Figure3'
fig.savefig(out + '.png', dpi=300)
fig.savefig(out + '.tiff', dpi=300, pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig(out + '.pdf')
print('Panels B, C: sigma(x)=1/(1+exp[-%g*(x-%g)])' % (K, THETA))
print('Panel B equilibria (s*, b*):', [(round(float(p), 4), round(float(p), 4)) for p in fp])
print('Panel C early (c=0 at t=110): final s=%.3f, final g=%.3f' % (s_early[-1], g_early[-1]))
print('Panel C late  (c=0 at t=260): final s=%.3f, final g=%.3f' % (s_late[-1], g_late[-1]))
print('Panel D: k=%g, theta=%g (translated drive coordinate)' % (K, TH))
