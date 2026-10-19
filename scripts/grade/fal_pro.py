import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
KEEP=(" The table must stay exactly as in the image: SQUARE top with softly rounded corners and equal overhang on every side, ONE wide cylindrical "
      "satin brushed aluminium leg exactly centred under the top. Same soft neutral studio light from the upper left, warm grey concrete floor, "
      "soft shadow to the right. Photoreal product photography, very sharp. No wall visible, only floor behind. No text.")
P={'frontal':("Close-up detail photo of this table, camera close and at table height looking straight at the front edge: the front edge of the "
              "square top runs horizontally across the upper third of the frame with BOTH front rounded corners visible near the left and right "
              "frame edges, the centred cylindrical leg below it, the leg's foot and soft shadow near the bottom of the frame."+KEEP),
   'angle':("Three-quarter photo of this whole table, camera fairly close and above table height looking down at about 30 degrees toward one "
            "corner: the ENTIRE square top is visible as a diamond-like shape filling most of the frame width, its nearest corner pointing toward "
            "the camera at the bottom-left of the top, all four rounded corners visible; the single leg stands exactly under the CENTRE of the "
            "square, so equal amounts of top overhang it on the left and right; the foot of the leg and its soft shadow visible below."+KEEP)}
SRC={'frontal':'fal_out/ii/g2-frontal-0.png','angle':'fal_out/ii/g2-angle-2.png'}
def go(a):
    v,k=a; return call('fal-ai/nano-banana-pro/edit',{'prompt':P[v],'image_urls':[uri(SRC[v])],'num_images':1,'output_format':'png','aspect_ratio':'1:1','resolution':'4K'},f'fal_out/ii/p-{v}-{k}.png')
with ThreadPoolExecutor(4) as ex: list(ex.map(go,[(v,k) for v in ['angle'] for k in range(2,5)]))
