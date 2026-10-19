import sys,glob; sys.path.insert(0,'.'); from common import *
def measure(p):
    im=Image.open(p).convert('RGB'); im.thumbnail((1400,1400)); lab=rgb2lab(np.asarray(im,dtype=np.float32)/255); H_,W_=lab.shape[:2]
    top=(lab[...,2]<-25)&(np.hypot(lab[...,1],lab[...,2])>25); top=blur(top.astype(np.float32),2)>0.5
    rows=np.nonzero(top.sum(1)>W_*0.15)[0]
    if len(rows)==0: return None
    r0,r1=rows.min(),rows.max(); cols=np.nonzero(top[r0:r1+1].any(0))[0]; L=cols.max()-cols.min()
    band=lab[r1+8:r1+40]; warm=(band[...,2]>12)&(band[...,0]>35)&(np.hypot(band[...,1],band[...,2])>15)
    colw=warm.mean(0)>0.5; xs=np.nonzero(colw)[0]
    runs=np.split(xs,np.nonzero(np.diff(xs)>3)[0]+1) if len(xs) else []
    runs=[r for r in runs if len(r)>L*0.05]
    if len(runs)<2: return dict(L=L,legs=len(runs))
    d=np.mean([len(r) for r in runs[:2]]); c=[r.mean() for r in runs[:2]]
    return dict(diam_ratio=round(d/L,3), cc_ratio=round((c[1]-c[0])/L,3), thick_ratio=round((r1-r0)/L,3))
for p in sorted(glob.glob(sys.argv[1])): print(p.split('/')[-1], measure(p))
