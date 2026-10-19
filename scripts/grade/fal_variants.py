import sys,os; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
COL={'yellow':('signal yellow','#DFE145'),'cobalt':('deep cobalt / ultramarine blue','#25227B'),'plum':('deep wine plum','#502D38')}
KEEP=" Do not change anything else: same shape, geometry, framing, camera, lighting, floor and shadows."
def brass(view):
    call('fal-ai/nano-banana/edit',{'prompt':"Change only the material of the cylindrical leg from satin brushed aluminium to satin brushed champagne brass (warm pale gold, soft diffuse vertical sheen, not shiny gold, not copper)."+KEEP,
        'image_urls':[uri(f'fal_out/ii/v-{view}-stone-aluminium.png')],'num_images':1,'output_format':'png'},f'fal_out/ii/v-{view}-stone-brass.png')
def colour(view,metal,c):
    n,h=COL[c]
    call('fal-ai/nano-banana/edit',{'prompt':f"Change only the colour of the lacquered tabletop to {n} ({h}), an even satin lacquer finish on the top surface and its edge."+KEEP,
        'image_urls':[uri(f'fal_out/ii/v-{view}-stone-{metal}.png')],'num_images':1,'output_format':'png'},f'fal_out/ii/v-{view}-{c}-{metal}.png')
with ThreadPoolExecutor(8) as ex: list(ex.map(brass,('frontal','angle')))
with ThreadPoolExecutor(12) as ex: list(ex.map(lambda a:colour(*a),[(v,m,c) for v in ('frontal','angle') for m in ('aluminium','brass') for c in COL]))
print(sorted(f for f in os.listdir('fal_out/ii') if f.startswith('v-')))
