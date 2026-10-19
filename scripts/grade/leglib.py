import sys; sys.path.insert(0,'.'); from common import *
BINS=200
def legs(mask):
    # label connected components (two legs) by flood fill on a coarse grid
    m=mask.copy(); lab=np.zeros(m.shape,np.int32); n=0
    ys,xs=np.nonzero(m)
    for y0,x0 in zip(ys[::997],xs[::997]):
        if lab[y0,x0]: continue
        n+=1; stack=[(y0,x0)]
        while stack:
            y,x=stack.pop()
            if y<0 or x<0 or y>=m.shape[0] or x>=m.shape[1] or not m[y,x] or lab[y,x]: continue
            # scanline fill
            l=x
            while l>0 and m[y,l-1] and not lab[y,l-1]: l-=1
            r=x
            while r<m.shape[1]-1 and m[y,r+1] and not lab[y,r+1]: r+=1
            lab[y,l:r+1]=n
            for yy in (y-1,y+1):
                if 0<=yy<m.shape[0]:
                    seg=np.nonzero(m[yy,l:r+1]&(lab[yy,l:r+1]==0))[0]
                    for s in seg[::8]: stack.append((yy,l+s))
    return [lab==i for i in range(1,n+1) if (lab==i).sum()>5000]
def xrel(leg,ref_width=None):
    # fit straight left/right silhouette edges through the unobstructed middle of the leg
    rows=np.nonzero(leg.any(1))[0]; y0,y1=rows.min(),rows.max(); h=y1-y0
    ys=np.arange(int(y0+0.35*h),int(y1-0.2*h))
    L=np.array([np.nonzero(leg[y])[0].min() for y in ys]); R=np.array([np.nonzero(leg[y])[0].max() for y in ys])
    pl,pr=np.polyfit(ys,L,1),np.polyfit(ys,R,1)
    yy=np.arange(leg.shape[0])[:,None]; xx=np.arange(leg.shape[1])[None,:]
    l=np.polyval(pl,yy); r=np.polyval(pr,yy)
    W_=leg.shape[1]
    if ref_width and R.max()>=W_-3: r=l+ref_width          # clipped on the right edge
    if ref_width and L.min()<=2: l=r-ref_width             # clipped on the left edge
    xr=np.clip((xx-l)/(r-l),0,1).astype(np.float32)
    return np.where(leg,xr,np.nan)
def profile(lab,leg,ref_width=None):
    xr=xrel(leg,ref_width); rows=np.nonzero(leg.any(1))[0]; y0,y1=rows.min(),rows.max(); h=y1-y0
    mid=np.zeros(leg.shape,bool); mid[int(y0+0.12*h):int(y1-0.15*h)]=True
    sel=leg&mid&~np.isnan(xr); b=np.clip((xr[sel]*(BINS-1)).astype(int),0,BINS-1)
    prof=np.stack([np.bincount(b,lab[sel][:,k],BINS)/np.maximum(np.bincount(b,None,BINS),1) for k in range(3)],-1)
    # median-filter to drop the seam, then light smoothing
    pad=np.pad(prof,((3,3),(0,0)),mode='edge'); prof=np.stack([np.median(pad[i:i+7],0) for i in range(BINS)])
    pad=np.pad(prof,((4,4),(0,0)),mode='edge'); prof=np.stack([pad[i:i+9].mean(0) for i in range(BINS)])
    return prof,xr,mid
def gblur(a,r):
    k=int(3*r)+1; x=np.arange(-k,k+1); g=np.exp(-x**2/(2*r*r)); g/=g.sum()
    a=np.apply_along_axis(lambda v:np.convolve(v,g,'same'),0,a) if a.ndim==2 else a
    return np.apply_along_axis(lambda v:np.convolve(v,g,'same'),1,a)
def lowpass(arr,mask,r):
    ys,xs=np.nonzero(mask); y0,y1,x0,x1=max(ys.min()-60,0),ys.max()+60,max(xs.min()-60,0),xs.max()+60
    sub=(slice(y0,y1),slice(x0,x1)); m=mask[sub]
    den=gblur(m,r); out=arr.copy()
    for k in range(3): out[sub+(k,)]=gblur(arr[sub+(k,)]*m,r)/np.maximum(den,1e-4)
    return out
