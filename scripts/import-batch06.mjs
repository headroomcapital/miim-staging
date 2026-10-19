import sharp from 'sharp'
import { readdir, mkdir } from 'fs/promises'
import { join, parse } from 'path'

const SRC_DIR = '/Users/headroom/Desktop/MIIM/Batch06'
const PROJECT = '/Users/headroom/Desktop/claude/miim-v2'
const CANONICAL_DIR = join(PROJECT, 'public/images')
const RESPONSIVE_DIR = join(PROJECT, 'public/images/responsive')

const COLOR_MAP = { Blue: 'cobalt', Yellow: 'yellow', Taupe: 'stone', Purple: 'plum' }
const MAT_MAP   = { Messing: 'brass', Silver: 'steel' }
const VIEW_MAP  = { Angle: 'angle', Frontal: 'frontal' }

const WIDTHS = [640, 1280, 1920]
const CANONICAL_WIDTH = 1920

const re = /^MIIM_2Poot_Detail(Angle|Frontal)_(Blue|Yellow|Taupe|Purple)(Messing|Silver)\.png$/

function normalizedBase({ view, color, material }) {
  return `miim-i-${color}-${material}-detail-${view}`
}

async function run() {
  await mkdir(CANONICAL_DIR, { recursive: true })
  await mkdir(RESPONSIVE_DIR, { recursive: true })

  const files = await readdir(SRC_DIR)
  const targets = files.filter(f => re.test(f))
  console.log(`Found ${targets.length} source renders.\n`)

  for (const file of targets) {
    const m = file.match(re)
    const view     = VIEW_MAP[m[1]]
    const color    = COLOR_MAP[m[2]]
    const material = MAT_MAP[m[3]]
    const base     = normalizedBase({ view, color, material })
    const src      = join(SRC_DIR, file)
    const meta     = await sharp(src).metadata()

    console.log(`${file}`)
    console.log(`  → ${base}  (${meta.width}×${meta.height}, ${(meta.size / 1_000_000).toFixed(1)}MB)`)

    // Canonical JPG (highest responsive width)
    const canonicalOut = join(CANONICAL_DIR, `${base}.jpg`)
    await sharp(src).resize(CANONICAL_WIDTH).jpeg({ quality: 85, mozjpeg: true }).toFile(canonicalOut)
    console.log(`    canonical → public/images/${base}.jpg`)

    // Responsive variants
    for (const w of WIDTHS) {
      if (w > meta.width) continue
      for (const fmt of ['webp', 'jpg']) {
        const out = join(RESPONSIVE_DIR, `${base}-${w}.${fmt}`)
        const pipe = sharp(src).resize(w)
        if (fmt === 'webp') pipe.webp({ quality: 82 })
        else pipe.jpeg({ quality: 85, mozjpeg: true })
        await pipe.toFile(out)
      }
    }
    console.log(`    responsive → ${WIDTHS.join(', ')}w × webp+jpg\n`)
  }

  console.log('Done.')
}

run().catch(e => { console.error(e); process.exit(1) })
