import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
SRC='/Users/headroom/Desktop/MIIM/directions/canal/studio3-rey-1.png'
P=("Make a photorealistic edit to this exact photograph. Keep EVERYTHING identical — the room, curved plaster walls and ceiling, the glass-block wall, "
   "the stone floor, the light, the camera, the two chairs, and the table exactly as it is — except the contents of the steel bookcase. Restyle the "
   "bookcase as a calm, curated architect's library: fewer books with generous gaps; plain clothbound and linen books with completely blank spines, "
   "absolutely no lettering, titles, logos or text anywhere; a restrained tonal palette of off-white, warm grey, stone, charcoal and a few deep "
   "navy-blue volumes; some books standing, several laid flat in neat horizontal stacks; a few handmade ceramic vessels and a small stone object "
   "on some shelves; some shelves partly empty. The bookcase sits slightly softer in focus than the table, like a shallow depth of field. "
   "It must look like the same real photograph, razor-sharp on the table.")
def go(k): return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(SRC)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'1:1'},f'/Users/headroom/Desktop/MIIM/directions/canal/studio-books-{k}.png')
with ThreadPoolExecutor(3) as ex: print(list(ex.map(go,range(3))))
