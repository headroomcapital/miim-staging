# Wide hero variants: extend the studio backdrop left/right (table untouched) to ~2.4:1.
# Texture = the photo's own clean backdrop strip, mirrored outward (seamless at the edge);
# broad brightness eases from the edge colour toward the room's average backdrop.
import sys; sys.path.insert(0,'.'); from leglib import *
ASPECT=2.4; R_LOW=40; FALL=350; MAXBAND=260
def ld(f): return np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255
def vblur(a,r):
    k=np.exp(-np.arange(-3*r,3*r+1)**2/(2*r*r)); k/=k.sum()
    return np.stack([np.convolve(np.pad(a[:,c],3*r,mode='reflect'),k,'valid') for c in range(a.shape[1])],-1)
def blur2(a,r):
    k=np.exp(-np.arange(-3*r,3*r+1)**2/(2*r*r)); k/=k.sum(); n=3*r
    a=np.pad(a,n,mode='edge')
    a=np.apply_along_axis(lambda v:np.convolve(v,k,'valid'),0,a)
    return np.apply_along_axis(lambda v:np.convolve(v,k,'valid'),1,a)
def pingpong(n,bw):
    j=np.arange(n)%(2*bw); return np.where(j<bw,j,2*bw-1-j)
def extend(f):
    lab=rgb2lab(ld(f)); H_,W_=lab.shape[:2]; p=(round(H_*ASPECT)-W_)//2
    at,ab=np.load('matte_I.npy' if '/miim-i-' in f else 'matte_II.npy')[:2]
    obj=blur(((at+ab)>0.01).astype(np.float32),40)>0.02
    cols=np.nonzero(obj.any(0))[0]
    bwL=int(min(MAXBAND,cols.min()-20)); bwR=int(min(MAXBAND,W_-cols.max()-20))
    # room-average backdrop per row (wall/floor smoothed separately), then blurred like the low-pass layer
    bg=~obj; tgt=np.array([lab[y][bg[y]].mean(0) for y in range(H_)])
    g=np.abs(np.diff(np.convolve(tgt[:,0],np.ones(9)/9,'same'))); hz=int(np.argmax(g[50:-50])+50)+1
    tgt=np.concatenate([vblur(tgt[:hz],30),vblur(tgt[hz:],30)],0); tgt=vblur(tgt,R_LOW)
    out=np.zeros((H_,W_+2*p,3),np.float32); out[:,p:p+W_]=lab
    for name,bw in (('L',bwL),('R',bwR)):
        band=lab[:,:bw] if name=='L' else lab[:,W_-bw:][:,::-1]    # index 0 = the image edge column
        low=np.stack([blur2(band[...,c],R_LOW) for c in range(3)],-1)
        mid6=np.stack([blur2(band[...,c],6) for c in range(3)],-1)
        fine=band-mid6; mid=mid6-low; edge_low=low[:,0]          # grain repeats invisibly; blotches only near the seam
        idx=pingpong(p,bw); dx=np.arange(p)[None,:,None]; fall=1-np.exp(-dx/FALL)
        smooth_edge=np.concatenate([vblur(edge_low[:hz],45),vblur(edge_low[hz:],45)],0)
        near=np.exp(-dx/120)                                     # edge blotches fade out instead of streaking sideways
        base=(smooth_edge[:,None,:]+(edge_low-smooth_edge)[:,None,:]*near)
        ext=base*(1-fall)+tgt[:,None,:]*fall+fine[:,idx]+mid[:,idx]*near
        if name=='L': out[:,:p]=ext[:,::-1]
        else: out[:,p+W_:]=ext
    o=f.rsplit('.',1)[0]+'-wide.png'
    Image.fromarray((np.clip(lab2rgb(out),0,1)*255+0.5).astype(np.uint8)).save(o); return o,bwL,bwR
files=[f'out/miim-i-{c}-{m}.png' for c in COLORS for m in ('steel','brass')]+[f'out/miim-ii-{c}-{m}.jpg' for c in COLORS for m in ('aluminium','brass')]
for f in (sys.argv[1:] or files): print(*extend(f))
