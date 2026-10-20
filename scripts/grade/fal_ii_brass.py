import sys; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
P=("Change ONLY the material of the cylindrical leg in the FIRST image: make it satin brushed champagne brass exactly like the leg in the SECOND image "
   "- light, warm, clean champagne-gold with fine vertical brushing, a soft bright highlight running down the cylinder and gentle shading toward its "
   "edges, a crisp clean silhouette and a clean round foot, no seam, no dents, no smudges. Keep EVERYTHING else identical: the exact tabletop colour, "
   "shape and edge, the leg's exact size, position and outline, the floor, the shadows, the camera and the crop. It must look like the same photograph "
   "with only the metal changed. No text.")
def go(a):
    c,v,n=a
    return call('fal-ai/nano-banana-pro/edit',{'prompt':P,'image_urls':[uri(f'out/miim-ii-{c}-aluminium-detail-{v}.png'),uri(f'out/miim-ii-{c}-brass.jpg')],
        'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'1:1'},f'fal_out/ii-brass/{c}-{v}-{n}.png')
todo=[(c,v,n) for c in ['plum','yellow','cobalt','stone'] if not ARGS or c in ARGS for v in ['frontal','angle'] for n in range(2)]
with ThreadPoolExecutor(16) as ex: print(list(ex.map(go,todo)))
