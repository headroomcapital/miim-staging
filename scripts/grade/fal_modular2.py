import sys; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OUT='/Users/headroom/Desktop/MIIM/directions/modular'
REFS=['out/miim-i-cobalt-brass.png','out/miim-i-yellow-steel.png','out/miim-i-stone-steel.png','out/miim-ii-yellow-aluminium.jpg','out/miim-ii-stone-aluminium.jpg']
REFTXT=("Reference images 1-5 are product photos of the exact tables to use: 1 = MIIM-I in Cobalt Blue with brushed brass legs, 2 = MIIM-I in Signal "
  "Yellow with brushed steel legs, 3 = MIIM-I in Stone with brushed steel legs, 4 = MIIM-II in Signal Yellow with aluminium leg, 5 = MIIM-II in Stone "
  "with aluminium leg. Copy their colours, materials and proportions exactly. ")
DIM=("PROPORTIONS: every MIIM-I top is 210 cm long and 100 cm wide (the length only just over twice the width - not long and narrow), 3.8 cm thick, "
  "on exactly two cylindrical legs 40 cm in diameter (two fifths of the top's width, so the top clearly overhangs each leg by 30 cm on both long "
  "sides), leg centres 52 cm in from each end, table height 76 cm. Every MIIM-II is a square top on one single centred 40 cm cylinder, the top two "
  "and a half times as wide as the leg. Legs are slender relative to the tops, never fat drums. ")
COL=("COLOURS: Cobalt Blue is a deep, dark ultramarine-indigo (#25227B), never a bright or light royal blue. Signal Yellow is an acid, slightly "
  "greenish lemon yellow (#DFE145), never golden or warm yellow. Stone is a warm putty beige (#DAD1C3), never white. Satin matte lacquer. ")
RULES=(" Soft, cool, neutral daylight, but a warm, lived-in, characterful space - not sterile. Table tops empty apart from what is named. No "
  "people, no text, no lettering, no logos, no books, no screens. Professional architectural interior photograph, razor-sharp, photorealistic.")
OFFICE=("A lived-in creative studio office in an old Amsterdam canal house: soft off-white lime-plaster walls (neutral, not green or yellow), wide old oak floorboards, tall "
  "windows with linen curtains. Three MIIM-I tables - each with TWO legs, none with one leg - spaced 1.5 metres apart in one straight line across the room as desks. Camera at standing eye level, square-on to the long sides of all three desks, so each desk's top is seen as a long rectangle and both of its legs are clearly visible, well apart, at a quarter and three quarters of its length. The swivel chairs stand on the far side of the desks, facing the camera, so they do not hide the legs - Cobalt Blue with brass legs, Signal Yellow with steel legs, Stone with "
  "steel legs - each with two Fritz Hansen Series 7 swivel chairs on castors in white and one small Louis Poulsen Panthella Mini lamp. Around them: a "
  "large potted olive tree, a big Monstera in a terracotta pot, a large abstract colour-field painting leaning against the wall, a low oak sideboard "
  "with a few hand-thrown ceramic vases, a woven wool rug under one desk. ")
CAFE=("A lived-in Scandinavian café with textured warm-white plaster walls, pale oak floorboards and tall windows. On one side a long oak counter with "
  "a chrome espresso machine (no branding), pastries under glass domes and stacked ceramic cups; open oak shelves with ceramics and a few plants; "
  "two Louis Poulsen PH5 pendants. Along the window a row of three MIIM-II tables (Signal Yellow, Stone, Signal Yellow) each with two Børge Mogensen "
  "J39 chairs; in the middle one MIIM-I in Cobalt Blue with brass legs used as a communal table with six Hans Wegner CH24 Wishbone chairs. A large "
  "fiddle-leaf fig in a corner, a framed abstract print on the wall. ")
EDIT=("Edit the FIRST image. Keep the camera, composition, room layout, window positions and chairs exactly as they are. Make three changes only: "
  "(1) recolour the table tops to the exact colours of the matching product references, (2) correct the tables' proportions as described, keeping "
  "their positions, (3) make the space feel warm and lived-in by adding plants, art and a few objects as described. ")
S=[
 ('v1',OFFICE,REFS[:3],3),
 ('v2',CAFE,REFS,3),
 ('v5',"Edit the FIRST image. Keep the camera, room, plants, art, chairs, lamps, colours and everything else exactly as they are. Change only "
   "the three tables' proportions: shorten each table so its top is 210 cm long and 100 cm wide - the length only just over twice the width - and "
   "make each of its two cylindrical legs slimmer, 40 cm in diameter, two fifths of the top's width, so the top clearly overhangs the legs, leg "
   "centres 52 cm in from each end. It must look like the same photograph. ",['/Users/headroom/Desktop/MIIM/directions/modular/v3-0.png'],2),
 ('v3',EDIT+"Add a large potted olive tree, a Monstera in a terracotta pot, a big abstract colour-field painting leaning on the wall, a low oak "
   "sideboard with ceramic vases and linen curtains. Tables: left = Cobalt Blue (reference 2), middle = Signal Yellow (reference 3), right = Stone "
   "(reference 4); keep the steel legs. ",[f'{OUT}/o2-0.png']+REFS[:3],2),
 ('v4',EDIT+"Add an oak café counter along the right wall with an unbranded espresso machine and ceramic cups, open shelves with ceramics, a "
   "fiddle-leaf fig, a framed abstract print and PH5 pendants. Tables: square ones = Stone and Signal Yellow (references 5 and 6), long one = Cobalt "
   "Blue with brass legs (reference 2). ",[f'{OUT}/m02-1.png']+REFS,2),
]
def go(a):
    (k,p,refs,_),n=a
    txt=(REFTXT if k in('v1','v2') else "The following reference images are product photos of the exact tables. ")+p+DIM+COL+RULES
    return call('fal-ai/nano-banana-pro/edit',{'prompt':txt,'image_urls':[uri(r) for r in refs],'num_images':1,'output_format':'png',
        'resolution':'4K','aspect_ratio':'16:9'},f'{OUT}/{k}-{n}.png')
todo=[(s,n+(6 if s[0]=='v1' else 0)) for s in S if not ARGS or s[0] in ARGS for n in range(s[3])]
with ThreadPoolExecutor(10) as ex: print(list(ex.map(go,todo)))
