import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
P=("Re-photograph this exact table in a professional product studio, camera a little higher so the background behind the table is only the warm grey "
   "concrete floor (no wall visible). Keep the table identical: SQUARE tabletop with softly rounded corners, ONE single wide cylindrical satin brushed "
   "aluminium leg exactly centred under the top, same proportions and thickness. Soft diffuse light from the upper left, soft shadow to the right. "
   "Photoreal, extremely sharp, high detail, no text.")
SRC={'frontal':'fal_out/ii/g2-frontal-0.png','angle':'fal_out/ii/g2-angle-1.png'}
def go(a):
    v,k=a; return call('fal-ai/bytedance/seedream/v4/edit',{'prompt':P,'image_urls':[uri(SRC[v])],'num_images':1,'image_size':{'width':4096,'height':4096}},f'fal_out/ii/s-{v}-{k}.png')
with ThreadPoolExecutor(4) as ex: list(ex.map(go,[(v,k) for v in SRC for k in range(2)]))
