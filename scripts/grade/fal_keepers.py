import sys; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
D='/Users/headroom/Desktop/MIIM/directions/series20/'
KEEP=(" Keep EVERYTHING else identical: the room, walls, windows, light, camera and framing, every other object, and the table exactly as it is — "
      "same top colour, shape and thickness, same cylindrical legs with the same diameter, number and positions. It must look like the same photograph.")
MVS=("Replace only the chairs with authentic Muller Van Severen Alu Chairs (Valerie Objects): minimal chairs folded from thin anodised aluminium sheet, "
     "a flat square seat and a flat rectangular backrest on slim flat-bar legs, matte {c} anodised finish. Same number of chairs, same positions and scale.")
J=[('s02-limestone','s02',"Replace only the floor with large, pale, honed limestone slabs with fine joints, calm and even."+KEEP),
   ('s02-oak','s02',"Replace only the floor with wide, pale, matte oiled oak floorboards."+KEEP),
   ('s07-mvs','s07',MVS.format(c='silver-grey')+KEEP),
   ('s20-mvs','s20',MVS.format(c='soft powder-blue')+KEEP)]
jobs=[(o,s,p,k) for o,s,p in J for k in range(2)]
def go(a):
    o,s,p,k=a; return call('fal-ai/nano-banana-pro/edit',{'prompt':p,'image_urls':[uri(D+s+'.png')],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'16:9' if s=='s03' else '4:3'},f'{D}keepers/{o}-{k}.png')
with ThreadPoolExecutor(8) as ex: print(len(list(ex.map(go,jobs))))
