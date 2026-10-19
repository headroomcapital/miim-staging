import sys; sys.path.insert(0,'.'); from common import *
def ld(f): return np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255
_,abI,coreI=np.load('matte_I.npy'); _,abII,coreII=np.load('matte_II.npy'); coreI=coreI>0.5; coreII=coreII>0.5
ref=rgb2lab(ld('out/miim-ii-stone-brass.jpg'))[coreII]
q=np.linspace(0,1,257); tq=np.quantile(ref[:,0],q)
fitII=[np.polyfit(ref[:,0],ref[:,k],2) for k in (1,2)]
src=rgb2lab(ld('out/miim-i-stone-brass.jpg'))[coreI]; sq=np.quantile(src[:,0],q)
fitI=[np.polyfit(src[:,0],src[:,k],2) for k in (1,2)]
for c in COLORS:
    f=f'out/miim-i-{c}-brass.jpg'; lab=rgb2lab(ld(f)); new=lab.copy()
    L=lab[...,0]; Ln=np.interp(L,sq,tq)
    new[...,0]=Ln
    for i,k in enumerate((1,2)): new[...,k]=lab[...,k]-np.polyval(fitI[i],L)+np.polyval(fitII[i],Ln)
    w=abI[...,None]; out=lab*(1-w)+new*w
    Image.fromarray((np.clip(lab2rgb(out),0,1)*255+0.5).astype(np.uint8)).save(f,quality=92); print('brass',f)
for n,core,fn in [('I',coreI,'out/miim-i-stone-brass.jpg'),('II',coreII,'out/miim-ii-stone-brass.jpg')]:
    x=rgb2lab(ld(fn))[core]; p=np.percentile(x[:,0],[5,50,95,99])
    print(f'{n} brass mean L{x[:,0].mean():.1f} a{x[:,1].mean():.1f} b{x[:,2].mean():.1f}  L p5/50/95/99 {p.round(1)}')
