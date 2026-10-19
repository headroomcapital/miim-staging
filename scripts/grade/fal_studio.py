import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
SRC='/Users/headroom/Desktop/MIIM/originals/miim-i-cobalt-brass-studio.png'
P=("Make a subtle, photorealistic correction to this exact photograph and output it at high resolution. Keep EVERYTHING the same: the room, the "
   "curved plaster wall and ceiling, the bookcase and books, the glass-block wall, the stone floor, the light, the two wooden chairs and their "
   "positions, the camera, and the deep cobalt lacquered tabletop with its edge and surface sheen. Change only the two cylindrical table legs: they "
   "are satin brushed champagne brass, clean and uniform (no stains, patina or mottling), with a soft vertical sheen and natural shading from the "
   "room's light, no mirror reflections. Their diameter is about one fifth of the table length and their centres sit at one quarter and three "
   "quarters of the table length, with equal overhang at both ends. Do not restyle the image; it must look like the same photograph.")
def go(k): return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(SRC)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'1:1'},f'/Users/headroom/Desktop/MIIM/directions/canal/studio-{k}.png')
with ThreadPoolExecutor(3) as ex: print(list(ex.map(go,range(3))))
