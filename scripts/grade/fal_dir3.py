import sys,os,json; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
G='/Users/headroom/Desktop/MIIM/directions/gallery'; OUT='/Users/headroom/Desktop/MIIM/directions/gallery-r2'
KEEP=(" Keep the room, the design furniture and the MIIM table exactly as they are: same table proportions, tabletop thickness, cylindrical legs, "
      "their number and positions. Photoreal architectural interior photography, sharp, no text, no people, no logos.")
V=[
 ('g6a','g6',"Move the camera much closer at seated eye level, a three-quarter view of the table and the Cesca chairs filling most of the frame, the Arco lamp's arc entering from above."),
 ('g6b','g6',"Same view, but late afternoon: low warm sun through a window outside the frame casts long raking light and chair shadows across the floor."),
 ('g6c','g6',"Same view, but the tabletop is deep cobalt blue lacquer (#25227B) instead of plum; legs stay brushed brass."),
 ('g8a','g8',"Move the camera closer at seated eye level, a three-quarter view of the square table, the two Wishbone chairs and the PH5 pendant filling the frame."),
 ('g8b','g8',"Same view at evening: daylight gone, the PH5 pendant is lit and casts a warm pool of light on the tabletop and floor, the room falling softly into shadow."),
 ('g8c','g8',"Same view, but the tabletop is deep wine plum lacquer (#502D38) and the single cylindrical leg is satin brushed champagne brass."),
]
def go(v):
    k,src,p=v
    call('fal-ai/nano-banana-pro/edit',{'prompt':p+KEEP,'image_urls':[uri(f'{G}/{src}.png')],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'4:3'},f'{OUT}/{k}.png'); return k
with ThreadPoolExecutor(6) as ex: print(list(ex.map(go,V)))
src_of={'g6':'miim-i-plum-brass.png','g8':'miim-ii-stone-aluminium.jpg'}
json.dump([{'id':k,'source':src_of[s],'prompt':f'From {s.upper()}: '+p} for k,s,p in V],open(f'{OUT}/prompts.json','w'),indent=1)
