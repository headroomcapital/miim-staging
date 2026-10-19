import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
D='/Users/headroom/Desktop/MIIM/directions/warm/'
P=("Make a subtle, photorealistic correction to this exact photograph. Keep EVERYTHING the same: the room, walls, floor, windows, every piece of "
   "furniture and lighting fixture and their positions, the camera, and the MIIM table exactly as it is (same tabletop colour, legs, shape and "
   "proportions). Two changes only: 1) remove every object from the tabletop (bowls, fruit, vases, books, cups, teapot, glasses, bread, napkins) so the "
   "top is completely empty and clean; 2) change the light from warm golden/amber to cooler, neutral soft daylight like a bright overcast morning: "
   "walls read clean off-white or their true colour rather than orange, wood and floors keep their natural colour, softer and less amber shadows. "
   "It must look like the same photograph, not restyled.")
jobs=[(k,i) for k in ('w1','w3','w5','w6') for i in range(2)]
def go(a):
    k,i=a; return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(D+k+'.png')],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'4:3'},f'{D}{k}-cool-{i}.png')
with ThreadPoolExecutor(8) as ex: print(list(ex.map(go,jobs)))
