import sys,os,json; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OUT='/Users/headroom/Desktop/MIIM/directions/modular'
R1='out/miim-i-stone-steel.png'; R1b='out/miim-i-cobalt-brass.png'; R2='out/miim-ii-stone-aluminium.jpg'
I=("MIIM-I tables exactly like the FIRST reference image: long rectangular tops, 210 cm long and 100 cm wide, 3.8 cm thick, in smooth matte LACQUER "
   "(a flat painted finish, no stone or wood texture), on exactly TWO wide cylindrical legs per table - each leg diameter about one fifth of the "
   "table length, the two legs far apart with their centres at one quarter and three quarters of the length, a wide open gap between them")
II=("MIIM-II tables exactly like the reference image: SQUARE lacquered tops with softly rounded corners on ONE single wide cylindrical leg exactly "
    "under the centre, the top about two and a half times as wide as the leg")
RULES=(" Reproduce the named design chairs faithfully. Soft, cool, neutral daylight. No people, no text, no lettering, no logos, no screens, no books, "
       "no paper. Professional architectural interior photograph, razor-sharp, photorealistic.")
EDIT=(" Keep EVERYTHING else identical: the tables, their legs, colours and positions, the room, floor, light and camera. Only the chairs change. "
      "It must look like the same photograph.")
M04=f'{OUT}/m04-1.png'
S=[
 ('o1',"An open-plan design studio office in a converted warehouse: whitewashed brick, polished concrete floor, big factory windows. Four "+I+", in "
  "warm stone-beige lacquer with brushed stainless steel legs, placed in two neat rows as desks with generous space between them. At each desk two "
  "Vitra Pacific Chair office task chairs by Barber Osgerby in soft warm grey with five-star polished aluminium bases on castors, and one Artemide "
  "Tolomeo desk lamp. Table tops otherwise empty. Clean and calm.",[R1],None),
 ('o2',"A bright Scandinavian office with white walls, pale oak floor and tall windows. Three "+I+" placed in a single row as desks, tops in deep "
  "cobalt blue, signal yellow and stone lacquer, legs in brushed steel. At each desk two Fritz Hansen Series 7 swivel chairs on five-star aluminium "
  "bases with castors, in white. One Louis Poulsen Panthella table lamp per desk. Otherwise empty tops.",[R1,R2],None),
 ('o3',"Replace every chair in this photograph with a Knoll Pollock Executive Chair by Charles Pollock in black leather, with its signature "
  "polished aluminium rim around the shell and five-star base on castors."+EDIT,[M04],'edit'),
 ('o4',"Replace every chair in this photograph with a Fritz Hansen Oxford Chair by Arne Jacobsen, low back, in black leather on a five-star "
  "polished aluminium swivel base."+EDIT,[M04],'edit'),
 ('o5',"A coworking space with white walls, light oak floor and large windows. Along the window two "+I+" in stone lacquer with steel legs used as "
  "shared desks, each with Vitra Pacific Chair office task chairs in soft grey. In the room three "+II+" in signal yellow and deep cobalt blue with "
  "brushed aluminium legs used as small meeting tables, each with Muller Van Severen Alu Chairs in silver-grey. All table tops empty.",[R1,R2],None),
]
def go(v):
    (k,p,refs,mode),n=v
    call('fal-ai/nano-banana-pro/edit',{'prompt':p+RULES,'image_urls':[uri(r) for r in refs],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'16:9'},f'{OUT}/{k}-{n}.png'); return f'{k}-{n}'
if __name__=='__main__':
    todo=[(v,n) for v in S if not ARGS or v[0] in ARGS for n in range(2)]
    with ThreadPoolExecutor(10) as ex: print(list(ex.map(go,todo)))
