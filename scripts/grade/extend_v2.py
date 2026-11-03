# Wide hero variants (2.4:1) for Jochem's Nov 2026 product set.
# The tables fill more of the frame than the old renders, so the clean edge strip is too narrow to
# mirror (repeats + mirrored shadow edges). Instead: smooth backdrop eases from the edge colour to the
# room's row-average, and the grain comes from the photo's own full-width clean wall rows (above the
# table) and floor rows (below the columns), so it never repeats across the extension.
# Object matte = union of silhouette-edge masks over each object's 8 images (objmask_v2.py).
import sys; sys.path.insert(0,'.')
from common import *
import numpy as np; from PIL import Image
ASPECT=2.4; FALL=500; R_LOW=40; XF=80
def ld(f): return np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255
def vblur(a,r):
    k=np.exp(-np.arange(-3*r,3*r+1)**2/(2*r*r)); k/=k.sum()
    return np.stack([np.convolve(np.pad(a[:,c],3*r,mode='reflect'),k,'valid') for c in range(a.shape[1])],-1)
def blur2(a,r):
    k=np.exp(-np.arange(-3*r,3*r+1)**2/(2*r*r)); k/=k.sum(); n=3*r
    a=np.pad(a,n,mode='reflect')
    a=np.apply_along_axis(lambda v:np.convolve(v,k,'valid'),0,a)
    return np.apply_along_axis(lambda v:np.convolve(v,k,'valid'),1,a)
def synth(patch,shape,rng):
    # random-phase texture with the patch's own spectrum: same grain and mottling, no repeated marks
    h,w=shape; out=np.zeros((h,w,3),np.float32)
    ph=np.exp(2j*np.pi*rng.random((h,w)))
    for c in range(3):
        A=np.abs(np.fft.fftshift(np.fft.fft2(patch[...,c]-patch[...,c].mean())))
        A=np.asarray(Image.fromarray(A.astype(np.float32)).resize((w,h),Image.BILINEAR))
        t=np.real(np.fft.ifft2(np.fft.ifftshift(A*ph))); out[...,c]=t/(t.std()+1e-6)*patch[...,c].std()*(1 if c==0 else 0.35)  # keep chroma grain faint: random a/b reads as blotches
    return out
def mirror_idx(n,m): j=np.arange(n)%(2*m); return np.where(j<m,j,2*m-1-j)
def extend(f):
    rng=np.random.default_rng(7)
    lab=rgb2lab(ld(f)); H,W=lab.shape[:2]; p=(round(H*ASPECT)-W)//2
    obj=np.load('matte_I_v2.npy' if '/miim-i-' in f else 'matte_II_v2.npy')
    rows=np.nonzero(obj.any(1))[0]; cols=np.nonzero(obj.any(0))[0]
    bg=~obj; tgt=np.array([lab[y][bg[y]].mean(0) if bg[y].any() else lab[y].mean(0) for y in range(H)])
    g=np.abs(np.diff(np.convolve(tgt[:,0],np.ones(9)/9,'same'))); hz=int(np.argmax(g[50:-50])+50)+1
    tgt=np.concatenate([vblur(tgt[:hz],30),vblur(tgt[hz:],30)],0); tgt=vblur(tgt,R_LOW//2)
    low=np.stack([blur2(lab[...,c],R_LOW) for c in range(3)],-1); det=lab-low   # grain + mottling
    wt=max(rows.min()-30,60); fb=min(rows.max()+30,H-60)
    wall_src=det[30:wt]; floor_src=det[fb:H-10]
    out=np.zeros((H,W+2*p,3),np.float32); out[:,p:p+W]=lab
    for side in ('L','R'):
        edge=low[:,0] if side=='L' else low[:,-1]
        dx=np.arange(p)[None,:,None]; fall=1-np.exp(-dx/FALL)
        base=edge[:,None,:]*(1-fall)+tgt[:,None,:]*fall
        tex=np.concatenate([synth(wall_src,(hz,p),rng),synth(floor_src,(H-hz,p),rng)],0)
        bw=int(min(XF, (cols.min() if side=='L' else W-cols.max())-10))
        band=det[:,:bw] if side=='L' else det[:,W-bw:][:,::-1]
        near=band[:,mirror_idx(p,bw)]; w=np.clip(1-dx/XF,0,1)                      # cross-fade from the edge's own grain
        ext=base+near*w+tex*(1-w)
        if side=='L': out[:,:p]=ext[:,::-1]
        else: out[:,p+W:]=ext
    o=f.rsplit('.',1)[0]+'-wide.png'
    Image.fromarray((np.clip(lab2rgb(out),0,1)*255+0.5).astype(np.uint8)).save(o); return o,hz,wt,fb
for f in sys.argv[1:]: print(*extend(f))
