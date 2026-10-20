"""Demonstrate isolated versus coupled defensive-state persistence under zero residual threat.
All models synthetic and based on Figure 4 parameterization, not empirical FND data.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(__file__).resolve().parent
k,theta=4.,.75
sig=lambda z:1/(1+np.exp(-k*(z-theta)))
dt=.02;t=np.arange(0,300,dt)

def simulate(h,u,T_post,w=.7):
 s=np.empty(len(t));d=np.empty(len(t));b=np.empty(len(t))
 s[0],d[0],b[0]=.03,.05,.03
 for i in range(1,len(t)):
  T=.9 if 40<=t[i-1]<70 else T_post
  s[i]=s[i-1]+dt*(-s[i-1]+sig(.45*s[i-1]+.3*b[i-1]+w*d[i-1]-.05))
  d[i]=d[i-1]+dt/2*(-d[i-1]+sig(h*d[i-1]+u*s[i-1]+T))
  b[i]=b[i-1]+dt/3*(-b[i-1]+s[i-1])
 return s,d
cases=[(1.3,0,.1,'Residual threat T=0.10; no symptom→defence loop'),
       (1.3,0,0,'T=0, u=0: isolated defensive state resets'),
       (1.3,.15,0,'T=0, u=0.15: coupled loop can maintain capture'),
       (1.4,0,0,'T=0, h=1.40: defensive recurrence sustains high state')]
fig,ax=plt.subplots(2,2,figsize=(10.5,6.0),sharex=True,sharey=True)
for a,(h,u,T_post,label) in zip(ax.flat,cases):
 s,d=simulate(h,u,T_post)
 a.axvspan(40,70,alpha=.12,color='gray')
 a.plot(t,s,label='symptom state s',lw=1.6)
 a.plot(t,d,label='defensive state d',lw=1.3,ls='--')
 a.set_title(label,fontsize=9.5)
 a.text(0.97,.22,f'end: s={s[-1]:.3f}, d={d[-1]:.3f}',transform=a.transAxes,ha='right',va='bottom',fontsize=8.5)
 a.set_ylim(0,1.05)
 a.spines[['top','right']].set_visible(False)
for a in ax[:,0]:a.set_ylabel('State coordinate (arbitrary)')
for a in ax[-1,:]:a.set_xlabel('Time (arbitrary)')
ax[0,0].legend(loc='center right',fontsize=7.5,frameon=False)
fig.suptitle('Dependence of apparent defensive-state persistence on residual input and reciprocal coupling',fontsize=11)
fig.tight_layout()
fig.savefig(out/'figure4_reset_sensitivity.png',dpi=240)
fig.savefig(out/'figure4_reset_sensitivity.pdf')
print('saved Figure 4 reset-sensitivity check')
