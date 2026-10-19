import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
SRC='/Users/headroom/Desktop/MIIM/directions/canal/studio-1.png'; REF='out/miim-i-cobalt-brass.png'
BASE=("Re-render the FIRST image from scratch as a brand-new, ultra-sharp, high-resolution architectural interior photograph, shot on a medium-format "
      "camera with a tilt-shift lens: crisp fine detail everywhere, no blur, no smudging, no upscaling artefacts, no AI mush. Keep the same scene and "
      "composition: the curved plaster wall and ceiling, the tall metal-framed bookcase full of real, legible book spines, the large glass-block wall "
      "on the right, the old stone-slab floor, two dark wooden Bruno Rey chairs, and the same camera position. The dining table is exactly the MIIM-I "
      "from the SECOND image: a long deep cobalt-blue lacquered top, 3.8 cm thick with tight corners, on two wide cylindrical legs of satin brushed "
      "champagne brass, leg diameter about one fifth of the table length, centres at one quarter and three quarters of its length. Empty tabletop. ")
LIGHT={'warm':"Keep the warm, soft daylight and warm plaster tones of the original.",
       'cool':"Use cooler, neutral soft daylight like a bright overcast morning: plaster reads as pale warm-grey limewash rather than orange, stone floor cool grey, glass blocks bright white."}
jobs=[(t,k) for t in ('warm','cool') for k in range(2)]
def go(a):
    t,k=a; return call('fal-ai/nano-banana-pro/edit',{'prompt':BASE+LIGHT[t],'image_urls':[uri(SRC),uri(REF)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'1:1'},f'/Users/headroom/Desktop/MIIM/directions/canal/studio2-{t}-{k}.png')
with ThreadPoolExecutor(4) as ex: print(list(ex.map(go,jobs)))
