import numpy as np
from PIL import Image, ImageFilter
IMG='/Users/headroom/Desktop/claude/miim-v2/public/images'
SRC_I='/Users/headroom/Desktop/MIIM/MIIM-I_product_originals'
B04='/Users/headroom/Desktop/MIIM/MIIM_Batch04'
W,H=2000,1406
COLORS=['yellow','stone','cobalt','plum']
SRC04={'yellow':'Yellow','stone':'Taupe','cobalt':'Blue','plum':'Purple'}
def load_I(c,m): return np.asarray(Image.open(f'{SRC_I}/miim-i-{c}-{m}.jpg').convert('RGB'),dtype=np.float32)/255
def load_II(c,m):
    f=f"{B04}/MIIM_1Poot_{SRC04[c]}{'Alu' if m=='aluminium' else 'Messing'}.png"
    return np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255
def s2l(c): return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
def l2s(c): c=np.clip(c,0,1); return np.where(c<=0.0031308,c*12.92,1.055*c**(1/2.4)-0.055)
M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]]); Mi=np.linalg.inv(M)
WP=np.array([0.95047,1.0,1.08883])
def f(t): return np.where(t>0.008856,np.cbrt(t),7.787*t+16/116)
def fi(t): return np.where(t>0.206893,t**3,(t-16/116)/7.787)
def rgb2lab(rgb):
    xyz=s2l(rgb)@M.T/WP; fx,fy,fz=f(xyz[...,0]),f(xyz[...,1]),f(xyz[...,2])
    return np.stack([116*fy-16,500*(fx-fy),200*(fy-fz)],-1)
def lab2rgb(lab):
    fy=(lab[...,0]+16)/116; fx=fy+lab[...,1]/500; fz=fy-lab[...,2]/200
    xyz=np.stack([fi(fx),fi(fy),fi(fz)],-1)*WP
    return l2s(xyz@Mi.T)
def blur(mask,r):
    im=Image.fromarray((np.clip(mask,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))
    return np.asarray(im,dtype=np.float32)/255
def masks(load,mats):
    a,b=mats
    stack=np.stack([load(c,a) for c in COLORS])
    top=(stack.std(0).max(-1)>0.06).astype(np.float32)
    # erode-ish: blur then threshold keeps solid area, then feather
    top=(blur(top,3)>0.9).astype(np.float32)
    base=(np.abs(load('stone',a)-load('stone',b)).max(-1)>0.05).astype(np.float32)
    base=(blur(base,3)>0.9).astype(np.float32)*(1-top)
    bg=(1-np.clip(blur(top+base,12)*4,0,1))
    return top,base,bg
def hexs(rgb): return '#'+''.join(f'{int(round(x*255)):02x}' for x in np.clip(rgb,0,1))
def stats(img,mask):
    lab=rgb2lab(img); w=mask>0.5
    return lab[w].mean(0), lab[w].std(0)
