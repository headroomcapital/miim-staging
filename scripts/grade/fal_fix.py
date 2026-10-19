import os, sys, json, base64, subprocess, tempfile
from PIL import Image
def uri(p): return 'data:image/jpeg;base64,'+base64.b64encode(open(p,'rb').read()).decode()
def call(model, payload, out):
    with tempfile.NamedTemporaryFile(suffix='.json',delete=False) as tf: tf.write(json.dumps(payload).encode())
    r=subprocess.run(['curl','-sS','--max-time','400','-X','POST',f'https://fal.run/{model}','-H',f"Authorization: Key {os.environ['FAL_KEY']}",
                      '-H','Content-Type: application/json','--data-binary','@'+tf.name],capture_output=True,text=True); os.unlink(tf.name)
    res=json.loads(r.stdout); imgs=res.get('images')
    if not imgs: raise SystemExit(f'{model} ERR {json.dumps(res)[:300]}')
    subprocess.run(['curl','-sS','-o',out,imgs[0]['url']],check=True); return out
PROMPT=("Retouch only the metal cylinder legs. Remove the rendering artifacts: the thin bright white mirror-like strip running down the "
        "left edge of the front leg, and the broken white streaks and smears on the leg at the back right. Each leg must read as one "
        "clean, continuous satin brushed {mat} cylinder with smooth vertical shading and a crisp outline, consistent with the rest of that leg. "
        "Do not change anything else: same tabletop shape, colour and corners, same floor, shadows, lighting, camera and framing.")
if __name__=='__main__':
    src,out,metal,model=sys.argv[1:5]
    tmp=out+'.in.jpg'; Image.open(src).convert('RGB').resize((1536,1536),Image.LANCZOS).save(tmp,quality=94)
    mat='stainless steel' if metal=='steel' else 'champagne brass'
    p={'prompt':PROMPT.format(mat=mat),'image_urls':[uri(tmp)],'num_images':1,'output_format':'png'}
    if 'seedream' in model: p.pop('output_format'); p['image_size']={'width':2048,'height':2048}
    print(call(model,p,out)); os.unlink(tmp)
