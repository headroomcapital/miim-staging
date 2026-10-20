import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
SRC='/Users/headroom/Desktop/MIIM/directions/canal/studio3-rey-1.png'
KEEP=" Keep everything else identical: the room, glass-block wall, stone floor, light, camera position and framing, the two chairs, and the table exactly as it is. It must look like the same real photograph."
P={'dof':("Make this photograph look shot with a fast lens at f/1.8, focused on the blue table: the table and chairs stay razor-sharp while the bookcase "
          "and its books on the left wall fall into a soft, natural optical blur with creamy bokeh, so no book titles or lettering are legible at all, "
          "only the colours and shapes of real, varied books. Natural lens depth-of-field falloff, no artificial blur halo around the table."+KEEP),
   'wall':("Remove the bookcase and all books entirely. In its place the curved limewash plaster wall continues, with one deep, shallow-arched niche "
           "set into the wall holding a single large handmade stoneware vessel, softly lit by the daylight. Calm, minimal, no text anywhere."+KEEP)}
jobs=[(k,i) for k in P for i in range(2)]
def go(a):
    k,i=a; return call('fal-ai/nano-banana-pro/edit',{'prompt':P[k],'image_urls':[uri(SRC)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'1:1'},f'/Users/headroom/Desktop/MIIM/directions/canal/studio-{k}-{i}.png')
with ThreadPoolExecutor(4) as ex: print(list(ex.map(go,jobs)))
