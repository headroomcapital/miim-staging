import sys; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OUT='/Users/headroom/Desktop/MIIM/directions/modular'; PI='../../public/images/'
REAL=[PI+'miim-i-stone-steel-insitu-canal.jpg',PI+'miim-i-plum-brass-insitu-paris-v2.jpg']
PHOTO=("A real documentary interior photograph, NOT a 3D render: shot at eye level (camera 140 cm high) with a 35 mm lens, natural overcast daylight from "
  "windows on one side only, so the room is clearly brighter near the windows and falls off into softer, darker areas away from them; real contact "
  "shadows under every table leg and chair foot; honest everyday surfaces - slightly worn floorboards with fine gaps and scuffs, limewashed walls with "
  "subtle unevenness, old cast-iron radiators under the windows, a power socket; fine film grain, slight lens vignetting, neutral cool colour. Match the "
  "photographic realism, light and colour of the LAST TWO reference images exactly.")
TABLE=("The tables must look exactly like the product reference photographs (first reference images) in colour, finish and proportion. "
  "MIIM-I: 210 cm long, 100 cm wide, 75 cm high, top 3.8 cm thick lacquer, on TWO cylinders each 40 cm in diameter with centres 105 cm apart - "
  "so the cylinders are clearly narrower than the table width and there is a wide open space between them. MIIM-II: square 80 x 80 cm top, 75 cm high, "
  "on ONE 32 cm cylinder under the centre. Chair seats are 45 cm high, so table tops are well above the seats. Lacquer colours: Signal Yellow is a cool "
  "lemon yellow, Cobalt Blue is a deep dark ultramarine (not bright royal blue), Stone is a warm pale greige. Satin brushed steel or satin champagne "
  "brass. Table tops empty except where stated. No people, no text, no logos, no screens, no books.")
S=[
 ('p1',[PI+'miim-i-cobalt-steel.jpg',PI+'miim-i-yellow-steel.jpg',PI+'miim-i-stone-steel.jpg'],
  "A small architecture office in an old Copenhagen apartment: three MIIM-I tables used as desks, placed in one row end to end with a small gap, tops in "
  "cobalt blue, signal yellow and stone, brushed steel legs. At each desk one white Fritz Hansen Series 7 swivel chair on castors, and one Louis "
  "Poulsen Panthella table lamp on each desk. Seen from the side of the room at a slight diagonal so all three desks and their legs are clearly visible."),
 ('p2',[PI+'miim-ii-stone-aluminium-v2.jpg',PI+'miim-ii-yellow-aluminium-v2.jpg',PI+'miim-i-cobalt-brass.jpg'],
  "A neighbourhood café-bakery in an old Copenhagen building: along the windows two MIIM-II tables in stone and signal yellow with brushed aluminium "
  "legs, each with two Børge Mogensen J39 chairs; in the middle of the room one MIIM-I in cobalt blue with champagne brass legs used as a communal "
  "table with Hans Wegner CH24 Wishbone chairs. A simple wooden counter with a glass cake dome far in the background, slightly out of focus."),
]
def go(a):
    (k,refs,p),n=a
    return call('fal-ai/nano-banana-pro/edit',{'prompt':p+' '+TABLE+' '+PHOTO,'image_urls':[uri(r) for r in refs+REAL],'num_images':1,
        'output_format':'png','resolution':'4K','aspect_ratio':'3:2'},f'{OUT}/{k}-{n}.png')
with ThreadPoolExecutor(8) as ex: print(list(ex.map(go,[(s,n) for s in S if not ARGS or s[0] in ARGS for n in range(4)])))
