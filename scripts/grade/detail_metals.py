# Give close-up metals the product-shot tonality: MIIM-II brass/aluminium brightness range + hue-vs-lightness curve.
import sys; sys.path.insert(0,'.'); from common import *
def ld(f): return np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255
q=np.linspace(0,1,257)
_,_,cII=np.load('matte_II.npy'); cII=cII>0.5
refs={}
for metal,ref in (('brass','brass'),('steel','aluminium')):
    r=rgb2lab(ld(f'out/miim-ii-stone-{ref}.jpg'))[cII]
    refs[metal]=(np.quantile(r[:,0],q),[np.polyfit(r[:,0],r[:,k],2) for k in (1,2)])
for view in ('Frontal','Angle'):
    at,ab,mb,bg=np.load(f'matte_D{view}.npy'); mb=mb>0.5
    for metal in ('brass','steel'):
        tq,fitR=refs[metal]
        src=rgb2lab(ld(f'out/miim-i-stone-{metal}-detail-{view.lower()}.png'))[mb]
        sq=np.quantile(src[:,0],q); fitS=[np.polyfit(src[:,0],src[:,k],2) for k in (1,2)]
        for c in COLORS:
            f=f'out/miim-i-{c}-{metal}-detail-{view.lower()}.png'; lab=rgb2lab(ld(f)); new=lab.copy()
            L=lab[...,0]; Ln=np.interp(L,sq,tq); new[...,0]=Ln
            for i,k in enumerate((1,2)): new[...,k]=lab[...,k]-np.polyval(fitS[i],L)+np.polyval(fitR[i],Ln)
            w=ab[...,None]; out=lab*(1-w)+new*w
            Image.fromarray((np.clip(lab2rgb(out),0,1)*255+0.5).astype(np.uint8)).save(f)
        x=rgb2lab(ld(f'out/miim-i-stone-{metal}-detail-{view.lower()}.png'))[mb]
        print(f'{view:7s} {metal:5s} L p5/50/95 {np.percentile(x[:,0],[5,50,95]).round(1)}  ref {np.interp([.05,.5,.95],q,tq).round(1)}  mean {hexs(lab2rgb(x.mean(0)))}')
