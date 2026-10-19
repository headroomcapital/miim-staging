# AI reference asset sheets: one per table x colour x base.
# Photo panels come from the graded renders; front/side/top views are drawn to scale from DIMS.
import sys, os; sys.path.insert(0, '.'); from leglib import *
from PIL import ImageDraw, ImageFont

FONTS = '/Users/headroom/Desktop/claude/miim-v2/public/fonts/'
BOLD = lambda s: ImageFont.truetype(FONTS + 'TWKEverett-Bold.woff2', s)
MED = lambda s: ImageFont.truetype(FONTS + 'MIIMEverett-strong.ttf', s)
OUTDIR = '/Users/headroom/Desktop/MIIM/asset-sheets'

DIMS = {  # mm. MIIM-I: fabrication drawing; spacing confirmed from render (~1080 measured)
    'miim-i':  dict(L=2100, W=1000, H=760, T=38, R=55, D=400, CC=1050, lift=5, legs=2),
    'miim-ii': None,  # awaiting dimensions
}
COLOR = {'yellow': ('Signal Yellow', '#DFE145'), 'stone': ('Stone', '#DAD1C3'),
         'cobalt': ('Cobalt Blue', '#25227B'), 'plum': ('Plum', '#502D38')}
METAL = {'steel': ('Steel', 'brushed', '#8F8B84'), 'aluminium': ('Aluminium', 'brushed', '#8F8B84'),
         'brass': ('Brass', 'brushed', '#9A8267')}
BG, INK, MUTED, RULE = (244, 243, 240), (20, 20, 20), (120, 118, 112), (204, 204, 196)

def hex2rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def shade(rgb, k): return tuple(int(max(0, min(255, c * k))) for c in rgb)

# real cylinder shading across the drum width, taken from the graded MIIM-II leg
_, abII, _ = np.load('matte_II.npy'); legII = max(legs(abII > 0.5), key=lambda m: m.sum())
PROF = {}
for m, ref in (('brass', 'brass'), ('steel', 'aluminium'), ('aluminium', 'aluminium')):
    lab = rgb2lab(np.asarray(Image.open(f'out/miim-ii-stone-{ref}.jpg').convert('RGB'), dtype=np.float32) / 255)
    PROF[m] = (np.clip(lab2rgb(profile(lab, legII)[0]), 0, 1) * 255).astype(np.uint8)  # (BINS,3)

SS = 3  # supersampling for clean edges

def drum(draw_img, x0, x1, y0, y1, metal):
    w = int(x1 - x0); h = int(y1 - y0)
    if w < 2 or h < 2: return
    prof = PROF[metal][np.linspace(0, BINS - 1, w).astype(int)].astype(np.float32)
    block = np.repeat(prof[None], h, 0)
    t = np.linspace(0, 1, h)[:, None, None]
    block *= 1 - 0.18 * np.exp(-t / 0.06)            # soft shadow under the tabletop
    draw_img.paste(Image.fromarray(block.clip(0, 255).astype(np.uint8)), (int(x0), int(y0)))

def dim_h(d, x0, x1, y, label, f):
    d.line([(x0, y), (x1, y)], fill=MUTED, width=SS)
    for x in (x0, x1): d.line([(x, y - 6 * SS), (x, y + 6 * SS)], fill=MUTED, width=SS)
    tw = d.textlength(label, font=f); d.rectangle([((x0 + x1) / 2 - tw / 2 - 8 * SS, y - 9 * SS), ((x0 + x1) / 2 + tw / 2 + 8 * SS, y + 9 * SS)], fill=BG)
    d.text(((x0 + x1) / 2, y), label, fill=MUTED, font=f, anchor='mm')

def dim_v(d, x, y0, y1, label, f):
    d.line([(x, y0), (x, y1)], fill=MUTED, width=SS)
    for y in (y0, y1): d.line([(x - 6 * SS, y), (x + 6 * SS, y)], fill=MUTED, width=SS)
    d.text((x + 12 * SS, (y0 + y1) / 2), label, fill=MUTED, font=f, anchor='lm')

