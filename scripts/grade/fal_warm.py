import sys,os,json; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OUT='/Users/headroom/Desktop/MIIM/directions/warm'
KEEP=(" Keep the MIIM table EXACTLY as in the image: same shape, proportions, tabletop colour and thickness, the same cylindrical legs, their number and "
      "positions. Reproduce the named design pieces faithfully and recognisably. Warm, lived-in, inviting atmosphere. Photoreal architectural interior "
      "photography, natural light, sharp, no text, no people, no logos.")
V=[
 ('w1','out/miim-i-cobalt-brass.png',"A warm Amsterdam canal-house dining room: wide oiled oak floorboards, warm lime-plaster walls in soft ochre, tall window with golden "
  "late-afternoon sun. Four Hans Wegner CH24 Wishbone chairs in oiled oak with natural paper-cord seats around the table, a wool rug in warm terracotta, "
  "a Louis Poulsen PH5 pendant in brass above the table, a ceramic bowl with fruit on the table."),
 ('w2','out/miim-i-plum-brass.png',"A warm Mediterranean dining room: whitewashed lime walls glowing warm, terracotta tile floor, deep window with low golden sun "
  "casting warm patterned light. Four Pierre Jeanneret Chandigarh chairs in teak with cane seats and backs around the table, an Isamu Noguchi Akari "
  "paper lantern hanging above, olive branches in a stoneware jug."),
 ('w3','out/miim-i-yellow-steel.png',"A warm mid-century living-dining space: walnut wall panelling, honey-coloured parquet, soft evening lamplight. Four Charlotte "
  "Perriand style Méribel straw-seat chairs in pine around the table, a Flos Arco floor lamp lit and arching over, a stack of books and a "
  "ceramic vase on the table."),
 ('w4','out/miim-ii-stone-brass.jpg',"A warm reading corner in a Parisian apartment: herringbone oak floor, warm limewash walls, morning sun through linen curtains. "
  "Two Hans Wegner CH24 Wishbone chairs in oiled oak at the small square table, a Louis Poulsen PH5 pendant in brass above, an espresso cup and a book "
  "on the table, a potted olive tree in the corner."),
 ('w5','out/miim-ii-plum-brass.jpg',"A warm café-style kitchen nook: terracotta floor tiles, warm plaster walls, golden afternoon light from a window on the left. "
  "Two Thonet No. 14 bentwood chairs in dark walnut at the square table, a Nelson Bubble lamp glowing above, a linen napkin, two glasses of wine and "
  "a small bread board on the table."),
 ('w6','out/miim-ii-cobalt-aluminium.jpg',"A warm Scandinavian breakfast corner: pale oak floorboards, warm white walls with soft sunlight, a large wool rug in "
  "oatmeal. Two Alvar Aalto Chair 66 in natural birch at the square table, an Artek Golden Bell pendant in brass above, a teapot and two "
  "ceramic cups on the table, a stoneware vase with dried grasses."),
]
def go(v):
    k,src,p=v
    call('fal-ai/nano-banana-pro/edit',{'prompt':p+KEEP,'image_urls':[uri(src)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'4:3'},f'{OUT}/{k}.png'); return k
with ThreadPoolExecutor(6) as ex: print(list(ex.map(go,V)))
json.dump([{'id':k,'source':os.path.basename(s),'prompt':p} for k,s,p in V],open(f'{OUT}/prompts.json','w'),indent=1)
