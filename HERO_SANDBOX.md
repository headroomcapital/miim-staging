# MIIM Hero Sandbox

You are helping experiment with the **hero section** of the MIIM furniture studio website (`miim-v2`). This is a React + Vite app using Framer Motion.

## Task
Design and test different hero animation/layout ideas. Iterate freely — the user will pick what to keep.

---

## Tech stack
- React 18 + Vite
- Framer Motion (`motion`, `useScroll`, `useTransform`, `AnimatePresence`)
- No Tailwind — inline styles only
- Fonts: `TWK Everett Strong` (display/wordmark), `TWK Everett` (body)

## Brand tokens
```css
--yellow:       #D2FF00     /* neon yellow-green — the brand mark color */
--black:        #141414
--white:        #F7F7F2     /* warm off-white */
--border:       #CCCCC4
--font-display: 'TWK Everett Strong', 'TWK Everett', sans-serif
--font:         'TWK Everett', 'Helvetica Neue', sans-serif
--gutter:       clamp(20px, 4vw, 60px)
--max:          1440px
```

Hero background: `#ADADA5` (warm grey)

## CSS utilities available
```css
.label { font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 700; color: #141414; }
.mono  { font-variant-numeric: tabular-nums; letter-spacing: 0.04em; }
```

---

## Current Hero (from `miim-v2/src/pages/Home.jsx` — hero section only)

Visual: large yellow MIIM wordmark centered on warm grey (#ADADA5) hero. On scroll, the wordmark scales down and fades. Two small label lines sit at the bottom corners.

```jsx
import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'

const markStyle = {
  fontFamily: 'var(--font-display)',
  fontSize: 'clamp(86px, 24.3vw, 360px)',
  fontWeight: 500,
  lineHeight: 0.85,
  letterSpacing: '-0.02em',
  color: 'var(--yellow)',       /* #D2FF00 */
  textAlign: 'center',
  display: 'block',
  userSelect: 'none',
}

export default function Hero() {
  const heroRef = useRef(null)
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ['start start', 'end start'],
  })

  const scale   = useTransform(scrollYProgress, [0, 1], [1, 0.3])
  const opacity = useTransform(scrollYProgress, [0, 0.7, 1], [1, 1, 0])
  const y       = useTransform(scrollYProgress, [0, 1], [0, -80])

  return (
    <section
      ref={heroRef}
      style={{
        minHeight: '95vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        backgroundColor: '#ADADA5',
        overflow: 'hidden',
      }}
    >
      {/* Wordmark — scales down as user scrolls */}
      <motion.div style={{ scale, opacity, y, width: '100%' }}>
        <span style={markStyle}>MIIM</span>
      </motion.div>

      {/* Meta labels — bottom corners */}
      <div style={{
        position: 'absolute',
        bottom: 40,
        left: 0, right: 0,
        display: 'flex',
        justifyContent: 'space-between',
        padding: '0 var(--gutter)',
      }}>
        <span className="label">Amsterdam · 2026 · I-Series</span>
        <span className="label mono">001–003</span>
      </div>
    </section>
  )
}
```

---

## Design constraints
- **No scaling of elements during animation** — things appear/disappear, they don't grow or shrink
- **Grid-locked** — elements sit on fixed positions, no floating or drifting
- **Instant state changes** — `transition: 'none'` preferred, like a tile/game feel
- **MIIM wordmark stays readable** — yellow, centered
- The scroll-scale on the wordmark is fine to keep or remove
- Keep it tasteful and minimal — MIIM is a precise, architectural design studio

## Brand personality
MIIM is a furniture studio exploring **Spatial Harmony** and **Irrational Minimalism**. Objects produced in numbered series. Aesthetic is precise, architectural, quietly bold.

---

## Previously tried (all rejected as too busy)
1. Letterform tiles — M → II → M appearing sequentially, snapping to MIIM
2. Circle grid step sequencer — 8×5 grid of white circles blinking in rhythm patterns
3. 2×2 composition cycling — MI/IM stacked → M·II·M spread → MIIM tight

## Direction
Experiment freely. Some directions worth exploring:
- Very subtle — almost nothing, just a reveal or breath
- Typographic — working with the letterforms themselves
- Geometric — brand motif is circles and 2×2 grids
- Completely static — valid too, the wordmark alone is strong
