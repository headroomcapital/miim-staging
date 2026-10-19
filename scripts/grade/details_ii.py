# Grade fal-generated MIIM-II close-ups to the house targets (same values as MIIM-I).
import sys; sys.path.insert(0,'.'); from common import *
TOP={'yellow':(86.9,-18.7,71.8),'stone':(84.3,0.7,8.0),'cobalt':(20.0,31.5,-50.2),'plum':(23.2,17.8,-0.1)}
BRASS=(55.3,4.7,18.4); SILVER=(58.1,0.4,3.9); FLOOR=np.array([67.0,0.2,4.4])
def ld(view,c,m): return np.asarray(Image.open(f'fal_out/ii/v2-{view}-{c}-{m}.png').convert('RGB').resize((2048,2048),Image.LANCZOS),dtype=np.float32)/255   # plain resize: ESRGAN bands smooth metal
for view in ('frontal','angle'):
    labs={(c,m):rgb2lab(ld(view,c,m)) for c in COLORS for m in ('aluminium','brass')}
    st=np.stack([labs[(c,'aluminium')] for c in COLORS]).std(0); st=np.sqrt((st**2).sum(-1))
    core=st>np.percentile(st,99)*0.6; at=np.clip(st/np.median(st[core]),0,1)
    at=blur((blur(at,3)>0.5).astype(np.float32),1.5)                              # clean solid tabletop matte
    coret=at>0.97
    d=np.hypot(labs[('stone','aluminium')][...,1]-labs[('stone','brass')][...,1],labs[('stone','aluminium')][...,2]-labs[('stone','brass')][...,2])
    legm=(blur((d>8).astype(np.float32),4)>0.5)&(at<0.05)                           # brass vs aluminium differ only on the leg
    # fill each row between the leg's outer edges: highlights are near-white in both metals and would otherwise fall out of the matte
    # extend each row outward from the leg core to the true silhouette: stop where the pixel matches the floor in both metals
    A,Bm=labs[('stone','aluminium')],labs[('stone','brass')]
    rows=np.nonzero(legm.sum(1)>20)[0]; solid=np.zeros_like(legm); W_=legm.shape[1]
    for y in rows:
        xs=np.nonzero(legm[y])[0]; lo,hi=int(np.percentile(xs,2)),int(np.percentile(xs,98))
        fl=np.concatenate([A[y,max(lo-120,0):max(lo-60,1)],A[y,min(hi+60,W_-2):min(hi+120,W_-1)]]).mean(0)
        def notfloor(x): return min(np.abs(A[y,x]-fl).max(),np.abs(Bm[y,x]-fl).max())>4.5
        while lo>0 and lo>min(xs.min(),int(np.percentile(xs,2)))-25 and notfloor(lo-1): lo-=1
        while hi<W_-1 and hi<max(xs.max(),int(np.percentile(xs,98)))+25 and notfloor(hi+1): hi+=1
        solid[y,lo:hi+1]=True
    legm=solid&(at<0.05)
    ab=blur(legm.astype(np.float32),1.5)*(1-at); mb=ab>0.97
    bg=(at<0.01)&(ab<0.01)&(blur(((at+ab)>0.01).astype(np.float32),40)<0.02)
    np.save(f'matte_IID{view}.npy',np.stack([at,ab,mb.astype(np.float32),bg.astype(np.float32)]))
    for c in COLORS:
        for mt in ('aluminium','brass'):
            lab=labs[(c,mt)]
            lab=lab+(FLOOR-lab[bg].mean(0))                                          # per image: fal variants drift slightly
            lab=lab+at[...,None]*(np.array(TOP[c])-lab[coret].mean(0))+ab[...,None]*(np.array(BRASS if mt=='brass' else SILVER)-lab[mb].mean(0))
            n=f"miim-ii-{c}-{mt}-detail-{view}.png"
            Image.fromarray((np.clip(lab2rgb(lab),0,1)*255+0.5).astype(np.uint8)).save(f'out/{n}')
            chk=rgb2lab(np.asarray(Image.open(f'out/{n}'),dtype=np.float32)/255)
            print(f"{n:44s} top {hexs(lab2rgb(chk[coret].mean(0)))} base {hexs(lab2rgb(chk[mb].mean(0)))} floor L{chk[bg][:,0].mean():.1f}")
    Image.fromarray((np.stack([at,ab,bg*0.4],-1)*255).astype(np.uint8)).resize((512,512)).save(f'fal_out/ii/mask-{view}.png')
