# 20 in-situ scenes. House rules: cool neutral daylight, empty top, real designer pieces, no text/books, table exact.
import sys,os,json; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OUT='/Users/headroom/Desktop/MIIM/directions/series20'
T1=("the exact table from the reference image, MIIM-I: a long rectangular {top} lacquered top, 3.8 cm thick with tight corners, on two wide cylindrical "
    "legs of satin brushed {base}; each leg diameter about one fifth of the table length; leg centres at one quarter and three quarters of the length, "
    "equal overhang at both ends")
T2=("the exact table from the reference image, MIIM-II: a SQUARE {top} lacquered top with softly rounded corners, 3.8 cm thick, on ONE single wide "
    "cylindrical leg of satin brushed {base} standing exactly under the centre, the top about two and a half times as wide as the leg")
RULES=(" The tabletop is completely empty. Soft, cool, neutral daylight like a bright overcast morning, no golden or amber cast. Reproduce the named design "
       "pieces faithfully and recognisably. No books, no magazines, no posters, no text, lettering or logos anywhere. No people. Professional architectural "
       "interior photograph, medium-format camera, razor-sharp, photorealistic, natural materials.")
TOP={'stone':'stone off-white','yellow':'signal yellow','cobalt':'deep cobalt blue','plum':'deep wine plum'}
BASE={'steel':'stainless steel','aluminium':'aluminium','brass':'champagne brass'}
S=[
 # MIIM-I (two legs)
 ('s01','i','stone','steel',"A white-plastered Amsterdam canal-house dining room with tall sash windows and wide oak floorboards. Four Hans Wegner CH24 Wishbone chairs in natural oak. A Louis Poulsen PH5 pendant in white above the table.",'4:3'),
 ('s02','i','cobalt','brass',"A Belgian brick-and-limewash farmhouse kitchen-diner, grey bluestone floor, steel-framed window. Four Pierre Jeanneret Office Cane chairs in teak, two on each long side, set back so that BOTH cylindrical legs are clearly visible. A three-quarter view showing the full length of the table. An Isamu Noguchi Akari 75A paper lantern above.",'4:3'),
 ('s03','i','yellow','steel',"A minimal concrete loft with a polished concrete floor and a long ribbon window. Six Arne Jacobsen Series 7 chairs in black. Two Flos IC Lights S pendants in brushed steel above the table.",'16:9'),
 ('s04','i','plum','brass',"A Parisian Haussmann apartment with herringbone parquet, wall mouldings in soft grey, tall French windows with sheer linen. Four Marcel Breuer Cesca chairs with cane seats. A Flos Arco floor lamp arching over.",'4:3'),
 ('s05','i','stone','brass',"A Japanese-inspired dining room with pale cedar slat walls, tatami-toned floor, shoji screen windows. Four authentic George Nakashima Conoid chairs in walnut (cantilevered sled base, tall spindle back). The table is 210 cm long by 100 cm deep, not overly long. A large Noguchi Akari lantern above.",'4:3'),
 ('s06','i','cobalt','steel',"A white gallery-like dining space with a terrazzo floor and large steel windows. Four Charles and Ray Eames DSW chairs in white with oak legs. A Vitra Akari-style pleated pendant.",'16:9'),
 ('s07','i','yellow','brass',"A Scandinavian dining room with whitewashed pine floors, pale grey walls, large window onto birch trees. Four Alvar Aalto Chair 69 in natural birch. An Artek A110 Hand Grenade pendant in brass.",'4:3'),
 ('s08','i','plum','steel',"A converted industrial studio, white-painted brick walls, grey epoxy floor, large factory windows. Four Jean Prouvé Standard chairs, black steel with oak. A black Serge Mouille three-arm ceiling light.",'16:9'),
 ('s09','i','stone','steel',"A modernist villa dining area with floor-to-ceiling glass onto a garden, travertine floor. Four Mies van der Rohe MR10 cantilever chairs in chrome and natural leather. A Poul Henningsen PH Artichoke pendant in copper.",'16:9'),
 ('s10','i','cobalt','brass',"A calm Milanese apartment, parquet floor, pale plaster walls, tall window. Four Gio Ponti Superleggera chairs in white with natural rush seats. A Flos Taccia lamp on a low sideboard.",'4:3'),
 # MIIM-II (one leg)
 ('s11','ii','plum','brass',"A small kitchen corner with terracotta floor tiles and whitewashed walls, window on the left. Two Thonet No. 14 bentwood chairs in dark walnut. A George Nelson Bubble lamp above.",'4:3'),
 ('s12','ii','cobalt','aluminium',"A bright breakfast nook, pale oak floor, white walls, window with a radiator below. Two Alvar Aalto Chair 66 in natural birch with black seats. An Artek Golden Bell pendant in brass.",'4:3'),
 ('s13','ii','yellow','aluminium',"A white concrete studio corner with a polished concrete floor and a steel window. Two Arne Jacobsen Series 7 chairs in white. A Gras N°302 wall lamp in black on the wall.",'4:3'),
 ('s14','ii','stone','brass',"A Parisian salon corner with herringbone oak floor and grey wall mouldings, tall window with linen curtains. Two Pierre Jeanneret Chandigarh chairs in teak and cane. A Louis Poulsen PH5 pendant in white above.",'4:3'),
 ('s15','ii','plum','aluminium',"A minimal Japanese room, pale wood floor, washi paper sliding doors, a single ikebana branch on the floor in a far corner. Two Hans Wegner CH24 Wishbone chairs in oak. A Noguchi Akari 45A lantern above.",'4:3'),
 ('s16','ii','cobalt','brass',"A gallery corner with white walls and a pale microcement floor, cool skylight. Two Mario Bellini CAB chairs in black leather. An Isamu Noguchi Akari 10A floor lamp beside.",'4:3'),
 ('s17','ii','yellow','brass',"A Scandinavian café corner, light grey walls, pale ash floorboards, window onto the street. Two Børge Mogensen J39 chairs in natural oak with paper-cord seats. A Louis Poulsen PH 3/2 pendant above.",'4:3'),
 ('s18','ii','stone','aluminium',"A brutalist board-marked concrete room, cool daylight through a slot window, honed concrete floor. Two Jean Prouvé Standard chairs, black steel and oak. A Flos IC Lights S1 pendant above.",'4:3'),
 ('s19','ii','cobalt','aluminium',"A Mediterranean whitewashed room with a terracotta floor and a deep-set wooden window. Two Gio Ponti Superleggera chairs in black. A large Noguchi Akari 55A lantern above.",'4:3'),
 ('s20','ii','plum','brass',"A modernist apartment corner with a terrazzo floor and white walls, large window. Two Charles and Ray Eames DSW chairs in white with walnut legs. An Arco floor lamp arching over the table.",'4:3'),
 ('s21','i','stone','steel',"A calm architecture-office meeting room: white walls, grey linoleum floor, a large steel-framed window over the city, a plain white pinboard with blank sheets of paper. Six Vitra Eames Aluminium Group EA 108 chairs in black leather. Two Flos Aim pendants above.",'16:9'),
 ('s22','i','cobalt','aluminium' if False else 'steel',"A design-studio workspace in a converted warehouse, whitewashed brick, polished concrete floor, tall factory windows. The table used as a large shared desk with four Vitra Tip Ton chairs in grey and a Tolomeo desk lamp by Artemide. A blank cork board on the wall.",'16:9'),
 ('s23','ii','plum','brass',"A small private office in a Haussmann building: herringbone parquet, pale grey mouldings, tall window. The table used as a desk with one Pierre Jeanneret Office Cane chair in teak and an Anglepoise Type 75 lamp in black.",'4:3'),
 ('s24','ii','yellow','aluminium',"A bright creative-agency meeting corner: white walls, light oak floor, glass partition in the background, a whiteboard with no writing. Two Hay About A Chair AAC22 in white. A Louis Poulsen PH 3/2 pendant above.",'4:3'),
]
def go(v):
    k,m,top,base,scene,ar=v
    ref=f"out/miim-{m}-{top}-{base}.{'png' if m=='i' else 'jpg'}"
    tbl=(T1 if m=='i' else T2).format(top=TOP[top],base=BASE[base])
    p=scene+" In the room stands "+tbl+"."+RULES
    call('fal-ai/nano-banana-pro/edit',{'prompt':p,'image_urls':[uri(ref)],'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':ar},f'{OUT}/{k}.png')
    return k
if __name__=='__main__':
    sel=ARGS or None
    todo=[v for v in S if not sel or v[0] in sel]
    with ThreadPoolExecutor(10) as ex: print(list(ex.map(go,todo)))
    json.dump([{'id':k,'source':f"miim-{m}-{t}-{b}.{'png' if m=='i' else 'jpg'}",'prompt':sc} for k,m,t,b,sc,ar in S],open(f'{OUT}/prompts.json','w'),indent=1)
