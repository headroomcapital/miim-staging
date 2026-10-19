# Build a comparison board for a direction folder: web-sized images, table-drift check, prompts.
import sys,os,json,html; sys.path.insert(0,'.'); from common import *
D=sys.argv[1]; title=sys.argv[2]
HEX={'yellow':'#DFE145','stone':'#DAD1C3','cobalt':'#25227B','plum':'#502D38'}
def topmask(path,color):
    im=Image.open(path).convert('RGB'); im.thumbnail((900,900)); lab=rgb2lab(np.asarray(im,dtype=np.float32)/255)
    t=rgb2lab(np.array([int(HEX[color][i:i+2],16) for i in (1,3,5)],dtype=np.float32)/255)
    d=np.sqrt(((lab-t)*[0.5,1,1])**2).sum(-1)**0.5 if False else np.sqrt((((lab-t)*np.array([0.5,1,1]))**2).sum(-1))
    m=d<(14 if color!='stone' else 7); m=blur(m.astype(np.float32),2)>0.5
    ys,xs=np.nonzero(m); 
    if len(xs)<50: return None
    # largest blob only (rough): keep pixels near the median
    return (xs.max()-xs.min())/(ys.max()-ys.min()+1), m.mean()
entries=[]
for f in ('prompts.json','prompts2.json'):
    p=os.path.join(D,f)
    if os.path.exists(p):
        for e in json.load(open(p)):
            if not any(x['id']==e['id'] for x in entries): entries.append(e)
cards=[]
for e in entries:
    img=os.path.join(D,e['id']+'.png')
    if not os.path.exists(img): continue
    web=os.path.join(D,e['id']+'-web.jpg'); Image.open(img).convert('RGB').resize((1600,1200),Image.LANCZOS).save(web,quality=88)
    color=e['source'].split('-')[2] if e['source'].startswith('miim-i-') else e['source'].split('-')[2]
    src='/Users/headroom/Desktop/claude/miim-v2/scripts/grade/out/'+e['source']
    a,b=topmask(src,color),topmask(img,color)
    notes=json.load(open(os.path.join(D,'notes.json'))) if os.path.exists(os.path.join(D,'notes.json')) else {}
    if e['id'] in notes: flag,check=notes[e['id']]
    elif a and b:
        drift=abs(b[0]-a[0])/a[0]*100; check=f"Top outline ratio {a[0]:.2f} → {b[0]:.2f} ({drift:.0f}% drift)"
        flag='ok' if drift<12 else 'warn'
    else: check,flag='Top not measurable','warn'
    table=e['source'].replace('.png','').replace('.jpg','').replace('miim-ii','MIIM-II').replace('miim-i','MIIM-I').replace('-',' ',1).replace('-',' · ')
    cards.append(f"""<figure class="card"><img src="{e['id']}-web.jpg" alt="{html.escape(e['id'])}"><figcaption>
<div class="row"><b>{e['id'].upper()}</b><span>{html.escape(table)}</span></div>
<p class="check {flag}">{html.escape(check)}</p><p class="prompt">{html.escape(e['prompt'])}</p></figcaption></figure>""")
page=f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<style>@font-face{{font-family:Ev;src:url('/Users/headroom/Desktop/claude/miim-v2/public/fonts/TWKEverett-Bold.woff2')}}
:root{{--bg:#F7F7F2;--ink:#141414;--mut:#77756f;--rule:#CCCCC4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 Ev,'Helvetica Neue',sans-serif}}
header{{padding:28px 32px;border-bottom:1px solid var(--rule)}}h1{{margin:0;font-size:13px;letter-spacing:.14em;text-transform:uppercase}}header p{{margin:6px 0 0;color:var(--mut)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr))}}.card{{margin:0;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}}
.card img{{width:100%;display:block;aspect-ratio:4/3;object-fit:cover}}figcaption{{padding:14px 16px 18px}}.row{{display:flex;justify-content:space-between;font-size:11px;letter-spacing:.12em;text-transform:uppercase}}
.check{{font-size:11px;margin:8px 0 6px}}.check.ok{{color:#3d7a4f}}.check.warn{{color:#b5562a}}.prompt{{color:var(--mut);font-size:12px;margin:0}}
@media(max-width:480px){{.grid{{grid-template-columns:1fr}}header{{padding:20px 16px}}}}</style></head><body>
<header><h1>{html.escape(title)}</h1><p>Each scene edited from a graded MIIM product photo with fal nano-banana Pro (4K). G1–G4: empty rooms. G5–G8: with design classics as reference points. Green = table on-model, orange = table drifted.</p></header>
<main class="grid">{''.join(cards)}</main></body></html>"""
open(os.path.join(D,'board.html'),'w').write(page); print(len(cards),'cards ->',os.path.join(D,'board.html'))
