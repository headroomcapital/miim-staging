import sys; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
P=("Re-render ONLY the surface of the brass cylinder leg so the brushed finish is crisp and EVEN over the whole leg: very fine, sharp, horizontal "
   "circumferential brushing lines (like a lathe-turned satin brass cylinder) clearly visible everywhere on the leg, from top to bottom and edge to "
   "edge, with no smooth, smeared, soft or blurry patches anywhere. Keep the same light champagne brass colour, the same soft vertical highlight and "
   "shading. Keep EVERYTHING else identical: the tabletop, the leg's exact size, outline and position, the floor, the shadows, the camera and the crop. "
   "It must look like the same photograph, in perfect focus.")
SRC={'frontal':'{c}-frontal-0.png','angle':'{c}-angle-s0.png'}
def go(a):
    c,v,n=a
    return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri('fal_out/ii-brass/'+SRC[v].format(c=c))],'num_images':1,'output_format':'png',
        'resolution':'4K','aspect_ratio':'1:1'},f'fal_out/ii-brass/{c}-{v}-c{n}.png')
todo=[(c,v,n) for c in ['plum','yellow','cobalt','stone'] if not ARGS or c in ARGS for v in ['frontal','angle'] for n in range(2)]
with ThreadPoolExecutor(16) as ex: print(list(ex.map(go,todo)))
