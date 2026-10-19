import sys,os; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OBJ="out/miim-ii-stone-aluminium.jpg"
TABLE=("the exact table in the image: MIIM-II, a SQUARE lacquered tabletop (all four sides equal, softly rounded corners, about 3.8 cm thick) "
       "resting on ONE single wide cylindrical leg of satin brushed aluminium that stands exactly under the CENTRE of the square. "
       "The square top is about two and a half times as wide as the leg diameter, so the top overhangs the leg equally on every side.")
LOOK=(" Same warm grey concrete studio floor, same soft diffuse studio light and soft shadows as the image, photoreal product photography, "
      "square 1:1 format, no text, no other objects, no second leg.")
P={'frontal':"Close-up product photo, camera at about table-top height looking straight at the FRONT EDGE of "+TABLE+
   " Framing: the front edge of the top runs horizontally across the upper third of the frame and BOTH front corners are visible, "
   "with equal overhang left and right of the leg; the leg is exactly centred horizontally; the foot of the leg and its soft shadow are visible near the bottom."+LOOK,
   'angle':"Close-up three-quarter product photo, camera slightly above the table looking diagonally at one CORNER of "+TABLE+
   " Framing: the nearest rounded corner of the square top points toward the camera, slightly left of centre; both edges meeting at that corner "
   "recede to the left and right; the leg stands under the middle of the square, set back from the corner by about the leg's own diameter, "
   "so the top clearly overhangs it; the foot and its soft shadow are visible near the bottom."+LOOK}
def gen(a):
    v,k=a; return call('fal-ai/nano-banana/edit',{'prompt':P[v],'image_urls':[uri(OBJ)],'num_images':1,'output_format':'png','aspect_ratio':'1:1'},f'fal_out/ii/g2-{v}-{k}.png')
with ThreadPoolExecutor(6) as ex: print(list(ex.map(gen,[(v,k) for v in P for k in range(3)])))
