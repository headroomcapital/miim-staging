# House grade for Jochem's product set (Nov 2026). His MIIM-I and MIIM-II renders came out with
# different casts (MIIM-II aluminium reads red, its brass warmer and redder, floor lighter), so pull all 16
# to one shared target = the average of his own set (keeps his look, removes the drift):
#  1. background: per-row Lab offset so wall and floor hit the same grey in every image. It is applied to
#     the whole frame, so there is no halo around the table;
#  2. columns and tops: shift the region mean to the target, keeping the shading.
# Masks: columns = where the brass and aluminium renders of the same object differ (they are pixel-aligned);
# tops = where the four colour versions differ. Built at 1920 from his JPGs, reused at 4800 for the 4K PNGs.
# Writes out/v2g/<name>.jpg (1920 canonical) and, with --full, out/v2g-4k/<name>.png (responsive + wide source).
import sys,os; sys.path.insert(0,'.')
import numpy as np
from PIL import Image
from common import rgb2lab, lab2rgb
Image.MAX_IMAGE_PIXELS=None
S='/Users/headroom/Desktop/MIIM/site-jpg'; PNG={'i':S+'/bron-png-4k 2','ii':S+'/bron-png-4k'}
COLORS=['yellow','stone','cobalt','plum']; VER={('i','aluminium'):'v2',('i','brass'):'v2',('ii','aluminium'):'v3',('ii','brass'):'v2'}
FULL='--full' in sys.argv

def blurf(a,r):  # separable gaussian, float in / float out
    R=int(np.ceil(3*r)); k=np.exp(-0.5*(np.arange(-R,R+1)/r)**2); k/=k.sum(); a=a.astype(np.float32); p=len(k)//2
    a=np.apply_along_axis(lambda v:np.convolve(np.pad(v,p,mode='edge'),k,'valid'),0,a)
    return np.apply_along_axis(lambda v:np.convolve(np.pad(v,p,mode='edge'),k,'valid'),1,a).astype(np.float32)
def up(a,size): return np.asarray(Image.fromarray(a.astype(np.float32),mode='F').resize(size,Image.BILINEAR))
def load(p): return np.asarray(Image.open(p).convert('RGB'),dtype=np.float32)/255
def name(o,c,m): return f'miim-{o}-{c}-{m}-{VER[(o,m)]}'

items={}   # name -> dict(lab, masks, measurements)
for o in ['i','ii']:
    labs={(c,m):rgb2lab(load(f'{S}/{name(o,c,m)}.jpg')) for c in COLORS for m in ['aluminium','brass']}
    H,W=labs[('stone','brass')].shape[:2]
    d=np.abs(labs[('stone','aluminium')][...,2]-labs[('stone','brass')][...,2])
    colcore=blurf((d>9).astype(np.float32),6)>0.97
    near=lambda core,r=12: np.clip(blurf(core.astype(np.float32),r)*20,0,1)   # dilated region around a core
    col=np.clip(blurf(np.clip((d-4)/8,0,1)*near(colcore),1.5),0,1)            # no speckle out on the floor
    for m in ['aluminium','brass']:
        st=np.sqrt((np.stack([labs[(c,m)] for c in COLORS]).std(0)**2).sum(-1))
        core=st>np.percentile(st,99)*0.6
        at=np.clip(blurf(np.clip(st/np.median(st[core]),0,1),1.5)*1.3,0,1)
        at=at*(1-blurf(colcore.astype(np.float32),4))           # coloured reflections on the column are not top
        at=at*near(core&(at>0.95))
        topcore=core&(at>0.95)
        am=col*(1-at); mcore=colcore&(at<0.02)
        obj=blurf((topcore|colcore).astype(np.float32),40)>0.01
        prof=np.array([labs[('stone',m)][y][~obj[y],0].mean() if (~obj[y]).sum()>50 else np.nan for y in range(H)])
        ok=~np.isnan(prof); prof=np.interp(np.arange(H),np.arange(H)[ok],prof[ok])
        g=np.abs(np.convolve(prof,[1]*8+[-1]*8,'same')); g[:int(.15*H)]=0; g[int(.7*H):]=0; hz=int(g.argmax())
        sel=np.zeros(H); sel[hz:]=1; fw=blurf(np.tile(sel[:,None],(1,8)),12)[:,0]
        for c in COLORS:
            lab=labs[(c,m)]
            wr=slice(int(.03*H),hz-int(.04*H))
            wall=lab[wr][~obj[wr]].mean(0)
            fl=np.concatenate([lab[int(.86*H):int(.97*H),int(.02*W):int(.15*W)].reshape(-1,3),lab[int(.86*H):int(.97*H),int(.85*W):int(.98*W)].reshape(-1,3)]).mean(0)
            items[name(o,c,m)]=dict(o=o,c=c,m=m,lab=lab,at=at,am=am,fw=fw,hz=hz,wall=wall,floor=fl,
                                    metal=lab[mcore].mean(0),top=lab[topcore].mean(0),mcore=mcore,topcore=topcore)

