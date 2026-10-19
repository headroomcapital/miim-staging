import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
REF='out/miim-i-cobalt-brass.png'
P=("Professional architectural interior photograph, medium-format camera, razor-sharp, natural fine detail, photorealistic. A quiet library room in a "
   "renovated Mediterranean house: a softly curved limewash plaster wall and ceiling in pale warm-grey, a tall slim steel-framed bookcase on the left "
   "wall filled with real hardback books and magazines with crisp legible spines, a full-height glass-block wall on the right letting in soft cool "
   "daylight, an old honed limestone slab floor in cool grey. In the centre of the room, slightly right, three-quarter view: the exact table from the "
   "reference image (MIIM-I) — a long deep cobalt-blue lacquered top, 3.8 cm thick with tight corners, on two wide cylindrical legs of satin brushed "
   "champagne brass, each leg diameter about one fifth of the table length, centres at one quarter and three quarters of its length. Two dark walnut "
   "Bruno Rey dining chairs, one on each side of the table. Empty tabletop. Calm, minimal, cooler neutral daylight, soft shadows. Square format, no "
   "people, no text.")
def go(k): return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(REF)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'1:1'},f'/Users/headroom/Desktop/MIIM/directions/canal/studio3-{k}.png')
with ThreadPoolExecutor(4) as ex: print(list(ex.map(go,range(4))))
