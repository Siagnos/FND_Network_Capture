"""Figure 6: synthetic ensemble sensitivity to noise level and intervention timing.

Synthetic, not patient data. Normalised Ito SDE:
 ds = -(s-I + 2*pi*s*(1-s)*(1-2*s))*dt + sqrt(2*D)*dW.
Parameter schedules are described explicitly below; no clinical effects should be inferred.

Requires numpy and matplotlib. Run via `python src/run_all.py --suite figures`, or directly with
`python src/make_figure6.py` (outputs are then written next to the script).
"""
from pathlib import Path
from math import sqrt
import csv
import numpy as np
import matplotlib.pyplot as plt

SEED=20261019; N=1000; DT=.05; END=300.
DS=(.004,.006,.008)
SCENARIOS=('control','tilt','flatten','concurrent','tilt_then_flatten','flat_then_tilt')
LABELS={'control':'Control','tilt':'Tilt only','flatten':'Flatten only','concurrent':'Concurrent','tilt_then_flatten':'Tilt → flatten','flat_then_tilt':'Flatten → tilt'}

def parameters(t, scenario):
    I, pi = .5,3.
    if scenario in ('tilt','concurrent','tilt_then_flatten') and t>=80:I=.42
    if scenario=='flat_then_tilt' and t>=160:I=.42
    if scenario in ('flatten','concurrent','flat_then_tilt') and 80<=t<160:pi=1.3
    if scenario=='tilt_then_flatten' and 160<=t<240:pi=1.3
    return I,pi

def simulate(scenario,D,n=N,seed=SEED):
    rng=np.random.default_rng(seed)
    s=np.full(n, .5+sqrt(1./6.))
    first=np.full(n, np.nan)
    for step in range(round(END/DT)):
        t=step*DT
        I,pi=parameters(t,scenario)
        fp=(s-I)+2*pi*s*(1-s)*(1-2*s)
        s+= -fp*DT+sqrt(2*D*DT)*rng.standard_normal(n)
        new=np.isnan(first)&(s<.5)
        first[new]=(step+1)*DT
    return s,first

def wilson(x,n,z=1.9599639845):
    p=x/n;den=1+z*z/n;cen=(p+z*z/(2*n))/den
    half=z/den*sqrt(p*(1-p)/n+z*z/(4*n*n))
    return max(0,cen-half),min(1,cen+half)

def main():
    out=Path(__file__).resolve().parent
    rows=[]
    for D in DS:
        for cond in SCENARIOS:
            final, first=simulate(cond,D)
            yes=int(np.sum(final<.5)); lo,hi=wilson(yes,N)
            rows.append(dict(condition=cond,D=f'{D:.3f}',n=N,final_low_count=yes,
                             recovery_final=yes/N,wilson_lower=lo,wilson_upper=hi,
                             median_first_cross_time=np.nanmedian(first) if np.isfinite(first).any() else ''))
    with open(out/'capture_ensemble_results.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

    fig,ax=plt.subplots(figsize=(11.5,4.8))
    groups=np.arange(len(SCENARIOS));bar=.24
    for j,D in enumerate(DS):
        rr=[r for r in rows if r['D']==f'{D:.3f}']
        values=np.array([float(r['recovery_final']) for r in rr])*100
        errLo=np.array([float(r['recovery_final'])-float(r['wilson_lower']) for r in rr])*100
        errHi=np.array([float(r['wilson_upper'])-float(r['recovery_final']) for r in rr])*100
        ax.bar(groups+(j-1)*bar,values,bar,label=f'D={D:.3f}',yerr=np.maximum(0,np.array([errLo,errHi])),capsize=2,linewidth=.4)
    ax.set_ylim(0,108)
    ax.set_ylabel('Trajectories ending in low state at t = 300 (%)')
    ax.set_xticks(groups,[LABELS[c] for c in SCENARIOS],rotation=16,ha='right')
    ax.set_title('Synthetic ensemble sensitivity to noise and intervention timing (1,000 trajectories/arm)')
    ax.legend(loc='upper left',frameon=False,ncols=3)
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y',alpha=.2)
    fig.tight_layout()
    fig.savefig(out/'Figure6.png',dpi=300,bbox_inches='tight')
    fig.savefig(out/'Figure6.tiff',dpi=300,bbox_inches='tight',pil_kwargs={'compression':'tiff_lzw'})
    fig.savefig(out/'Figure6.pdf',bbox_inches='tight')
    plt.close(fig)
    for r in rows: print(r['D'], r['condition'], f"{float(r['recovery_final']):.3f}",f"CI [{float(r['wilson_lower']):.3f}, {float(r['wilson_upper']):.3f}]")
if __name__=='__main__': main()