def curve(lab,core,n=10):   # mean a,b per lightness band of the column core
    p=lab[core]; q=np.percentile(p[:,0],np.linspace(0,100,n+1)); c=[];
    for i in range(n):
        s_=p[(p[:,0]>=q[i])&(p[:,0]<=q[i+1])]; c.append(s_.mean(0))
    return np.array(c)                                     # n x (L,a,b)
def at_L(cv,L): return np.stack([np.interp(L,cv[:,0],cv[:,k]) for k in (1,2)],-1)
avg=lambda key,f=lambda it:True: np.mean([it[key] for it in items.values() if f(it)],0)
# Lightness = average of the set; colour (a*, b*) of the grey backdrop and the aluminium = MIIM-I's, because
# MIIM-II's read red next to it. Brass = average of both (MIIM-I's is greener, MIIM-II's redder).
isI=lambda it:it['o']=='i'
mix=lambda allv,refv: np.array([allv[0],refv[1],refv[2]])
WALL=mix(avg('wall'),avg('wall',isI)); FLOOR=mix(avg('floor'),avg('floor',isI))
FLOOR[1]=-0.5   # MIIM-I's floor (-1.0) reads faintly olive next to neutral aluminium
METAL={'aluminium':mix(avg('metal',lambda it:it['m']=='aluminium'),avg('metal',lambda it:it['m']=='aluminium' and isI(it))),
       'brass':avg('metal',lambda it:it['m']=='brass')}
TOP={c:avg('top',lambda it,c=c:it['c']==c) for c in COLORS}
# Column hue per lightness band. Aluminium = neutral at every L (Jochem's MIIM-I highlights lean green-yellow,
# MIIM-II's lean red); brass = the average band curve of all eight brass images.
ALU_AB=np.array([-0.3,3.0])
BRASS_CV=np.mean([curve(it['lab'],it['mcore']) for it in items.values() if it['m']=='brass'],0)
print('targets  wall',WALL.round(1),' floor',FLOOR.round(1),' alu',METAL['aluminium'].round(1),' brass',METAL['brass'].round(1))
print('         tops',{c:v.round(1).tolist() for c,v in TOP.items()})
os.makedirs('out/v2g',exist_ok=True); os.makedirs('out/v2g-4k',exist_ok=True)
for n,it in items.items():
    fw=it['fw']; rowoff=(1-fw)[:,None]*(WALL-it['wall'])+fw[:,None]*(FLOOR-it['floor'])
    lab=it['lab']+rowoff[:,None,:]
    dm=METAL[it['m']]-lab[it['mcore']].mean(0); dm[0]*=0.5   # half the L: darker tops really do reflect darker
    dt=TOP[it['c']]-lab[it['topcore']].mean(0)
    print(f"{n:30s} hz={it['hz']/lab.shape[0]:.3f} wall {np.round(WALL-it['wall'],1)} floor {np.round(FLOOR-it['floor'],1)} column {np.round(dm,1)} top {np.round(dt,1)}")
    cv=curve(lab,it['mcore'])
    def colfix(L):   # a,b shift for column pixels of lightness L (after the row offset)
        tgt=np.broadcast_to(ALU_AB,L.shape+(2,)) if it['m']=='aluminium' else at_L(BRASS_CV,L)
        return tgt-at_L(cv,L)
    dm=np.array([dm[0],0,0])
    def apply(lab,am,at,ro):
        lab=lab+ro[:,None,:]
        cf=np.concatenate([np.zeros(lab.shape[:2]+(1,),np.float32),colfix(lab[...,0])],-1)
        return lab+am[...,None]*(dm+cf)+at[...,None]*dt
    out=apply(it['lab'],it['am'],it['at'],rowoff)
    Image.fromarray((np.clip(lab2rgb(out),0,1)*255+0.5).astype(np.uint8)).save(f'out/v2g/{n}.jpg',quality=95)
    if FULL:
        big=load(f"{PNG[it['o']]}/{n}.png"); h,w=big.shape[:2]; H=lab.shape[0]
        ro=np.stack([np.interp(np.linspace(0,H-1,h),np.arange(H),rowoff[:,k]) for k in range(3)],-1).astype(np.float32)
        res=apply(rgb2lab(big),up(it['am'],(w,h)),up(it['at'],(w,h)),ro); del big
        Image.fromarray((np.clip(lab2rgb(res),0,1)*255+0.5).astype(np.uint8)).save(f'out/v2g-4k/{n}.png'); del res
