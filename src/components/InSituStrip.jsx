import { useEffect, useRef } from 'react'
import ResponsiveImage from './ResponsiveImage'

const SPEED = 45 // px per second
const RESUME_AFTER = 2500 // ms after the visitor stops interacting

// Endless horizontal strip: drifts slowly on its own, but is a native scroller,
// so visitors can swipe, drag-scroll, wheel or step through it with the arrows.
export default function InSituStrip({ items, label }) {
  const ref = useRef(null)
  const stepRef = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const half = () => el.scrollWidth / 2
    let pausedUntil = 0
    const pause = () => { pausedUntil = performance.now() + RESUME_AFTER }
    // One image per click. Jump to the identical copy first so the smooth scroll never crosses the loop seam.
    // Rapid clicks build on the previous target rather than the mid-animation position.
    let target = 0, targetAt = 0
    stepRef.current = dir => {
      pause()
      const w = el.querySelector('.insitu-item')?.offsetWidth ?? el.clientWidth
      let left = performance.now() - targetAt < 700 ? target : el.scrollLeft
      if (dir > 0 && left + w >= half()) left -= half()
      if (dir < 0 && left - w < 0) left += half()
      el.scrollLeft = left
      target = left + dir * w; targetAt = performance.now()
      el.scrollTo({ left: target, behavior: reduced ? 'auto' : 'smooth' })
    }
    if (reduced) return
    let raf, last = performance.now(), hovering = false, pos = el.scrollLeft
    const tick = now => {
      const dt = Math.min(now - last, 64); last = now
      if (Math.abs(el.scrollLeft - pos) > 2) pos = el.scrollLeft   // follow any outside scroll (keys, scrollbar, momentum)
      if (!hovering && now > pausedUntil) {
        pos += (SPEED * dt) / 1000
        if (pos >= half()) pos -= half()
        el.scrollLeft = pos
      } else {
        pos = el.scrollLeft
        // don't wrap while an arrow step is still animating, or it would cancel the step
        if (pos >= half() && now - targetAt > 800) { pos -= half(); el.scrollLeft = pos }
      }
      raf = requestAnimationFrame(tick)
    }
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
    <>
    <div className="insitu-head">
      <span className="label">{label}</span>
      <div>
        <button className="label insitu-arrow" aria-label="Previous image" onClick={() => stepRef.current?.(-1)}>←</button>
        <button className="label insitu-arrow" aria-label="Next image" onClick={() => stepRef.current?.(1)}>→</button>
      </div>
    </div>
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
    </>
  )
}
