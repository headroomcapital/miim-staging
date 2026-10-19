import sys,glob; sys.path.insert(0,'.'); from common import *
def score(path, view):
    at,ab,mb,bg=np.load(f'matte_D{view}.npy')
    m=(blur((ab>0.05).astype(np.float32),10)>0.02)&(at<0.3)
    lab=rgb2lab(np.asarray(Image.open(path).convert('RGB').resize(ab.shape[::-1]),dtype=np.float32)/255)
    if 'brass' in path: bad=(lab[...,0]>82)&(np.hypot(lab[...,1],lab[...,2])<10)    # white/chrome inside brass
    else: bad=(lab[...,0]>90)                                                      # blown highlights on steel
    return bad[m].mean()*1000
if __name__=='__main__':
    for f in sorted(glob.glob(sys.argv[1])): v='Angle' if 'angle' in f else 'Frontal'; print(f'{score(f,v):7.2f}  {f.split("/")[-1]}')
