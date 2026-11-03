# Object mask from sharp silhouette edges (soft shadows and floor gradients fall below the threshold).
import numpy as np
from common import blur
def find_obj(lab, thr=0.012):
    L=blur(lab[...,0]/100,2); gy,gx=np.gradient(L); e=np.abs(gx)>thr   # |gx| only: the wall/floor horizon is horizontal
    H,W=e.shape; o=np.zeros_like(e)
    for y in range(H):
        xs=np.nonzero(e[y])[0]
        if len(xs)>=4: o[y,xs[0]:xs[-1]+1]=True
    return blur(o.astype(np.float32),20)>0.1
