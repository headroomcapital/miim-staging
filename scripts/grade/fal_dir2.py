# Gallery direction, round 2: real design classics in the scene as references.
import sys,os,json; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OUT='/Users/headroom/Desktop/MIIM/directions/gallery'
KEEP=(" Keep the MIIM table EXACTLY as in the image — same shape, proportions, tabletop colour and thickness, the same cylindrical legs, their number "
      "and positions. Reproduce the named design pieces faithfully and recognisably, true to their real proportions and materials. Change only the room, "
      "light and the added furniture. Photoreal architectural interior photography, sharp, no text, no people, no logos.")
V=[
 ('g5','out/miim-i-cobalt-brass.png',"White-cube contemporary art gallery: white walls, pale polished concrete floor, a band of late-afternoon sun raking across the "
  "floor. Around the table stand four Mario Bellini CAB chairs (Cassina) in black saddle leather. On the table one clear glass Alvar Aalto Savoy vase."),
 ('g6','out/miim-i-plum-brass.png',"White gallery space with soft overcast skylight, pale microcement floor. Four Marcel Breuer Cesca chairs (chrome tube "
  "frame, natural cane seat and back) at the table, and a Flos Arco floor lamp (white marble base, arching stainless steel arm) reaching over the table."),
 ('g7','out/miim-i-yellow-steel.png',"Raw white gallery with whitewashed brick walls and grey epoxy floor, cool northern daylight. Four Jean Prouvé Standard "
  "chairs (Vitra, black steel legs, natural oak seat and back) around the table, and a black three-arm Serge Mouille wall lamp on the wall behind."),
 ('g8','out/miim-ii-stone-aluminium.jpg',"Intimate white gallery room, lime-plaster walls, pale limestone floor. Two Hans Wegner CH24 Wishbone chairs in "
  "natural oak with paper-cord seats at the table, and a Louis Poulsen PH5 pendant in white hanging above the table centre, softly lit."),
]
def go(v):
    k,src,p=v
    call('fal-ai/nano-banana-pro/edit',{'prompt':p+KEEP,'image_urls':[uri(src)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'4:3'},f'{OUT}/{k}.png')
    return k
with ThreadPoolExecutor(4) as ex: print(list(ex.map(go,V)))
old=json.load(open(f'{OUT}/prompts.json')) if os.path.exists(f'{OUT}/prompts.json') else []
json.dump(old+[{'id':k,'source':os.path.basename(s),'prompt':p} for k,s,p in V],open(f'{OUT}/prompts2.json','w'),indent=1)
