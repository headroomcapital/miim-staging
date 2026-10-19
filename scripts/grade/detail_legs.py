# Give close-up legs the main product photo's satin cylinder shading (mirrored: close-ups are lit from the left).
import sys; sys.path.insert(0,'.'); from leglib import *
GRAIN=0.15; VERT=0.4
def ld(f): return np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255
def width(leg):
    rows=np.nonzero(leg.any(1))[0]; y0,y1=rows.min(),rows.max(); h=y1-y0
    ys=range(int(y0+0.35*h),int(y1-0.2*h)); return np.median([np.ptp(np.nonzero(leg[y])[0]) for y in ys])
_,abII,_=np.load('matte_II.npy'); legII=max(legs(abII>0.5),key=lambda m:m.sum())
_,abI,_=np.load('matte_I.npy'); coreI=abI>0.95
main={m:rgb2lab(ld(f'out/miim-i-stone-{m}.png'))[coreI].mean(0) for m in ('brass','steel')}
refs={m:profile(rgb2lab(ld(f'out/miim-ii-stone-{r}.jpg')),legII)[0][::-1] for m,r in (('brass','brass'),('steel','aluminium'))}
def solid_leg(leg,at,cd=None):
    # Rebuild the full cylinder outline from geometry: reliable right edge, centre from the foot curve,
    # mirrored left edge, elliptical foot, top along the tabletop underside.
    H_,W_=leg.shape; rows=np.nonzero(leg.any(1))[0]; y0,y1=rows.min(),rows.max(); h=y1-y0
    if leg[:, -3:].any() or leg[:, :3].any(): return leg            # clipped by the frame: leave as is
    ys=np.arange(int(y0+0.35*h),int(y1-0.2*h))
    R=np.array([np.nonzero(leg[y])[0].max() for y in ys]); pr=np.polyfit(ys,R,1)
    cols=np.nonzero(leg.any(0))[0]; bot=np.array([np.nonzero(leg[:,x])[0].max() for x in cols])
    deep=bot>=np.percentile(bot,85); c=float(np.mean(cols[deep]))   # foot's lowest point = cylinder centre
    rmid=np.polyval(pr,ys.mean()); a=rmid-c                          # half width
    yy=np.arange(H_)[:,None]; xx=np.arange(W_)[None,:]
    r=np.polyval(pr,yy); l=r-2*a
    if cd is not None:                     # true left silhouette: where steel and brass renders differ in colour
        L=[]
        for y in ys:
            lo=int(np.polyval(pr,y)-2*a-80); seg=cd[y,max(lo,0):int(c)]
            hit=np.nonzero(seg>2)[0]
            if hit.size: L.append((y,max(lo,0)+hit[0]))
        if len(L)>20:
            Ly=np.array(L); pl=np.polyfit(Ly[:,0],Ly[:,1],1); l=np.polyval(pl,yy)-1
    # foot: ellipse y = yc + b*sqrt(1-((x-c)/a)^2) fitted on columns we trust (right half)
    ok=(cols>c)&(cols<c+0.9*a); u=np.sqrt(np.clip(1-((cols[ok]-c)/a)**2,0,1))
    A=np.stack([np.ones(ok.sum()),u],1); yc,b=np.linalg.lstsq(A,bot[ok],rcond=None)[0]
    foot=yc+b*np.sqrt(np.clip(1-((xx-c)/a)**2,0,1))
    under=at>0.5; top=np.where(under.any(0),H_-np.argmax(under[::-1],0),0)[None,:]   # just below the tabletop
    top=np.maximum(top,y0)
    return (xx>=l)&(xx<=r)&(yy<=foot)&(yy>=top)
for view in ('frontal','angle'):
    at,ab,mb,bg=np.load(f'matte_D{view.capitalize()}.npy')
    src=lambda m:rgb2lab(np.asarray(Image.open(f"/Users/headroom/Desktop/MIIM/Batch06/MIIM_2Poot_Detail{view.capitalize()}_Blue{m}.png").convert('RGB').resize(ab.shape[::-1]),dtype=np.float32)/255)
    sv,bv=src('Silver'),src('Messing'); cd=np.hypot(sv[...,1]-bv[...,1],sv[...,2]-bv[...,2])
    found=sorted(legs(ab>0.5),key=lambda m:-m.sum()); found=[solid_leg(m,at,cd) for m in found]; wref=width(found[0])
    print(view,'legs',[int(m.sum()) for m in found],'ref width',int(wref))
    for metal in ('brass','steel'):
        for c in COLORS:
            f=f'out/miim-i-{c}-{metal}-detail-{view}.png'; lab=rgb2lab(ld(f)); out=lab.copy()
            for leg in found:
                own,xr,mid=profile(lab,leg,wref)
                low=lowpass(lab,leg.astype(np.float32),14); fine=lowpass(lab,leg.astype(np.float32),1.5)
                b=np.clip((np.nan_to_num(xr)*(BINS-1)).astype(int),0,BINS-1)
                # top-to-bottom lighting only: one value per row, averaged across the leg (no sideways reflections)
                d=np.where(leg[...,None],low-own[b],0); n=np.maximum(leg.sum(1),1)[:,None]
                vrow=d.sum(1)/n; vrow=np.concatenate([vrow[:1].repeat(0,0),vrow]) if False else vrow
                vrow=np.stack([np.convolve(np.pad(vrow[:,k],20,mode='edge'),np.ones(41)/41,'valid') for k in range(3)],-1)
                new=refs[metal][b]+VERT*vrow[:,None,:]+GRAIN*(lab-fine)
                core=(ab>0.95)&leg; new=new-new[core].mean(0)+main[metal]   # same average as the main photo's legs
                grown=blur(leg.astype(np.float32),1.5)>0.05                     # include the soft edge pixels
                w=(np.clip(ab*1.6,0,1)*grown)[...,None]; out=out*(1-w)+new*w
            Image.fromarray((np.clip(lab2rgb(out),0,1)*255+0.5).astype(np.uint8)).save(f)
        x=rgb2lab(ld(f'out/miim-i-stone-{metal}-detail-{view}.png'))[ab>0.95]
        print(f'  {view} {metal}: leg mean {hexs(lab2rgb(x.mean(0)))}  main {hexs(lab2rgb(main[metal]))}')
