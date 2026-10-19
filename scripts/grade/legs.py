import sys; sys.path.insert(0,'.'); from leglib import *
GRAIN=0.15
def ld(f): return np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255
atI,abI,_=np.load('matte_I.npy'); atII,abII,_=np.load('matte_II.npy')
legsI=legs(abI>0.5); legII=max(legs(abII>0.5),key=lambda m:m.sum())
print('MIIM-I legs found:',len(legsI),[int(m.sum()) for m in legsI])
for metal,ref in (('brass','brass'),('steel','aluminium')):
    refprof,_,_=profile(rgb2lab(ld(f'out/miim-ii-stone-{ref}.jpg')),legII)
    for c in COLORS:
        f=f'out/miim-i-{c}-{metal}.jpg'; lab=rgb2lab(ld(f)); out=lab.copy()
        for leg in legsI:
            own,xr,mid=profile(lab,leg)
            lowf=leg.astype(np.float32)
            low=lowpass(lab,lowf,14); fine=lowpass(lab,lowf,1.5)
            b=np.clip((np.nan_to_num(xr)*(BINS-1)).astype(int),0,BINS-1)
            colmean=own[b]                          # MIIM-I's own left-right profile at each pixel
            vert=low-colmean                        # keep MIIM-I top-to-bottom shading (top shadow, reflections)
            new=refprof[b]+vert+GRAIN*(lab-fine)    # MIIM-II cylinder profile + MIIM-I vertical + trace of grain
            w=(abI*leg)[...,None]
            out=out*(1-w)+new*w
        Image.fromarray((np.clip(lab2rgb(out),0,1)*255+0.5).astype(np.uint8)).save(f.replace('.jpg','.png'))
        print('legs',f)
