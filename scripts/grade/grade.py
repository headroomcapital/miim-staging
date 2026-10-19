import sys; sys.path.insert(0,'.'); from common import *
TOP={'yellow':(86.9,-18.7,71.8),'stone':(84.3,0.7,8.0),'cobalt':(20.0,31.5,-50.2),'plum':(23.2,17.8,-0.1)}
BRASS=(55.3,4.7,18.4); SILVER=(58.1,0.4,3.9)
HZ_TARGET=0.376

def prep_II(c,m):
    im=Image.fromarray((load_II(c,m)*255+0.5).astype(np.uint8)).resize((W,H),Image.LANCZOS)
    return np.asarray(im,dtype=np.float32)/255
def prep_I(c,m):
    im=Image.fromarray((load_I(c,m)*255+0.5).astype(np.uint8)); w,h=im.size
    t=(0.426-HZ_TARGET)/(1-HZ_TARGET); k=1-t
    im=im.crop((round((0.5-k/2)*w),round(t*h),round((0.5+k/2)*w),h)).resize((W,H),Image.LANCZOS)
    return np.asarray(im,dtype=np.float32)/255

def mattes(load,mats):
    labs={(c,m):rgb2lab(load(c,m)) for c in COLORS for m in mats}
    st=np.stack([labs[(c,mats[0])] for c in COLORS]).std(0); st=np.sqrt((st**2).sum(-1))
    core=st>np.percentile(st,99)*0.6
    at=np.clip(st/np.median(st[core]),0,1)
    d=labs[('stone',mats[0])]-labs[('stone',mats[1])]; d=np.sqrt((d**2).sum(-1))
    coreb=(d>np.median(d[d>5])*0.8)&(at<0.05)
    ab=np.clip(d/np.median(d[coreb]),0,1)*(1-at)
    return labs,at,ab,core&(at>0.95),coreb

def row_profile(lab,bgmask):
    prof=np.zeros((lab.shape[0],3)); 
    for y in range(lab.shape[0]):
        r=bgmask[y]; prof[y]=lab[y][r].mean(0) if r.sum()>50 else np.nan
    # fill nans, smooth
    for k in range(3):
        v=prof[:,k]; idx=np.arange(len(v)); ok=~np.isnan(v); v[~ok]=np.interp(idx[~ok],idx[ok],v[ok])
        prof[:,k]=np.convolve(np.pad(v,60,mode='edge'),np.ones(121)/121,'valid')
    return prof

REF=None
def run(name,load,mats):
    global REF
    labs,at,ab,coret,coreb=mattes(load,mats)
    bgm=(at<0.01)&(ab<0.01)
    # exclude shadow pools under the table from the profile
    prof=row_profile(labs[('stone',mats[0])],bgm&(blur((at+ab>0.01).astype(np.float32),40)<0.02))
    if REF is None: REF=prof
    off=(REF-prof)[:,None,:]
    np.save(f'matte_{name}.npy',np.stack([at,ab,coreb&(ab>0.95)]))
    for c in COLORS:
        for mt in mats:
            lab=labs[(c,mt)]+off
            t=np.array(TOP[c])-lab[coret].mean(0)
            mb=coreb&(ab>0.95); b=np.array(BRASS if mt=='brass' else SILVER)-lab[mb].mean(0)
            lab=lab+at[...,None]*t+ab[...,None]*b
            im=Image.fromarray((np.clip(lab2rgb(lab),0,1)*255+0.5).astype(np.uint8))
            n=f"miim-{name.lower()}-{c}-{mt}.jpg"; im.save(f'out/{n}',quality=92); print('wrote',n)

run('II',prep_II,('aluminium','brass'))
run('I',prep_I,('steel','brass'))
