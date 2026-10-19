# Grade the four-table group shot to house values.
import sys; sys.path.insert(0,'.'); from common import *
TOP={'yellow':(86.9,-18.7,71.8),'stone':(84.3,0.7,8.0),'cobalt':(20.0,31.5,-50.2),'plum':(23.2,17.8,-0.1)}
BRASS=(55.3,4.7,18.4); WALL=(71.6,0.3,1.6); FLOOR=(67.0,0.2,4.4)
src=sys.argv[1]; out=sys.argv[2]
im=Image.open(src).convert('RGB'); W0,H0=im.size
lab=rgb2lab(np.asarray(im,dtype=np.float32)/255); L,a,b=lab[...,0],lab[...,1],lab[...,2]; C=np.hypot(a,b)
ys,xs=np.mgrid[0:H0,0:W0]/np.array([H0,W0])[:,None,None]
soft=lambda m:blur(blur(m.astype(np.float32),2)>0.5,1.5)
M={'yellow':soft((b>40)&(xs>0.5)),'cobalt':soft((b<-15)&(C>15)&(xs>0.5)&(ys<0.36)),'plum':soft((a>10)&(b<8)&(L<72)&(C>12)&(xs<0.50)&(ys<0.56)),
   'stone':soft((L>78)&(b>3)&(b<22)&(xs>0.15)&(xs<0.55)&(ys>0.2)&(ys<0.36))}
M['plum']=M['plum']*(1-M['cobalt'])
brass=soft((b>9)&(b<40)&(C>11)&(ys>0.3)&(L<85))
anyobj=np.clip(sum(M.values())+brass,0,1)
# backdrop: per-row profile of non-object pixels -> house wall/floor
bg=blur(anyobj,25)<0.02
prof=np.array([lab[y][bg[y]].mean(0) if bg[y].sum()>50 else np.nan*np.ones(3) for y in range(H0)])
for k in range(3):
    v=prof[:,k]; idx=np.arange(H0); ok=~np.isnan(v); v[~ok]=np.interp(idx[~ok],idx[ok],v[ok]); prof[:,k]=np.convolve(np.pad(v,60,mode='edge'),np.ones(121)/121,'valid')
g=np.abs(np.diff(prof[:,0])); hz=int(np.argmax(g[100:-100])+100)
t=np.clip((np.arange(H0)-(hz-40))/80,0,1)[:,None]
tgt=(1-t)*np.array(WALL)+t*np.array(FLOOR)
wall_mean=prof[:hz-60].mean(0); floor_mean=prof[hz+60:].mean(0)
off=(1-t)*(np.array(WALL)-wall_mean)+t*(np.array(FLOOR)-floor_mean)
lab=lab+off[:,None,:]
for k,m in M.items():
    core=m>0.95; mu=lab[core].mean(0); tg=np.array(TOP[k]); new=lab.copy()
    new[...,0]=lab[...,0]-mu[0]+tg[0]
    Cm=np.hypot(*lab[core][:,1:].T).mean(); Ct=np.hypot(tg[1],tg[2])
    if Ct>8:   # coloured top: force the house hue on every face (top and edge), keep relative saturation
        sc=np.clip(np.hypot(lab[...,1],lab[...,2])/max(Cm,1e-3),0.6,1.4)[...,None]
        new[...,1:]=tg[1:]*sc
    else:      # near-neutral stone: plain offset
        new[...,1:]=lab[...,1:]-mu[1:]+tg[1:]
    lab=lab*(1-m[...,None])+new*m[...,None]
core=brass>0.95; lab=lab+brass[...,None]*(np.array(BRASS)-lab[core].mean(0))
res=(np.clip(lab2rgb(lab),0,1)*255+0.5).astype(np.uint8)
Image.fromarray(res).save(out)
chk=rgb2lab(res.astype(np.float32)/255)
for k,m in list(M.items())+[('brass',brass)]: print(f'{k:7s} {hexs(lab2rgb(chk[m>0.95].mean(0)))}  px {int((m>0.95).sum())}')
print('horizon',hz/H0, 'wall L',chk[:int(hz*0.8)][bg[:int(hz*0.8)]][:,0].mean(),'floor L',chk[hz+100:][bg[hz+100:]][:,0].mean())
Image.fromarray((np.stack([M['yellow']+M['stone'],M['cobalt']+brass,M['plum']],-1).clip(0,1)*255).astype(np.uint8)).resize((1100,614)).save('fal_out/group-masks.png')
