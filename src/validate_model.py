"""Executable numerical checks of the models underlying Figures 1-5.
No empirical observations; all units and coordinates synthetic.
Requires numpy, scipy and matplotlib.
"""
from pathlib import Path
from math import log,sqrt
import csv,json
import numpy as np
from scipy.optimize import brentq
from scipy.linalg import eigvals
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DEST=Path(__file__).resolve().parent
K=4;TH=.75
sig=lambda z:1/(1+np.exp(-4*(z-TH)))
def dF(s,I,P):return (s-I)+2*P*s*(1-s)*(1-2*s)
def F(s,I,P):return .5*(s-I)**2+P*s*s*(1-s)**2
def d2F(s,P):return 1+2*P*(1-6*s+6*s*s)
def roots(I,P):
    # solve cubic for stationarity using analytically calculated coefficients
    # dF/ds: 4P s^3 -6P s^2 +(2P+1)s-I
    z=np.roots([4*P,-6*P,2*P+1,-I]);return sorted(float(v.real) for v in z if abs(v.imag)<1e-8)
def folds(P):
    if P<=1:return []
    # d2F/ds = 1 + 2P(1-6s+6s²); analytic quadratic roots
    discr= (12*P)**2-4*(12*P)*(1+2*P)
    x0=(12*P - np.sqrt(discr))/(24*P)
    x1=(12*P + np.sqrt(discr))/(24*P)
    return [(float(x),float(x+2*P*x*(1-x)*(1-2*x))) for x in (x0,x1)]
def logistic_fold(G,k=1,th=0):
    assert k*G>4
    d=sqrt(1-4/(k*G))
    s1,s2=(1-d)/2,(1+d)/2
    fun=lambda s:th+log(s/(1-s))/k-G*s
    return [s1,s2],[fun(s1),fun(s2)]

# Direct analytic validation of figures 1-3
r={}
s,I=logistic_fold(8)
r['figure1_G8_fold_states']=[round(v,8) for v in s]
r['figure1_G8_fold_drives']=[round(v,8) for v in I]
assert np.allclose(s,[.1464466094,.8535533906],atol=1e-9)
for p in [2,3,4]:
    f=folds(p)
    r[f'figure2_p{p}_folds']=[{'s':round(s,8),'I':round(I,8)} for s,I in f]
    for s,I in f:assert abs(dF(s,I,p))<1e-9 and abs(d2F(s,p))<1e-9
# numerical vs analytical derivatives
for p in [1.3,2,3]:
 for s in [-.1,.1,.5,.93,1.15]:
  eps=1e-5
  grad=(F(s+eps,.42,p)-F(s-eps,.42,p))/(2*eps)
  curv=(dF(s+eps,.42,p)-dF(s-eps,.42,p))/(2*eps)
  assert abs(grad-dF(s,.42,p))<1e-8
  assert abs(curv-d2F(s,p))<1e-8
r['figure2_derivatives_checked']=True
# phase plot fig3 B critical x's
f=lambda s:-s+sig(1.5*s)
xs=np.linspace(0,1,2001)
pts=[]
for x1,x2 in zip(xs[:-1],xs[1:]):
 if f(x1)*f(x2)<0:pts.append(brentq(f,x1,x2,xtol=1e-13))
pts.append(.5)
pts=sorted(set(round(x,10) for x in pts))
assert len(pts)==3,pts
stability=[]
for x in pts:
 a=K*x*(1-x)
 J=np.array([[-1+.5*a,1*a],[1/3,-1/3]])
 es=eigvals(J)
 stability.append({'s_b':x,'eigenvalues':[float(v.real) for v in es],'stable':bool(np.all(es.real<0))})
assert [v['stable'] for v in stability]==[True,False,True]
r['figure3_equilibria_and_jacobian']=stability
# fig4 B h=1.3, residual threat .1; NOT a self-sustaining d state at T=0
for h in [1.3,1.4]:
 disc=sqrt(.25-1/(K*h));ds=[.5-disc,.5+disc]
 fs=[TH+log(z/(1-z))/K-h*z for z in ds]
 r[f'figure4_h{h}_fold_T']=[round(v,7) for v in fs]
 assert fs[0]>fs[1]
r['figure4_Tzero_persistent_h13']=False
r['figure4_Tpoint1_persistent_h13']=True
assert 0<r['figure4_h1.3_fold_T'][1]<.1<r['figure4_h1.3_fold_T'][0]
assert r['figure4_h1.4_fold_T'][1]<0<r['figure4_h1.4_fold_T'][0]
# Figure5 barriers independent cubic root solution
for I,P in [(.5,3),(.5,1.3),(.42,3)]:
 all_roots=roots(I,P)
 assert len(all_roots)==3,(I,P,all_roots)
 lo,top,hi=all_roots
 assert d2F(lo,P)>0 and d2F(top,P)<0 and d2F(hi,P)>0
 r[f'figure5_I{I}_P{P}_barriers']={'low_to_high':round(F(top,I,P)-F(lo,I,P),8),'high_to_low':round(F(top,I,P)-F(hi,I,P),8)}
