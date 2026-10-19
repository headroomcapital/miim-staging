# Straighten ragged left leg silhouettes in the close-ups. Works in edge-relative coordinates (u = x - edge(y))
# with sub-pixel interpolation, so there are no row-to-row steps.
import sys,glob; sys.path.insert(0,'.'); from leglib import *
B=14; D=45; SIG=22; U=np.arange(-3*B,D+2*B+1,dtype=np.float32)
def left_edge(leg,cd):
    rows=np.nonzero(leg.any(1))[0]; y0,y1=rows.min(),rows.max(); h=y1-y0
    ys=np.arange(int(y0+0.15*h),int(y1-0.25*h)); pts=[]
    for y in ys:
        xs=np.nonzero(leg[y])[0]; lo=max(xs.min()-60,0); seg=cd[y,lo:xs.min()+60]; hit=np.nonzero(seg>2)[0]
        if hit.size: pts.append((y,lo+hit[0]))
    p=np.array(pts); fit=np.polyfit(p[:,0],p[:,1],1)
    for _ in range(2):
        r=p[:,1]-np.polyval(fit,p[:,0]); keep=np.abs(r)<2.5*np.median(np.abs(r))+1; fit=np.polyfit(p[keep,0],p[keep,1],1)
    yend=y1
    for y in range(int(y0+0.5*h),y1):
        if cd[y,int(np.polyval(fit,y))+4]<=2: yend=y; break
    return fit,int(y0),yend
def sample(row,xs):                                    # linear interpolation along a row
    x0=np.clip(np.floor(xs).astype(int),0,len(row)-2); t=(xs-x0)[:,None]
    return row[x0]*(1-t)+row[x0+1]*t
g=np.exp(-np.arange(-3*SIG,3*SIG+1)**2/(2*SIG*SIG)); g/=g.sum()
cache={}
for f in sorted(glob.glob('out/*-detail-*.png')):
    b=f.split('/')[-1]; v='angle' if 'angle' in b else 'frontal'; V=v.capitalize()
    at,ab,mb,bg=np.load(f'matte_D{V}.npy')
    if v not in cache:
        src=lambda m:rgb2lab(np.asarray(Image.open(f"/Users/headroom/Desktop/MIIM/Batch06/MIIM_2Poot_Detail{V}_Blue{m}.png").convert('RGB').resize(ab.shape[::-1]),dtype=np.float32)/255)
        sv,bv=src('Silver'),src('Messing'); cd=np.hypot(sv[...,1]-bv[...,1],sv[...,2]-bv[...,2])
        cache[v]=[left_edge(m,cd) for m in sorted(legs(ab>0.5),key=lambda m:-m.sum())]
    img=np.asarray(Image.open(f).convert('RGB'),dtype=np.float32); out=img.copy(); W_=img.shape[1]
    for fit,y0,y1 in cache[v]:
        ys=np.array([y for y in range(y0,y1) if at[y,max(int(np.polyval(fit,y))-B,0):int(np.polyval(fit,y))+D].max()<0.3])
        if ys.size<6*SIG: continue
        E=np.polyval(fit,ys)
        R=np.stack([sample(img[y],e+U) for y,e in zip(ys,E)])            # rows resampled in edge coordinates
        new=R.copy()
        fl=R[:,np.searchsorted(U,-B)-1-np.arange(2*B)]                       # floor mirrored about u=-B
        lv=R[:,np.searchsorted(U,B)+np.arange(2*B)[::-1]]                    # leg mirrored about u=+B
        band=(U>=-B)&(U<B); u=U[band]
        alpha=np.clip(u+0.5,0,1)[None,:,None]; rim=(1-0.05*np.clip(1-u/B,0,1))[None,:,None]
        new[:,band]=fl[:,:band.sum()]*(1-alpha)+lv[:,:band.sum()]*rim*alpha
        leg_u=(U>=0)&(U<D)                                                    # smooth along the leg's length near the edge
        sm=np.stack([np.stack([np.convolve(np.pad(new[:,i,c],3*SIG,mode='reflect'),g,'valid') for c in range(3)],-1) for i in np.nonzero(leg_u)[0]],1)
        wu=np.clip((D-U[leg_u])/15,0,1)[None,:,None]
        new[:,leg_u]=new[:,leg_u]*(1-wu)+sm*wu
        fade=np.clip(np.minimum(ys-ys[0],ys[-1]-ys)/20,0,1)
        for j,(y,e) in enumerate(zip(ys,E)):                                 # write back to pixel grid
            xs=np.arange(int(np.floor(e-B)),int(np.ceil(e+D))); xs=xs[(xs>=0)&(xs<W_)]
            vals=np.stack([np.interp(xs-e,U,new[j,:,c]) for c in range(3)],-1)
            out[y,xs]=img[y,xs]*(1-fade[j])+vals*fade[j]
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(f); print('edge',b)
