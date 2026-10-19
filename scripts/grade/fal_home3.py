import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
SRC='/Users/headroom/Desktop/MIIM/originals/miim-i-cobalt-brass-home.png'
P=("Make a subtle, photorealistic correction to this exact photograph and output it at high resolution. Keep EVERYTHING the same: the room, curtains, "
   "light, herringbone floor, the dome pendant, all five chairs and their positions, the camera, and the deep cobalt lacquered tabletop with its dark "
   "front edge and the soft daylight reflection on its surface. Change only the two cylindrical table legs: move them further apart so their centres "
   "sit at one quarter and three quarters of the table length (equal overhang at both ends, each about a quarter of the length), and make their "
   "diameter about one fifth of the table length. The legs are satin brushed champagne brass, lit from behind like the rest of the scene, with soft "
   "vertical sheen and natural shadow, no mirror reflections. Do not restyle the image; it must look like the same photograph.")
def go(k): return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(SRC)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'1:1'},f'/Users/headroom/Desktop/MIIM/directions/canal/home-v3-{k}.png')
with ThreadPoolExecutor(3) as ex: print(list(ex.map(go,range(3))))