assert np.isclose(r['figure5_I0.5_P3_barriers']['low_to_high'],1/12,atol=1e-6)

# Factorial test of Fig4D; reproduce its model and alter a SINGLE parameter or a pair.
DT=.02; END=420;steps=round(END/DT)
def run4(t_cut,condition='original_both',T_post=None):
 s,d,b,g=.03,.05,.03,.45
 for j in range(steps):
  t=j*DT
  T=.9 if 40<=t<70 else .1
  h=1.3;w=.7
  if t>=t_cut:
   if condition in ('h_only','original_both'):h=0.
   if condition in ('T_only','original_both'):T=-.2
   if condition=='w_only':w=0
  ds=-s+sig(g*s+.3*b+w*d-.05)
  dd=-d+sig(h*d+.15*s+T)
  db=-b+s
  dg=.006*max(s-.3,0)
  s,d,b,g=s+DT*ds,d+DT/2*dd,b+DT/3*db,min(1.6,g+DT*dg)
 return [round(x,6) for x in (s,d,b,g)]
fac=[]
for cut in (120,300):
 for cond in ('none','h_only','T_only','w_only','original_both'):
  s,d,b,g=run4(cut,cond)
  fac.append(dict(intervention_time=cut,change=cond,final_s=s,final_d=d,final_b=b,final_g=g))
r['figure4_parameter_isolation']=fac
with open(DEST/'figure4_factorial_checks.csv','w',newline='') as file:
 z=csv.DictWriter(file,fieldnames=list(fac[0]));z.writeheader();z.writerows(fac)

# Dose-matched temporary schedules for Fig5. Neither is a model of real therapy.
SEED=319042; N=1200; TS=320.; STEP=.05; ST=round(TS/STEP)
DEES=(.004,.006,.008)
ARMS=('control','flatten_only','tilt_only','simultaneous_40','flatten_then_tilt','tilt_then_flatten')
base_root=roots(.5,3)[-1]
def params(t,arm):
 I=.5;P=3
 if arm=='flatten_only' and 80<=t<160:P=1.3
 elif arm=='tilt_only' and 80<=t<160:I=.42
 elif arm=='simultaneous_40' and 80<=t<120:I=.42;P=1.3
 elif arm=='flatten_then_tilt':
  if 80<=t<120:P=1.3
  elif 120<=t<160:I=.42
 elif arm=='tilt_then_flatten':
  if 80<=t<120:I=.42
  elif 120<=t<160:P=1.3
 return I,P
results=[]
for D in DEES:
 # common random numbers for paired between-condition stochastic comparison
 rng=np.random.default_rng(SEED+int(D*100000))
 S={a:np.full(N,base_root) for a in ARMS}
 crossed={a:np.zeros(N,dtype=bool) for a in ARMS}
 at160={}
 for j in range(ST):
  t=j*STEP
  noise=rng.standard_normal(N)*sqrt(2*D*STEP)
  for a in ARMS:
   I,P=params(t,a)
   x=S[a]
   x+= -dF(x,I,P)*STEP +noise
   crossed[a]|=x<.5
  if abs(t-160)<.025:
   at160={a:(S[a]<.5).mean() for a in ARMS}
 for a in ARMS:
  results.append(dict(D=D,condition=a,n=N,final_low_fraction=round(float((S[a]<.5).mean()),5),ever_low_fraction=round(float(crossed[a].mean()),5),at160_low_fraction=round(float(at160.get(a,np.nan)),5)))
r['figure5_ensemble']=results
with open(DEST/'figure5_dose_matched_ensemble.csv','w',newline='') as file:
 z=csv.DictWriter(file,fieldnames=list(results[0]));z.writeheader();z.writerows(results)

# summary figure of the dose-matched ensemble
fig,ax=plt.subplots(figsize=(9.4,4.6))
idx=np.arange(len(ARMS));w=.25
for j,D in enumerate(DEES):
 v=np.array([next(q['final_low_fraction'] for q in results if q['D']==D and q['condition']==a) for a in ARMS]);
 ax.bar(idx+(j-1)*w,100*v,w,label=f'D={D:.3f}')
ax.set_xticks(idx,['No change','Flatten only\n80 units','Tilt only\n80 units','Concurrent\n40 units each','Flatten → tilt\n40+40','Tilt → flatten\n40+40'])
ax.set_ylabel('Trajectories in low state at t=320 (%)')
ax.set_ylim(0,105)
ax.set_title('Unbiased stochastic ensemble, equal-duration sequential schedules (synthetic)')
ax.legend(frameon=False,ncol=3,loc='upper center')
ax.spines[['top','right']].set_visible(False)
fig.tight_layout()
fig.savefig(DEST/'figure5_dose_matched_ensemble.png',dpi=220)
plt.close(fig)
(DEST/'numerical_verification.json').write_text(json.dumps(r,indent=2))
print(json.dumps({k:v for k,v in r.items() if k!='figure5_ensemble'},indent=2))
print('FINAL DOSE-MATCHED ENSEMBLE')
for rr in results:print(rr)
