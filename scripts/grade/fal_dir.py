# Scene directions: edit a graded product photo into a new setting, table kept exact.
import sys,os,json; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OUT='/Users/headroom/Desktop/MIIM/directions/gallery'
KEEP=(" Keep the table EXACTLY as in the image — same shape, proportions, tabletop colour and thickness, the same cylindrical legs, their number "
      "and positions, the same camera angle and framing of the table. Change only the room, light and atmosphere around it. Photoreal architectural "
      "interior photography, sharp, no text, no people.")
V=[
 ('g1','out/miim-i-cobalt-brass.png',"Turn the setting into a white-cube contemporary art gallery: smooth white walls, polished pale grey concrete floor, a tall "
  "window outside the frame casting a long raking band of late-afternoon sun across the floor and the table, crisp shadows. Completely empty room."),
 ('g2','out/miim-i-plum-brass.png',"Turn the setting into a white-cube art gallery with soft overcast daylight from a long ceiling skylight, even and calm, very "
  "gentle shadows, pale microcement floor, white walls with a single shadow gap at the floor. Empty, silent, museum-like."),
 ('g3','out/miim-i-yellow-steel.png',"Turn the setting into a raw white gallery space: whitewashed brick walls, grey epoxy floor, cool northern daylight from "
  "high windows, a faint shadow of a window frame on the wall. Industrial but clean and empty."),
 ('g4','out/miim-ii-stone-aluminium.jpg',"Turn the setting into an intimate white gallery room: lime-plaster white walls, pale limestone floor, a single focused "
  "spotlight from above lighting the table like an exhibited sculpture, the room edges falling off softly into shadow."),
]
def go(v):
    k,src,p=v
    call('fal-ai/nano-banana-pro/edit',{'prompt':p+KEEP,'image_urls':[uri(src)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'4:3'},f'{OUT}/{k}.png')
    return k
with ThreadPoolExecutor(4) as ex: print(list(ex.map(go,V)))
json.dump([{'id':k,'source':os.path.basename(s),'prompt':p} for k,s,p in V],open(f'{OUT}/prompts.json','w'),indent=1)
