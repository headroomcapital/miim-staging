import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion'
import { Link } from 'react-router-dom'
import { useRef, useState, useEffect } from 'react'
import ObjectCard from '../components/ObjectCard'
import ShapeGrid from '../components/ShapeGrid'
import objects from '../data/objects'

const fade = { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } }

const markStyle = {
  fontFamily: 'var(--font-display)',
  fontSize: 'clamp(86px, 24.3vw, 360px)',
  fontWeight: 500,
  lineHeight: 0.85,
  letterSpacing: '-0.02em',
  color: 'var(--yellow)',
  textAlign: 'center',
  display: 'block',
  userSelect: 'none',
}


export default function Home() {
  const heroRef = useRef(null)
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ['start start', 'end start'],
  })

  const scale   = useTransform(scrollYProgress, [0, 1], [1, 0.3])
  const opacity = useTransform(scrollYProgress, [0, 0.7, 1], [1, 1, 0])
  const y       = useTransform(scrollYProgress, [0, 1], [0, -80])

  return (
    <motion.div {...fade} transition={{ duration: 0.3 }}>

      {/* ── Hero ───────────────────────────────────────── */}
      <section
        ref={heroRef}
        style={{
          minHeight: '95vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          backgroundColor: '#A0A096',
          overflow: 'hidden',
          gap: 0,
          isolation: 'isolate',
        }}
      >
        {/* Shape wallpaper — edge-to-edge, no gaps */}
        <ShapeGrid color="#C2C2BA" />

        <motion.div style={{ scale, opacity, y, width: '100%', position: 'relative', zIndex: 1, pointerEvents: 'none' }}>
          <span style={markStyle}>MIIM</span>
        </motion.div>

        {/* Meta labels */}
        <div style={{
          position: 'absolute',
          bottom: 40,
          left: 0, right: 0,
          display: 'flex',
          justifyContent: 'space-between',
          padding: '0 var(--gutter)',
        }}>
          <motion.span
            className="label"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.4 }}
          >
            Amsterdam · 2026 · I-Series
          </motion.span>
          <motion.span
            className="label mono"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.5 }}
          >
            001–003
          </motion.span>
        </div>
      </section>

      {/* ── Object Archive ─────────────────────────────── */}
      <section style={{ borderTop: 'var(--rule)' }}>
        <div style={{
          maxWidth: 'var(--max)',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
          padding: '20px var(--gutter)',
          borderBottom: 'var(--rule)',
        }}>
          <span className="label">Object Archive / I-Series / {objects.length} Objects</span>
          <Link to="/archive" className="label" style={{ color: 'var(--black)', transition: 'opacity 0.2s' }}
            onMouseEnter={e => e.target.style.opacity = 0.5}
            onMouseLeave={e => e.target.style.opacity = 1}
          >
            View all →
          </Link>
        </div>

        <div style={{ maxWidth: 'var(--max)', margin: '0 auto' }}>
          <div className="object-grid">
            {objects.map((obj, i) => (
              <ObjectCard key={obj.id} object={obj} index={i} border={i > 0} />
            ))}
          </div>
        </div>
      </section>

      {/* ── Manifesto ──────────────────────────────────── */}
      <section style={{
        backgroundColor: 'var(--dark)',
        padding: 'clamp(60px, 10vw, 120px) var(--gutter)',
      }}>
        <div style={{ maxWidth: 800, margin: '0 auto' }}>
          <motion.p
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.5 }}
            style={{
              color: 'var(--white)',
              fontSize: 'clamp(18px, 2.5vw, 28px)',
              lineHeight: 1.5,
              fontWeight: 700,
            }}
          >
            MIIM explores furniture through Spatial Harmony — the relationship between structure, proportion, and the space an object occupies.
          </motion.p>
          <motion.p
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.5, delay: 0.1 }}
            style={{
              color: 'var(--white)',
              fontSize: 'clamp(15px, 1.8vw, 20px)',
              lineHeight: 1.6,
              marginTop: 28,
              opacity: 0.75,
            }}
          >
            Rather than designing isolated pieces, objects are developed as part of a series. Each object emerges from the same structural idea while varying in dimension, surface, and scale.
          </motion.p>
          <motion.p
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.5, delay: 0.15 }}
            style={{
              color: 'var(--white)',
              fontSize: 'clamp(15px, 1.8vw, 20px)',
              lineHeight: 1.6,
              marginTop: 20,
              opacity: 0.75,
            }}
          >
            This approach reflects what we call Irrational Minimalism: a balance between mathematical clarity and intuitive judgment. Proportions are calculated, but the final object is guided by instinct — producing forms that feel simple, balanced, and inevitable within a space.
          </motion.p>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: 0.2 }}
            style={{ marginTop: 40 }}
          >
            <Link
              to="/studio"
              className="label"
              style={{ color: 'var(--grey)', borderBottom: '1px solid var(--grey)', paddingBottom: 3, transition: 'color 0.2s, border-color 0.2s' }}
              onMouseEnter={e => { e.target.style.color = 'var(--white)'; e.target.style.borderColor = 'var(--white)' }}
              onMouseLeave={e => { e.target.style.color = 'var(--grey)'; e.target.style.borderColor = 'var(--grey)' }}
            >
              Studio →
            </Link>
          </motion.div>
        </div>
      </section>

      {/* ── Series Statement ───────────────────────────── */}
      <section style={{
        padding: 'clamp(60px, 8vw, 100px) var(--gutter)',
        borderBottom: 'var(--rule)',
      }}>
        <div style={{
          maxWidth: 'var(--max)',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: '1fr 2fr',
          gap: 'clamp(40px, 6vw, 120px)',
          alignItems: 'start',
        }}>
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
          >
            <span className="label" style={{ display: 'block', marginBottom: 12 }}>Series</span>
            <p style={{ fontSize: 'clamp(20px, 2.5vw, 28px)', lineHeight: 1.2 }}>
              I-Series
            </p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <p style={{
              fontSize: 'clamp(15px, 1.5vw, 18px)',
              lineHeight: 1.65,
              color: 'var(--grey)',
              maxWidth: 540,
            }}>
              The I-Series studies a single spatial proposition:<br />
              a horizontal surface supported by two vertical cylinders.<br /><br />
              The cylinders remain constant.<br />
              The surface changes in scale and proportion.<br /><br />
              Individually, each object completes a space.<br />
              Together, the objects reveal the system behind them.
            </p>
            <div style={{ marginTop: 32 }}>
              <Link
                to="/archive"
                className="label"
                style={{ color: 'var(--black)', borderBottom: '1px solid var(--border)', paddingBottom: 3, transition: 'border-color 0.2s' }}
                onMouseEnter={e => e.target.style.borderColor = 'var(--black)'}
                onMouseLeave={e => e.target.style.borderColor = 'var(--border)'}
              >
                View Archive →
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── Full-width image ───────────────────────────── */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.7 }}
      >
        <img
          src="/images/miim-i-series-gallery.png"
          alt="MIIM I-Series detail"
          style={{ width: '100%', height: 'auto', display: 'block' }}
          loading="lazy"
        />
      </motion.section>

      {/* ── CTA ────────────────────────────────────────── */}
      <Link to="/inquiry" style={{ display: 'block' }}>
        <div style={{
          backgroundColor: 'var(--yellow)',
          padding: 'clamp(40px, 5vw, 70px) var(--gutter)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <span className="label">Interested in an object or commission?</span>
          <span style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(28px, 5vw, 64px)',
            fontWeight: 500,
            letterSpacing: '-0.01em',
            lineHeight: 1,
          }}>
            INQUIRY →
          </span>
        </div>
      </Link>

    </motion.div>
  )
}
