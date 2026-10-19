# Retry fal repair on images that still score badly; keep the best version.
import sys,os,shutil,subprocess; sys.path.insert(0,'.'); from fal_score import *
b=sys.argv[1]; f=f'out/{b}.png'; v='Angle' if 'angle' in b else 'Frontal'; metal='brass' if 'brass' in b else 'steel'
best=score(f,v); shutil.copy(f,f'fal_out/fix/{b}.best.png')
for k in range(3):
    if best<5: break
    tmp=f'fal_out/fix/{b}.try{k}.png'
    r=subprocess.run(['python3','fal_fix.py',f'fal_out/fix/{b}.best.png',tmp,metal,'fal-ai/nano-banana/edit'],capture_output=True,text=True)
    if r.returncode: continue
    at,ab,mb,bg=np.load(f'matte_D{v}.npy')
    m=blur(((ab>0.05)).astype(np.float32),10)>0.02; m=blur(m.astype(np.float32)*(at<0.3),3)
    base=np.asarray(Image.open(f'fal_out/fix/{b}.best.png').convert('RGB'),dtype=np.float32)
    fix=np.asarray(Image.open(tmp).convert('RGB').resize(base.shape[1::-1],Image.LANCZOS),dtype=np.float32)
    cand=f'fal_out/fix/{b}.cand.png'; Image.fromarray((base*(1-m[...,None])+fix*m[...,None]).clip(0,255).astype(np.uint8)).save(cand)
    s=score(cand,v)
    if s<best: best=s; shutil.copy(cand,f'fal_out/fix/{b}.best.png')
shutil.copy(f'fal_out/fix/{b}.best.png',f); print(f'{best:6.2f} {b}')
