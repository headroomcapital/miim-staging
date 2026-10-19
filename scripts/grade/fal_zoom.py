import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
KEEP=(" Keep the table exactly the same: square top, rounded corners, same thickness, the single leg centred under the top, same proportions, "
      "satin brushed aluminium leg, same lighting and concrete floor. Photoreal, 1:1, no text.")
P={'frontal':("Move the camera much closer to this table and slightly higher, looking at the front edge: the square tabletop now spans almost the "
              "full width of the frame with both front corners just inside the left and right edges, the front edge across the upper third, "
              "the centred leg below, its foot and soft shadow near the bottom. Only the concrete floor is visible behind the table, no wall."+KEEP),
   'angle':("Move the camera much closer to this table and slightly higher, a three-quarter detail view of one corner: the nearest rounded "
            "corner of the square top is in the upper left area of the frame, the top fills most of the upper half and is cropped by the right "
            "frame edge, the single leg stands under the middle of the square, set back from the corner, its foot and soft shadow near the "
            "bottom. Only the concrete floor is visible behind, no wall."+KEEP)}
SRC={'frontal':'fal_out/ii/g2-frontal-0.png','angle':'fal_out/ii/g2-angle-2.png'}
def go(a):
    v,k=a; return call('fal-ai/nano-banana/edit',{'prompt':P[v],'image_urls':[uri(SRC[v])],'num_images':1,'output_format':'png','aspect_ratio':'1:1'},f'fal_out/ii/z-{v}-{k}.png')
with ThreadPoolExecutor(6) as ex: list(ex.map(go,[(v,k) for v in P for k in range(3)]))