def elevation(dims, top_rgb, metal, s, along):
    """Front (along='L') or side (along='W') elevation, s = px per mm (final)."""
    span = dims[along]; S = s * SS; pad = 70 * SS
    Wp = int(span * S + 2 * pad + 160 * SS); Hp = int(dims['H'] * S + pad + 110 * SS)
    img = Image.new('RGB', (Wp, Hp), BG); d = ImageDraw.Draw(img); f = MED(15 * SS)
    ox = pad; floor = pad + dims['H'] * S
    d.line([(ox - 40 * SS, floor), (ox + span * S + 40 * SS, floor)], fill=RULE, width=SS)
    under = floor - (dims['H'] - dims['T']) * S
    centres = [span / 2] if along == 'W' or dims['legs'] == 1 else [span / 2 - dims['CC'] / 2, span / 2 + dims['CC'] / 2]
    for c in centres:   # contact shadow
        cx = ox + c * S; sh = Image.new('L', img.size, 0); ImageDraw.Draw(sh).ellipse(
            [cx - dims['D'] * 0.62 * S, floor - 7 * SS, cx + dims['D'] * 0.62 * S, floor + 7 * SS], fill=70)
        img.paste(shade(BG, 0.82), mask=sh.filter(ImageFilter.GaussianBlur(9 * SS)))
    for c in centres:
        cx = ox + c * S
        drum(img, cx - dims['D'] / 2 * S, cx + dims['D'] / 2 * S, under, floor - dims['lift'] * S, metal)
    d.rectangle([ox, floor - dims['H'] * S, ox + span * S, under], fill=shade(top_rgb, 0.9))
    d.line([(ox, floor - dims['H'] * S), (ox + span * S, floor - dims['H'] * S)], fill=shade(top_rgb, 1.08), width=SS)
    dim_h(d, ox, ox + span * S, floor + 45 * SS, f"{span / 10:g} cm", f)
    dim_v(d, ox + span * S + 50 * SS, floor - dims['H'] * S, floor, f"{dims['H'] / 10:g} cm", f)
    if along == 'L' and dims['legs'] == 2:
        a, b = ox + centres[0] * S, ox + centres[1] * S
        dim_h(d, a, b, floor - dims['H'] * S - 28 * SS, f"{dims['CC'] / 10:g} cm c–c", f)
    x = ox + centres[0] * S
    dim_h(d, x - dims['D'] / 2 * S, x + dims['D'] / 2 * S, floor + 80 * SS, f"Ø {dims['D'] / 10:g} cm", f)
    return img.resize((Wp // SS, Hp // SS), Image.LANCZOS)

def plan(dims, top_rgb, s):
    S = s * SS; pad = 60 * SS
    Wp = int(dims['L'] * S + 2 * pad + 120 * SS); Hp = int(dims['W'] * S + 2 * pad + 40 * SS)
    img = Image.new('RGB', (Wp, Hp), BG); d = ImageDraw.Draw(img); f = MED(15 * SS)
    x0, y0 = pad, pad; x1, y1 = x0 + dims['L'] * S, y0 + dims['W'] * S
    d.rounded_rectangle([x0, y0, x1, y1], radius=dims['R'] * S, fill=top_rgb)
    centres = [dims['L'] / 2] if dims['legs'] == 1 else [dims['L'] / 2 - dims['CC'] / 2, dims['L'] / 2 + dims['CC'] / 2]
    line = shade(top_rgb, 0.7) if sum(top_rgb) > 300 else shade(top_rgb, 1.9)
    for c in centres:   # hidden drums, dashed
        cx, cy, r = x0 + c * S, (y0 + y1) / 2, dims['D'] / 2 * S
        for a in range(0, 360, 12): d.arc([cx - r, cy - r, cx + r, cy + r], a, a + 7, fill=line, width=2 * SS)
    dim_h(d, x0, x1, y1 + 40 * SS, f"{dims['L'] / 10:g} cm", f)
    dim_v(d, x1 + 40 * SS, y0, y1, f"{dims['W'] / 10:g} cm", f)
    return img.resize((Wp // SS, Hp // SS), Image.LANCZOS)

def fit(img, w, h):
    im = img.copy(); im.thumbnail((w, h), Image.LANCZOS); return im

def label(d, xy, text): d.text(xy, text.upper(), fill=MUTED, font=BOLD(17), spacing=4)

def sheet(model, color, metal):
    dims = DIMS[model]; W_, H_ = 3000, 2000; m = 70
    img = Image.new('RGB', (W_, H_), BG); d = ImageDraw.Draw(img)
    cname, chex = COLOR[color]; mname, finish, mhex = METAL[metal]; top_rgb = hex2rgb(chex)
    name = model.upper().replace('MIIM-', 'MIIM-')
    d.text((m, 52), f"{name}", fill=INK, font=BOLD(40))
    d.text((m + d.textlength(name, font=BOLD(40)) + 28, 60), f"{cname} top  ·  {mname} base", fill=INK, font=MED(30))
    d.text((W_ - m, 60), "REFERENCE SHEET — DRAWINGS TO SCALE", fill=MUTED, font=BOLD(18), anchor='ra')
    d.line([(m, 120), (W_ - m, 120)], fill=RULE, width=2)
    # hero photo
    photo = Image.open(f'out/{model}-{color}-{metal}.png' if model == 'miim-i' else f'out/{model}-{color}-{metal}.jpg').convert('RGB')
    hero = fit(photo, 1600, 1130); img.paste(hero, (m, 150)); label(d, (m, 150 + hero.height + 14), 'Three-quarter view · photo')
    # elevations, shared scale
    s = 0.43
    fe = elevation(dims, top_rgb, metal, s, 'L'); se = elevation(dims, top_rgb, metal, s, 'W')
    rx = m + 1600 + 50
    img.paste(fe, (rx, 150)); label(d, (rx + 20, 150 + fe.height - 4), 'Front elevation')
    img.paste(se, (rx, 150 + fe.height + 50)); label(d, (rx + 20, 150 + fe.height + 50 + se.height - 4), 'Side elevation')
    # bottom row
    by = 150 + hero.height + 70
    pl = plan(dims, top_rgb, 0.3); img.paste(pl, (m - 20, by)); label(d, (m + 40, by + pl.height + 4), 'Top view (drums dashed)')
    x = m + pl.width + 20
    if model == 'miim-i':
        for view in ('frontal', 'angle'):
            cu = fit(Image.open(f'out/{model}-{color}-{metal}-detail-{view}.png').convert('RGB'), 420, 420)
            img.paste(cu, (x, by)); label(d, (x, by + cu.height + 14), f'Detail · {"frontal" if view == "frontal" else "angled"}'); x += cu.width + 40
    # swatches + specs
    sx = max(x + 20, W_ - m - 640); sy = by
    for i, (title, hexv, sub) in enumerate(((f'Top — {cname}', chex, 'Lacquered MDF, satin'), (f'Base — {mname}', mhex, f'Solid cylinder, {finish}'))):
        y = sy + i * 120
        d.rectangle([sx, y, sx + 90, y + 90], fill=hex2rgb(hexv), outline=RULE)
        d.text((sx + 115, y + 8), title, fill=INK, font=MED(26)); d.text((sx + 115, y + 46), f'{sub}  ·  {hexv}', fill=MUTED, font=MED(20))
    rows = [('Dimensions', f"{dims['L']/10:g} × {dims['W']/10:g} × {dims['H']/10:g} cm"), ('Top thickness', f"{dims['T']/10:g} cm"),
            ('Corner radius', f"{dims['R']/10:g} cm"), ('Drum', f"Ø {dims['D']/10:g} cm" + (f", {dims['CC']/10:g} cm c–c" if dims['legs'] == 2 else ''))]
    ty = sy + 270
    for k, v in rows:
        d.line([(sx, ty), (W_ - m, ty)], fill=RULE, width=2)
        d.text((sx, ty + 14), k.upper(), fill=MUTED, font=BOLD(17)); d.text((W_ - m, ty + 12), v, fill=INK, font=MED(22), anchor='ra')
        ty += 54
    d.line([(sx, ty), (W_ - m, ty)], fill=RULE, width=2)
    os.makedirs(OUTDIR, exist_ok=True)
    out = f'{OUTDIR}/{model}-{color}-{metal}-sheet.png'; img.save(out); return out

if __name__ == '__main__':
    jobs = [a.split(':') for a in sys.argv[1:]] or [('miim-i', c, m) for c in COLOR for m in ('steel', 'brass')]
    for model, c, m in jobs: print(sheet(model, c, m))
