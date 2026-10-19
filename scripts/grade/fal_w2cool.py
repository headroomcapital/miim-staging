import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
SRC='/Users/headroom/Desktop/MIIM/directions/warm/w2.png'
P=("Make a subtle, photorealistic correction to this exact photograph. Keep EVERYTHING the same: the room, arch, window, walls, terracotta floor, the "
   "Akari paper lantern, the four cane chairs and their positions, the camera, and the table exactly as it is (plum top, brass cylindrical legs, same "
   "shape and proportions). Two changes only: 1) remove the stoneware jug with olive branches from the tabletop, leaving the plum top completely empty "
   "and clean; 2) change the light from warm golden-hour to cooler, neutral soft daylight, like a bright overcast morning: white walls read clean "
   "off-white rather than orange, the terracotta keeps its natural colour, softer and less amber shadows, still gentle sun through the window. "
   "It must look like the same photograph, not restyled.")
def go(k): return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(SRC)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'4:3'},f'/Users/headroom/Desktop/MIIM/directions/warm/w2-cool-{k}.png')
with ThreadPoolExecutor(3) as ex: print(list(ex.map(go,range(3))))
