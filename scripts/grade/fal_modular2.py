import sys; ARGS=sys.argv[1:]; sys.argv=['x']
from fal_gen import uri, call
from concurrent.futures import ThreadPoolExecutor
OUT='/Users/headroom/Desktop/MIIM/directions/modular'; PI='../../public/images/'
REAL=PI+'miim-i-stone-steel-insitu-canal.jpg'
DIM=("Exact real-world dimensions: MIIM-I is 210 cm long, 100 cm wide, 75 cm high, top 3.8 cm thick, two legs each 40 cm in diameter with centres "
     "105 cm apart (at one quarter and three quarters of the length) - so the legs are slim relative to the long top, with a wide open gap between them. "
     "MIIM-II has an 80 x 80 cm square top, 75 cm high, on one 32 cm diameter leg exactly under the centre. Table tops sit just above the chair "
     "armrests / a hand's width above the seats (chair seats are 45 cm high).")
COL=("Match the lacquer colours EXACTLY to the product reference photographs: Signal Yellow is a cool, slightly green-leaning lemon yellow (not golden), "
     "Cobalt Blue is a deep, dark ultramarine-indigo (not bright royal blue), Stone is a warm pale greige. Matte satin lacquer. Legs are satin brushed "
     "stainless steel (soft, low-contrast, not mirror-chrome) or satin brushed champagne brass.")
REALISM=("It must look like a REAL photograph shot by an interiors photographer, exactly like the LAST reference image in realism: natural daylight "
     "with real falloff and soft bounce, realistic contact shadows under every leg and chair foot, subtle floor reflections, slight imperfections in "
     "plaster and wood, gentle lens vignetting and fine grain, nothing CGI-perfect. Table tops empty except where stated. No people, no text, no logos.")
S=[
 ('n1',f'{OUT}/o2-0.png',[PI+'miim-i-cobalt-steel.jpg',PI+'miim-i-yellow-steel.jpg',PI+'miim-i-stone-steel.jpg'],
  "Re-photograph the scene of the FIRST image as a real photograph: the same Scandinavian office, the same three MIIM-I desks in a row in cobalt, "
  "signal yellow and stone with steel legs, the same white Fritz Hansen Series 7 swivel chairs on castors and Louis Poulsen Panthella lamps, same "
  "camera angle. Correct the tables to look exactly like the MIIM-I in the product reference images (images 2-4) for proportions and colour."),
 ('n2',f'{OUT}/m02-1.png',[PI+'miim-ii-stone-aluminium.jpg',PI+'miim-ii-yellow-aluminium.jpg',PI+'miim-i-cobalt-brass.jpg'],
  "Re-photograph the scene of the FIRST image as a real photograph: the same Scandinavian café, along the window three MIIM-II tables (square tops on "
  "one centred leg) in stone, signal yellow and stone with brushed aluminium legs and Børge Mogensen J39 chairs, and one long cobalt MIIM-I with "
  "brushed brass legs and Hans Wegner CH24 Wishbone chairs. Same camera angle. Correct the tables to look exactly like the product reference images "
  "(images 2-4) for proportions and colour: the MIIM-II tops are truly square."),
]
def go(a):
    (k,base,refs,p),n=a
    return call('fal-ai/nano-banana-pro/edit',{'prompt':p+' '+DIM+' '+COL+' '+REALISM,'image_urls':[uri(base)]+[uri(r) for r in refs]+[uri(REAL)],
        'num_images':1,'output_format':'png','resolution':'4K','aspect_ratio':'16:9'},f'{OUT}/{k}-{n}.png')
with ThreadPoolExecutor(8) as ex: print(list(ex.map(go,[(s,n) for s in S if not ARGS or s[0] in ARGS for n in range(3)])))
