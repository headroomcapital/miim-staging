# Merge fal-repaired legs onto full-res close-ups with a TIGHT mask (no halo on the floor).
import sys,glob,os; sys.path.insert(0,'.'); from common import *
from fal_score import score as streak
def flecks(path,v):
    at,ab,mb,bg=np.load(f'matte_D{v}.npy'); L=rgb2lab(np.asarray(Image.open(path).convert('RGB'),dtype=np.float32)/255)[...,0]
    leg=ab>0.3; hp=L-blur(np.clip(L/100,0,1),4)*100; band=np.zeros_like(leg)
    for y in np.nonzero(leg.any(1))[0]:
        xs=np.nonzero(leg[y])[0]; band[y,max(xs.min()-8,0):xs.min()+25]=True
    return (np.abs(hp)[band&(at<0.3)]>6).mean()*1000
def score(p,v): return streak(p,v)+flecks(p,v)
T={'brass':rgb2lab(np.array([0x9A,0x82,0x67])/255.),'steel':rgb2lab(np.array([0x8F,0x8B,0x84])/255.)}
def dilate(m,r): return blur(m.astype(np.float32),r)>0.02
def tight_mask(base_lab,ab,at):
    leg=ab>0.3
    ring=dilate(leg,12)&~leg
    strip=ring&(base_lab[...,0]>80)&(np.hypot(base_lab[...,1],base_lab[...,2])<12)   # leftover white edge strips only
    m=(dilate(leg,1.5)|dilate(strip,1.5))&(at<0.3)
    return blur(m.astype(np.float32),1.2)
def ring_halo(img_lab,base_lab,ab):
    leg=ab>0.3; ring=dilate(leg,14)&~dilate(leg,3)
    return np.abs(img_lab[...,0]-base_lab[...,0])[ring].mean()
for f in sorted(glob.glob('fal_out/base/*-detail-*.png')):
    b=os.path.basename(f)[:-4]; v='Angle' if 'angle' in b else 'Frontal'; metal='brass' if 'brass' in b else 'steel'
    at,ab,mb,bg=np.load(f'matte_D{v}.npy')
    base=np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255; bl=rgb2lab(base)
    w=tight_mask(bl,ab,at)
    cands=[p for p in [f'fal_out/fix/{b}.png']+[f'fal_out/fix/{b}.try{k}.png' for k in range(7)] if os.path.exists(p)]
    best=None
    for c in cands:
        fix=np.asarray(Image.open(c).convert('RGB').resize(base.shape[1::-1],Image.LANCZOS),dtype=np.float32)/255
        lab=rgb2lab(base*(1-w[...,None])+fix*w[...,None])
        core=(ab>0.95)&(at<0.05); off=T[metal]-lab[core].mean(0); off[0]=np.clip(off[0],-4,4)
        lw=blur((ab>0.3).astype(np.float32),1.0)*(at<0.3)
        lab=lab+lw[...,None]*off
        out=(np.clip(lab2rgb(lab),0,1)*255+0.5).astype(np.uint8)
        tmp=f'out/{b}.png'; Image.fromarray(out).save(tmp); s=score(tmp,v)
        if best is None or s<best[0]: best=(s,out,c)
    Image.fromarray(best[1]).save(f'out/{b}.png')
    print(f'{b:38s} score {best[0]:5.2f}  halo ΔL {ring_halo(rgb2lab(best[1].astype(np.float32)/255),bl,ab):.2f}  from {os.path.basename(best[2])}')
