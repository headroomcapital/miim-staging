import sys,os,json,base64,subprocess,tempfile; sys.argv=['x']
from fal_gen import call
from PIL import Image
def uri(p,maxs=2048):
    t=tempfile.mktemp(suffix='.jpg'); im=Image.open(p).convert('RGB'); im.thumbnail((maxs,maxs)); im.save(t,quality=94)
    d='data:image/jpeg;base64,'+base64.b64encode(open(t,'rb').read()).decode(); os.unlink(t); return d
from concurrent.futures import ThreadPoolExecutor
P=("Edit the FIRST image. Keep its composition exactly: the same four tables, same positions, same camera, same table shapes and the same tabletop "
   "colours (cream back-left, plum front-left, blue back-right, yellow front-right). Change ONLY the metal cylindrical legs and the overall photographic tone: "
   "the legs of the PLUM table and of the BLUE table become satin brushed champagne brass, exactly like the brass leg in the SECOND image; the legs of the "
   "CREAM table and of the YELLOW table become satin brushed aluminium, exactly like the aluminium leg in the THIRD image. All legs are satin, with soft "
   "broad vertical highlight bands and no mirror reflections. Match the light, soft neutral studio look of the second and third images: brighter light grey "
   "wall and floor, soft diffuse light, soft shadows. Photoreal, sharp, no text.")
IMG='/Users/headroom/Desktop/claude/miim-v2/scripts/grade/out'
def go(k):
    return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri('fal_in/gallery3-src.jpg'),uri(f'{IMG}/miim-ii-stone-brass.jpg'),uri(f'{IMG}/miim-ii-stone-aluminium.jpg')],
               'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'16:9'},f'fal_out/group-{k}.png')
with ThreadPoolExecutor(2) as ex: list(ex.map(go,range(2)))
