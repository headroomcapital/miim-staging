// Jochem's Nov 2026 product set: miim-{i|ii}-{colour}-{brass|aluminium}-v2 (MIIM-II aluminium is -v3).
// Graded to one house standard first (scripts/grade/grade_v2.py): canonical = graded 1920 JPG, responsive from the graded 4K PNGs;
// wide hero variants built from the 4K PNGs by scripts/grade/extend_v2.py (WIDE_OUT=out/v2g-4k-wide, from the graded 4K), up to 4800 wide
// so large and retina screens aren't upscaling a 2880 file.
import sharp from 'sharp'
sharp.cache(false)
import { readdir, copyFile } from 'fs/promises'
import { join } from 'path'

const SRC = '/Users/headroom/Desktop/MIIM/site-jpg'
const PNG = { i: 'scripts/grade/out/v2g-4k', ii: 'scripts/grade/out/v2g-4k' }   // graded by scripts/grade/grade_v2.py
const WIDE = 'scripts/grade/out/v2g-4k-wide'
const IMG = 'public/images', RESP = 'public/images/responsive'

// Higher quality than the older imports: these photos are softer, and WebP q82 wipes out the brushing and grain.
const save = (pipe, out) => (out.endsWith('.webp') ? pipe.webp({ quality: 92, smartSubsample: true }) : pipe.jpeg({ quality: 90, mozjpeg: true })).toFile(out)

const files = (await readdir(SRC)).filter(f => /^miim-(i|ii)-\w+-(brass|aluminium)-v[23]\.jpg$/.test(f))
for (const f of files) {
  const base = f.replace(/\.jpg$/, '')
  const obj = base.startsWith('miim-ii-') ? 'ii' : 'i'
  await copyFile(join('scripts/grade/out/v2g', f), join(IMG, f))   // graded canonical (Jochem's originals stay in SRC)
  const png = join(PNG[obj], `${base}.png`)
  for (const w of [640, 1280, 1920])
    for (const fmt of ['webp', 'jpg']) await save(sharp(png).resize(w), join(RESP, `${base}-${w}.${fmt}`))
  const wide = join(WIDE, `${base}-wide.png`)
  await save(sharp(wide, { limitInputPixels: false }).resize(2880, 1200, { fit: 'fill' }), join(IMG, `${base}-wide.jpg`))
  for (const w of [1280, 1920, 2880, 3840, 4800])
    for (const fmt of ['webp', 'jpg']) await save(sharp(wide, { limitInputPixels: false }).resize(w, Math.round(w / 2.4), { fit: 'fill' }), join(RESP, `${base}-wide-${w}.${fmt}`))
  console.log(base)
}
