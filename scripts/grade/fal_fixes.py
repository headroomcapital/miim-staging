import sys; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
PI='../../public/images/'
SEAM=("Remove the thin vertical seam line on the cylindrical metal leg: the cylinder must be one seamless, continuous piece of satin brushed metal with "
      "even, crisp fine brushing and a continuous soft highlight. Keep EVERYTHING else identical: the tabletop, the leg's exact size, shape and position, "
      "the floor, the shadows, the light, the camera and the crop. It must look like the same photograph.")
BOOKS=("Replace the books on the shelf at the right edge with two or three plain, unlabelled matte ceramic vessels in off-white and pale grey - no books, "
       "no lettering or text anywhere. Keep EVERYTHING else identical: the table, chairs, lamp, walls, floor, light, camera and crop. It must look like "
       "the same photograph.")
J=[]
for c in ['plum','yellow','cobalt','stone']:
    J.append((SEAM,f'out/miim-ii-{c}-aluminium.jpg',f'fal_out/fix/{c}-aluminium-main'))
    J.append((SEAM,f'out/miim-ii-{c}-aluminium-detail-angle.png',f'fal_out/fix/{c}-aluminium-angle'))
J.append((BOOKS,PI+'miim-ii-plum-brass-insitu-kitchen-cool.jpg','fal_out/fix/kitchen'))
def go(a):
    (p,src,out),n=a
    return call('fal-ai/nano-banana-pro/edit',{'prompt':p,'image_urls':[uri(src)],'num_images':1,'output_format':'png','resolution':'4K'},f'{out}-{n}.png')
import os; os.makedirs('fal_out/fix',exist_ok=True)
with ThreadPoolExecutor(12) as ex: print(list(ex.map(go,[(j,n) for j in J for n in range(2)])))
