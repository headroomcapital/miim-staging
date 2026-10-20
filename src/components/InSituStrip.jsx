import { useEffect, useRef } from 'react'
import ResponsiveImage from './ResponsiveImage'

const SPEED = 30 // px per second
const RESUME_AFTER = 2500 // ms after the visitor stops interacting

// Endless horizontal strip: drifts slowly on its own, but is a native scroller,
// so visitors can swipe, drag-scroll or wheel through it at any time.
export default function InSituStrip({ items }) {
  const ref = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    let raf, last = performance.now(), pausedUntil = 0, hovering = false, pos = el.scrollLeft
    const half = () => el.scrollWidth / 2
    const tick = now => {
      const dt = Math.min(now - last, 64); last = now
      if (Math.abs(el.scrollLeft - pos) > 2) pos = el.scrollLeft   // follow any outside scroll (keys, scrollbar, momentum)
      if (!hovering && now > pausedUntil) {
        pos += (SPEED * dt) / 1000
        if (pos >= half()) pos -= half()
        el.scrollLeft = pos
      } else {
        pos = el.scrollLeft
        if (pos >= half()) { pos -= half(); el.scrollLeft = pos }
      }
      raf = requestAnimationFrame(tick)
    }
    const pause = () => { pausedUntil = performance.now() + RESUME_AFTER }
    let drag = null
    const down = e => {
      pause()
      if (e.pointerType !== 'mouse') return
      drag = { x: e.clientX, left: el.scrollLeft }
      el.setPointerCapture(e.pointerId); el.style.cursor = 'grabbing'
    }
    const move = e => {
      if (!drag) return
      let next = drag.left - (e.clientX - drag.x)
      if (next < 0) { next += half(); drag.left += half() }
      el.scrollLeft = next; pos = next; pause()
    }
    const up = () => { drag = null; el.style.cursor = '' }
    const enter = () => { hovering = true }
    const leave = () => { hovering = false; pause() }
    el.addEventListener('pointerdown', down)
    el.addEventListener('pointermove', move)
    el.addEventListener('pointerup', up)
    el.addEventListener('pointercancel', up)
    el.addEventListener('wheel', pause, { passive: true })
    el.addEventListener('touchstart', pause, { passive: true })
    el.addEventListener('mouseenter', enter)
    el.addEventListener('mouseleave', leave)
    raf = requestAnimationFrame(tick)
    return () => {
      cancelAnimationFrame(raf)
      el.removeEventListener('pointerdown', down)
      el.removeEventListener('pointermove', move)
      el.removeEventListener('pointerup', up)
      el.removeEventListener('pointercancel', up)
      el.removeEventListener('wheel', pause)
      el.removeEventListener('touchstart', pause)
      el.removeEventListener('mouseenter', enter)
      el.removeEventListener('mouseleave', leave)
    }
  }, [])

  return (
    <div ref={ref} className="insitu-strip" aria-label="MIIM objects in situ">
      <div className="insitu-track">
        {[...items, ...items].map((img, i) => (
          <figure key={i} className="insitu-item" aria-hidden={i >= items.length || undefined}>
            <ResponsiveImage
              src={img.src}
              widths={[640, 1280, 1920]}
              sizes="(max-width: 700px) 85vw, 34vw"
              alt={i < items.length ? img.alt : ''}
              style={{ width: '100%', aspectRatio: '4 / 3', objectFit: 'cover', display: 'block' }}
              loading="lazy"
              draggable={false}
            />
            <figcaption>
              <span className="label">{img.caption}</span>
              <span className="label" style={{ opacity: 0.6 }}>{img.credit}</span>
            </figcaption>
          </figure>
        ))}
      </div>
    </div>
  )
}
