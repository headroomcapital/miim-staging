import sys; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
P=("Remove the thin vertical seam line running down the left part of the brass cylinder leg: the cylinder must be one seamless, continuous piece "
   "of satin brushed champagne brass with smooth, even vertical brushing and a continuous soft highlight. Keep EVERYTHING else identical: the "
   "tabletop, the leg's exact size, shape and position, the floor, the shadows, the light, the camera and the crop. It must look like the same photograph.")
src=ARGS[0] if ARGS else 'ii-brass'
def go(a):
    c,n=a
    return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(f'fal_out/ii-brass/{c}-angle-0.png')],'num_images':1,'output_format':'png',
        'resolution':'4K','aspect_ratio':'1:1'},f'fal_out/ii-brass/{c}-angle-s{n}.png')
with ThreadPoolExecutor(8) as ex: print(list(ex.map(go,[(c,n) for c in ['plum','yellow','cobalt','stone'] for n in range(2)])))
