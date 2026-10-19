import sys; sys.path.insert(0,'.'); from leglib import *
src,out=sys.argv[1],sys.argv[2]
# in-scene targets measured from the original backlit Archive render (studio values look fake here)
COBALT=np.array([40.2,2.5,-13.0]); BRASS=np.array([38.1,3.5,14.5]); TOP_L_SCALE=0.5
im=Image.open(src).convert('RGB'); im=im.resize((3072,3072),Image.LANCZOS)
lab=rgb2lab(np.asarray(im,dtype=np.float32)/255); H_,W_=lab.shape[:2]; L,a,b=lab[...,0],lab[...,1],lab[...,2]; C=np.hypot(a,b)
top=blur(((b<-22)&(C>22)&(L<55)).astype(np.float32),2)>0.5
rows=np.nonzero(top.sum(1)>W_*0.12)[0]; r0,r1=rows.min(),rows.max(); cols=np.nonzero(top[r0:r1+1].any(0))[0]; x0,x1=cols.min(),cols.max()
band=lab[r1+10:r1+60]; warm=(band[...,2]>8)&(band[...,0]>22)&(np.hypot(band[...,1],band[...,2])>9); colw=warm.mean(0)>0.5
legcols=np.zeros(W_,bool); legcols[x0:x1]=colw[x0:x1]
legcols=np.convolve(legcols,np.ones(9),'same')>4
leg=np.zeros((H_,W_),bool); leg[r1:,:]=legcols[None,:]
leg&=(b>5)&(L>20)&(C>7)
leg=blur(leg.astype(np.float32),4)>0.5
comps=legs(leg); leg=np.zeros_like(leg)
for c in comps:                                   # keep only blobs hanging from the tabletop (drop floor reflections)
    if np.nonzero(c.any(1))[0].min()<=r1+25: leg|=c
leg=blur(leg.astype(np.float32),3)>0.5
mt=blur(top.astype(np.float32),1.5); ml=blur(leg.astype(np.float32),1.5)*(1-mt)
ct=top&(blur(top.astype(np.float32),3)>0.99); cl=leg&(blur(leg.astype(np.float32),3)>0.99)
mu=lab[ct].mean(0); new=lab-mu+COBALT
new[...,0]=COBALT[0]+(lab[...,0]-mu[0])*TOP_L_SCALE          # calm fal's blotchy highlight on the top
lab2=lab*(1-mt[...,None])+new*mt[...,None]
lab2=lab2+ml[...,None]*(BRASS-lab2[cl].mean(0))
res=(np.clip(lab2rgb(lab2),0,1)*255+0.5).astype(np.uint8); Image.fromarray(res).save(out)
chk=rgb2lab(res.astype(np.float32)/255)
print('top',hexs(lab2rgb(chk[ct].mean(0))),'legs',hexs(lab2rgb(chk[cl].mean(0))),'leg cols',int(legcols.sum()),'top x',x0,x1)
Image.fromarray((np.stack([mt,ml,np.zeros_like(mt)],-1)*255).astype(np.uint8)).resize((768,768)).save('fal_out/home-mask.png')
