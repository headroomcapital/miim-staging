import sharp from 'sharp'
import { readdir, mkdir } from 'fs/promises'
import { join, parse } from 'path'

const INPUT_DIR = 'public/images'
const OUTPUT_DIR = 'public/images/responsive'
const WIDTHS = [640, 1280, 1920]
const FORMATS = ['webp', 'jpg']

// Only process large hero/gallery images, skip small product shots
const LARGE_IMAGE_PATTERNS = [
  'cobalt-brass-home',
  'cobalt-brass-studio',
  'series-gallery3',
]

async function run() {
  await mkdir(OUTPUT_DIR, { recursive: true })

  const files = await readdir(INPUT_DIR)
  const targets = files.filter(f =>
    LARGE_IMAGE_PATTERNS.some(p => f.includes(p)) &&
    /\.(png|jpg|jpeg)$/i.test(f)
  )

  console.log(`Processing ${targets.length} images...`)

  for (const file of targets) {
    const { name } = parse(file)
    const input = join(INPUT_DIR, file)
    const img = sharp(input)
    const meta = await img.metadata()

    console.log(`  ${file} (${meta.width}x${meta.height})`)

    for (const w of WIDTHS) {
      if (w > meta.width) continue

      for (const fmt of FORMATS) {
        const outName = `${name}-${w}.${fmt}`
        const outPath = join(OUTPUT_DIR, outName)

        const pipeline = sharp(input).resize(w)

        if (fmt === 'webp') {
          pipeline.webp({ quality: 82 })
        } else {
          pipeline.jpeg({ quality: 85, mozjpeg: true })
        }

        await pipeline.toFile(outPath)
        const { size } = await sharp(outPath).metadata()
        console.log(`    -> ${outName}`)
      }
    }
  }

  console.log('Done.')
}

run().catch(console.error)
