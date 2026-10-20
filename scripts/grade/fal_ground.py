import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
D='/Users/headroom/Desktop/MIIM/directions/series20/'
P=("The two brass cylinder legs of the table look like they float above the parquet. Make them stand firmly ON the floor: each cylinder's flat base "
   "sits directly on the parquet with a thin, dark contact shadow line right where metal meets wood, soft ambient-occlusion darkening of the floor "
   "around the foot of each leg, a faint warm reflection of the brass in the floor directly beneath, and the table's soft shadow on the floor under "
   "the top consistent with the window light coming from behind. Keep EVERYTHING else identical: the table, its colour and proportions, the legs' "
   "exact size and position, the chairs, the lamp, the room, the light and the camera. It must look like the same photograph.")
def go(n): return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(D+'s04.png')],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'16:9'},f'{D}ground/s04-ground-{n}.png')
with ThreadPoolExecutor(4) as ex: print(list(ex.map(go,range(4))))
