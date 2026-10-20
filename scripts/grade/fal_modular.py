import sys,os,json; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OUT='/Users/headroom/Desktop/MIIM/directions/modular'
R1='out/miim-i-cobalt-brass.png'; R2='out/miim-ii-stone-aluminium.jpg'
I=("MIIM-I tables exactly like the FIRST reference image: long rectangular lacquered tops 3.8 cm thick with tight corners on TWO wide cylindrical legs, "
   "each leg diameter about one fifth of the table length, leg centres at one quarter and three quarters of the length")
II=("MIIM-II tables exactly like the SECOND reference image: SQUARE lacquered tops with softly rounded corners on ONE single wide cylindrical leg exactly "
    "under the centre, the top about two and a half times as wide as the leg")
RULES=(" Every table top is completely empty. Soft, cool, neutral daylight. Reproduce named design pieces faithfully. No people, no text, no lettering, "
       "no logos, no screens, no books, no menus. Professional architectural interior photograph, wide view, razor-sharp, photorealistic.")
S=[
 ('m01',"A bright, minimal café with white limewash walls, a large steel-framed shopfront window and a pale terrazzo floor. Six "+II+" arranged in a "
  "loose grid, tops in signal yellow, stone, deep cobalt blue and deep wine plum, legs in brushed aluminium and champagne brass. Two Thonet No. 14 "
  "bentwood chairs at each table. Three Louis Poulsen PH5 pendants above.",'16:9',[R2]),
 ('m02',"A Scandinavian café-bakery with pale oak floorboards, white walls and tall windows. Along the window a row of four "+II+" in alternating stone and "
  "signal yellow with aluminium legs, each with two Børge Mogensen J39 chairs; in the middle of the room one long "+I.replace('tables','table',1)+" in "
  "deep cobalt blue with brass legs, used as a communal table with six Hans Wegner CH24 Wishbone chairs.",'16:9',[R1,R2]),
 ('m03',"An open-plan design studio office in a converted warehouse: whitewashed brick, polished concrete floor, big factory windows. Four "+I+" placed "
  "in two neat rows as desks, tops in stone, legs in stainless steel, each desk with two Vitra Eames Aluminium Group chairs in black and one Artemide "
  "Tolomeo desk lamp. Clean, calm, no clutter.",'16:9',[R1]),
 ('m04',"A calm boardroom with pale grey walls, oak parquet and a long window. Two "+I+" placed end to end so they form one continuous 4.2-metre "
  "meeting table, a fine seam where the two tops meet, four cylindrical brass legs in total, tops in deep cobalt blue. Ten Vitra Eames Aluminium "
  "Group chairs in black leather around it. Two Flos Aim pendants above.",'16:9',[R1]),
 ('m05',"A coworking space with white walls, light oak floor and large windows. A mix of "+I+" in stone with steel legs used as shared desks, and "
  "several "+II+" in signal yellow and deep cobalt blue with aluminium legs used as small meeting tables. Muller Van Severen Alu Chairs in silver-grey "
  "at the meeting tables and Jean Prouvé Standard chairs at the desks.",'16:9',[R1,R2]),
 ('m06',"A gallery-like showroom with white walls, a pale microcement floor and soft skylight. The MIIM system displayed: three "+I+" and three "+II+" "
  "spaced generously in a calm composition, in all four colours (signal yellow, stone, deep cobalt blue, deep wine plum) and both bases (brushed "
  "steel and champagne brass). No chairs.",'16:9',[R1,R2]),
]
def go(v):
    (k,p,ar,refs),n=v
    call('fal-ai/nano-banana-pro/edit',{'prompt':p+RULES,'image_urls':[uri(r) for r in refs],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':ar},f'{OUT}/{k}-{n}.png'); return f'{k}-{n}'
if __name__=='__main__':
    todo=[(v,n) for v in S if not ARGS or v[0] in ARGS for n in range(2)]
    with ThreadPoolExecutor(12) as ex: print(list(ex.map(go,todo)))
    json.dump([{'id':k,'prompt':p} for k,p,ar,r in S],open(f'{OUT}/prompts.json','w'),indent=1)
