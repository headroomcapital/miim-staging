# Generate MIIM-II close-ups with fal nano-banana from the MIIM-II render + a MIIM-I close-up as framing reference.
import os, sys, json, base64, subprocess, tempfile
from PIL import Image
def uri(p):
    t=tempfile.mktemp(suffix='.jpg'); im=Image.open(p).convert('RGB'); im.thumbnail((1536,1536)); im.save(t,quality=93)
    d='data:image/jpeg;base64,'+base64.b64encode(open(t,'rb').read()).decode(); os.unlink(t); return d
def call(model,payload,out):
    with tempfile.NamedTemporaryFile(suffix='.json',delete=False) as tf: tf.write(json.dumps(payload).encode())
    r=subprocess.run(['curl','-sS','--max-time','400','-X','POST',f'https://fal.run/{model}','-H',f"Authorization: Key {os.environ['FAL_KEY']}",
                      '-H','Content-Type: application/json','--data-binary','@'+tf.name],capture_output=True,text=True); os.unlink(tf.name)
    res=json.loads(r.stdout); imgs=res.get('images') or ([res['image']] if 'image' in res else None)
    if not imgs: raise SystemExit(f'ERR {json.dumps(res)[:300]}')
    subprocess.run(['curl','-sS','-o',out,imgs[0]['url']],check=True); return out
VIEW={
 'frontal':"a straight-on, eye-level close-up of the front edge of the tabletop and the single cylindrical leg below it, the leg centred, the tabletop edge running horizontally across the upper part of the frame and cropped by the left and right frame edges, the foot of the leg and its soft shadow on the floor visible near the bottom",
 'angle':"a TIGHT detail close-up, camera very near the table and slightly above it, looking diagonally along the tabletop: one rounded corner of the tabletop enters from the left at mid-height, the tabletop surface fills the upper part of the frame and is cropped by the top and right frame edges, the single cylindrical leg stands below and to the right of centre and is cropped only by nothing at the bottom - its foot and soft shadow visible near the bottom edge. The table is far too big to fit in the frame; only this corner region is shown, exactly like the crop of the second image",
}
if __name__=='__main__':
    obj,ref,view,metal,out=sys.argv[1:6]
    mat='satin brushed aluminium' if metal=='aluminium' else 'satin brushed champagne brass'
    p=(f"Product photograph of the exact table shown in the FIRST image (MIIM-II: a square lacquered tabletop with softly rounded corners, "
       f"supported by ONE single wide cylindrical leg in the centre, {mat}). Compose it as {VIEW[view]}. "
       "Match the SECOND image exactly for camera distance, lens, crop tightness, lighting direction, soft shadows, the warm grey concrete studio floor "
       "and the overall photographic look. Keep the table's proportions, colour and materials identical to the first image: one leg only, same leg "
       "diameter relative to the top, same top thickness. Square format. No text, no extra objects.")
    print(call('fal-ai/nano-banana/edit',{'prompt':p,'image_urls':[uri(obj),uri(ref)],'num_images':1,'output_format':'png','aspect_ratio':'1:1'},out))
