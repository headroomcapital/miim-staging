import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
D='/Users/headroom/Desktop/MIIM/directions/modular/'
P=("Edit the FIRST image. Only the middle Signal Yellow table changes: turn it 90 degrees so it stands in the same orientation as the blue table on the "
   "left - its long side facing the camera, so BOTH of its two cylindrical steel legs are clearly visible side by side, well apart, at a quarter and "
   "three quarters of its length, exactly like the table in the SECOND image (same proportions, same acid lemon-yellow #DFE145 top, same brushed steel "
   "legs). Keep its two white swivel chairs behind it. Keep EVERYTHING else identical: the blue and stone tables, the room, plants, art, light and "
   "camera. It must look like the same photograph.")
def go(n): return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(D+'v1-6.png'),uri('out/miim-i-yellow-steel.png')],'num_images':1,
    'output_format':'png','resolution':'4K','aspect_ratio':'16:9'},f'{D}v6-{n}.png')
with ThreadPoolExecutor(3) as ex: print(list(ex.map(go,range(3))))
