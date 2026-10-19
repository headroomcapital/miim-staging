import sys; sys.path.insert(0,'.'); from common import *
TOP={'yellow':(86.9,-18.7,71.8),'stone':(84.3,0.7,8.0),'cobalt':(20.0,31.5,-50.2),'plum':(23.2,17.8,-0.1)}
BRASS=(55.3,4.7,18.4); SILVER=(58.1,0.4,3.9); FLOOR=np.array([67.0,0.2,4.4])
B06='/Users/headroom/Desktop/MIIM/Batch06'; SRC={'yellow':'Yellow','stone':'Taupe','cobalt':'Blue','plum':'Purple'}
S=2000
def ld(view,c,m):
    f=f"{B06}/MIIM_2Poot_Detail{view}_{SRC[c]}{'Messing' if m=='brass' else 'Silver'}.png"
    return np.asarray(Image.open(f).convert('RGB').resize((S,S),Image.LANCZOS),dtype=np.float32)/255
for view in ('Frontal','Angle'):
    labs={(c,m):rgb2lab(ld(view,c,m)) for c in COLORS for m in ('steel','brass')}
    st=np.stack([labs[(c,'steel')] for c in COLORS]).std(0); st=np.sqrt((st**2).sum(-1))
    core=st>np.percentile(st,99)*0.6; at=np.clip(st/np.median(st[core]),0,1); coret=core&(at>0.95)
    d=labs[('stone','steel')]-labs[('stone','brass')]; d=np.sqrt((d**2).sum(-1))
    coreb=(d>np.median(d[d>5])*0.8)&(at<0.05); ab=np.clip(d/np.median(d[coreb]),0,1)*(1-at); mb=coreb&(ab>0.95)
    bg=(at<0.01)&(ab<0.01)&(blur(((at+ab)>0.01).astype(np.float32),40)<0.02)
    off=FLOOR-labs[('stone','steel')][bg].mean(0)
    np.save(f'matte_D{view}.npy',np.stack([at,ab,mb.astype(np.float32),bg.astype(np.float32)]))
    for c in COLORS:
        for mt in ('steel','brass'):
            lab=labs[(c,mt)]+off
            lab=lab+at[...,None]*(np.array(TOP[c])-lab[coret].mean(0))+ab[...,None]*(np.array(BRASS if mt=='brass' else SILVER)-lab[mb].mean(0))
            n=f"miim-i-{c}-{mt}-detail-{view.lower()}.jpg"
            Image.fromarray((np.clip(lab2rgb(lab),0,1)*255+0.5).astype(np.uint8)).save(f'out/{n}'.replace('.jpg','.png'))
            chk=rgb2lab(np.asarray(Image.open(f'out/{n}'.replace('.jpg','.png')),dtype=np.float32)/255)
            print(f"{n:42s} top {hexs(lab2rgb(chk[coret].mean(0)))} base {hexs(lab2rgb(chk[mb].mean(0)))} floor L{chk[bg][:,0].mean():.1f}")
