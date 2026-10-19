import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
SRC='/Users/headroom/Desktop/MIIM/originals/miim-i-cobalt-brass-home.png'; REF='out/miim-i-cobalt-brass.png'
P=("Recreate the FIRST image at high resolution with an updated table. Keep the room exactly: the tall sheer white curtains, the two windows, the "
   "herringbone oak floor, the skirting, the smoked chrome-glass dome pendant on its thin cable, the five pale blue Bruno Rey chairs in the same "
   "positions, the same frontal symmetrical camera, the same soft daylight. Replace ONLY the dining table with the exact table from the SECOND image "
   "(MIIM-I), with these exact proportions: the top is a long rectangle, 210 cm long and 100 cm deep, only 3.8 cm thick, with SMALL tight corner "
   "radii (nearly square corners, not rounded like a pill); it is deep cobalt-blue lacquer. It stands on two cylindrical legs of satin brushed "
   "champagne brass (soft vertical highlights, no mirror reflections). Each leg's diameter is about one fifth of the table length (40 cm). The two "
   "leg centres are at one quarter and three quarters of the table length, so they are exactly half the table length apart, leaving equal overhangs "
   "at both ends. The table stands "
   "in the same place among the chairs, seen from the front. Photoreal interior photography, sharp, no text.")
def go(k): return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(SRC),uri(REF)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'1:1'},f'/Users/headroom/Desktop/MIIM/directions/canal/home-v2-{k}.png')
with ThreadPoolExecutor(3) as ex: print(list(ex.map(go,range(3))))
