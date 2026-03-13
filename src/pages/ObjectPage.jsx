import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useState } from 'react'
import objects from '../data/objects'
import ObjectCard from '../components/ObjectCard'

const fade = { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } }

const SpecRow = ({ label, value }) => (
  <div style={{
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'baseline',
    padding: '11px 0',
    borderBottom: 'var(--rule)',
  }}>
    <span className="label">{label}</span>
    <span style={{ fontSize: 13, letterSpacing: '0.03em' }}>{value}</span>
  </div>
)

export default function ObjectPage() {
  const { id } = useParams()
  const object = objects.find(o => o.id === id)
  const [activeColor, setActiveColor] = useState(null)

  if (!object) {
    return (
      <motion.div {...fade} className="page" style={{
        minHeight: '60vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 20,
      }}>
        <span className="label">Object not found</span>
        <Link to="/archive" className="label" style={{ color: 'var(--black)', borderBottom: 'var(--rule)', paddingBottom: 3 }}>
          Return to Archive →
        </Link>
      </motion.div>
    )
  }

  const [activeBase, setActiveBase] = useState('steel')

  const others = objects.filter(o => o.id !== object.id)
  const activeKey = activeColor ?? object.colors[0].key
  const hasBrass = !!object.images[`${object.colors[0].key}_brass`]
  const imageKey = activeBase === 'brass' ? `${activeKey}_brass` : activeKey
  const heroImage = object.images[imageKey] ?? object.images[activeKey] ?? object.images.hero

  return (
    <motion.div {...fade} transition={{ duration: 0.3 }}>

      {/* ── Dossier header ─────────────────────────────── */}
      <section style={{
        borderBottom: 'var(--rule)',
        padding: 'calc(var(--header-h) + 24px) var(--gutter) 20px',
      }}>
        <div style={{
          maxWidth: 'var(--max)',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
          flexWrap: 'wrap',
          gap: 12,
        }}>
          <div style={{ display: 'flex', gap: 20, alignItems: 'baseline' }}>
            <span className="label mono">Object {object.number}</span>
            <span className="label">{object.name}</span>
            <span className="label">{object.series}</span>
            <span className="label">{object.year}</span>
          </div>
          <Link to="/archive" className="label" style={{ color: 'var(--grey)', transition: 'color 0.2s' }}
            onMouseEnter={e => e.target.style.color = 'var(--black)'}
            onMouseLeave={e => e.target.style.color = 'var(--grey)'}
          >
            ← Archive
          </Link>
        </div>
      </section>

      {/* ── Hero image ─────────────────────────────────── */}
      <motion.section
        key={heroImage}
        initial={{ opacity: 0.7 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4 }}
      >
        <img
          src={heroImage}
          alt={`${object.name} — ${activeKey}`}
          style={{ width: '100%', height: '70vh', objectFit: 'cover', display: 'block' }}
        />
      </motion.section>

      {/* ── Dossier body ───────────────────────────────── */}
      <section style={{
        maxWidth: 'var(--max)',
        margin: '0 auto',
        padding: 'clamp(40px, 6vw, 80px) var(--gutter)',
      }}>
        <div className="col-2" style={{ alignItems: 'start' }}>

          {/* Left: object note + description */}
          <div>
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.1 }}
            >
              <span className="label" style={{ display: 'block', marginBottom: 14 }}>Object Note</span>
              <p style={{ fontSize: 'clamp(15px, 1.5vw, 18px)', lineHeight: 1.55, marginBottom: 28, whiteSpace: 'pre-line' }}>
                {object.note}
              </p>
              <p style={{ fontSize: 14, lineHeight: 1.7, color: 'var(--grey)', maxWidth: 480 }}>
                {object.description}
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.4, delay: 0.25 }}
              style={{ marginTop: 48 }}
            >
              <Link
                to="/inquiry"
                state={{ object: object.name }}
                style={{
                  display: 'inline-block',
                  padding: '12px 32px',
                  backgroundColor: 'var(--black)',
                  color: 'var(--white)',
                  fontSize: 11,
                  fontWeight: 700,
                  letterSpacing: '0.12em',
                  textTransform: 'uppercase',
                  transition: 'opacity 0.2s',
                }}
                onMouseEnter={e => e.target.style.opacity = 0.75}
                onMouseLeave={e => e.target.style.opacity = 1}
              >
                Request Inquiry
              </Link>
            </motion.div>
          </div>

          {/* Right: specs + colors */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.15 }}
          >
            <span className="label" style={{ display: 'block', marginBottom: 4 }}>Specifications</span>
            <SpecRow label="Series" value={object.series} />
            <SpecRow label="Year" value={object.year} />
            <SpecRow label="Dimensions" value={object.dimensions} />
            <SpecRow label="Weight" value={object.weight} />
            <SpecRow label="Materials" value={object.materials} />
            <SpecRow label="Base Materials" value={object.baseMaterials} />
            <SpecRow label="Status" value={object.status} />
            <SpecRow label="Edition" value={object.edition} />

            {/* Color variants */}
            <div style={{ marginTop: 40 }}>
              <span className="label" style={{ display: 'block', marginBottom: 16 }}>Color Variants</span>
              <div style={{ display: 'flex', gap: 16 }}>
                {object.colors.map(color => {
                  const isActive = activeKey === color.key
                  return (
                    <button
                      key={color.key}
                      onClick={() => setActiveColor(color.key)}
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        gap: 7,
                        padding: 0,
                        opacity: isActive ? 1 : 0.45,
                        transition: 'opacity 0.2s',
                      }}
                    >
                      <span style={{
                        width: 30,
                        height: 30,
                        backgroundColor: color.hex,
                        border: `${isActive ? 2 : 1}px solid ${isActive ? 'var(--black)' : 'var(--border)'}`,
                        display: 'block',
                      }} />
                      <span className="label" style={{ fontSize: 10 }}>{color.name}</span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Base selector */}
            {hasBrass && (
              <div style={{ marginTop: 32 }}>
                <span className="label" style={{ display: 'block', marginBottom: 16 }}>Base</span>
                <div style={{ display: 'flex', gap: 0, borderTop: 'var(--rule)' }}>
                  {['steel', 'brass'].map((base, i) => {
                    const isActive = activeBase === base
                    return (
                      <button
                        key={base}
                        onClick={() => setActiveBase(base)}
                        style={{
                          flex: 1,
                          padding: '10px 0',
                          borderBottom: isActive ? '2px solid var(--black)' : '1px solid var(--border)',
                          borderRight: i === 0 ? 'var(--rule)' : 'none',
                          fontSize: 11,
                          fontWeight: 700,
                          letterSpacing: '0.1em',
                          textTransform: 'uppercase',
                          color: isActive ? 'var(--black)' : 'var(--grey)',
                          transition: 'color 0.2s',
                          textAlign: 'center',
                        }}
                      >
                        {base === 'steel' ? 'Steel' : 'Brushed Brass'}
                      </button>
                    )
                  })}
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </section>

      {/* ── Variant image strip ────────────────────────── */}
      <section style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        borderTop: 'var(--rule)',
      }}>
        {object.colors.map((color, i) => (
          <motion.div
            key={color.key}
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: i * 0.07 }}
            style={{
              cursor: 'pointer',
              borderLeft: i > 0 ? 'var(--rule)' : 'none',
              opacity: activeKey === color.key ? 1 : 0.6,
              transition: 'opacity 0.3s',
            }}
            onClick={() => setActiveColor(color.key)}
          >
            <img
              src={object.images[activeBase === 'brass' ? `${color.key}_brass` : color.key] ?? object.images[color.key]}
              alt={`${object.name} — ${color.name}`}
              style={{ width: '100%', aspectRatio: '4/3', objectFit: 'cover', display: 'block' }}
              loading="lazy"
            />
            <div style={{ padding: '10px 14px', borderTop: 'var(--rule)' }}>
              <span className="label">{color.name}</span>
            </div>
          </motion.div>
        ))}
      </section>

      {/* ── Series note ────────────────────────────────── */}
      <section style={{
        borderTop: 'var(--rule)',
        padding: 'clamp(40px, 5vw, 70px) var(--gutter)',
        borderBottom: 'var(--rule)',
      }}>
        <div style={{
          maxWidth: 'var(--max)',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: '1fr 2fr',
          gap: 'clamp(40px, 6vw, 100px)',
        }}>
          <span className="label" style={{ paddingTop: 3 }}>Series Note</span>
          <p style={{ fontSize: 14, lineHeight: 1.7, color: 'var(--grey)', maxWidth: 500 }}>
            {object.seriesNote}
          </p>
        </div>
      </section>

      {/* ── Other objects ──────────────────────────────── */}
      {others.length > 0 && (
        <section>
          <div style={{
            maxWidth: 'var(--max)',
            margin: '0 auto',
            padding: '20px var(--gutter)',
            borderBottom: 'var(--rule)',
          }}>
            <span className="label">Other Objects in Series</span>
          </div>
          <div style={{ maxWidth: 'var(--max)', margin: '0 auto' }}>
            <div style={{
              display: 'grid',
              gridTemplateColumns: `repeat(${others.length}, 1fr)`,
            }}>
              {others.map((obj, i) => (
                <ObjectCard key={obj.id} object={obj} index={i} border={i > 0} />
              ))}
            </div>
          </div>
        </section>
      )}

    </motion.div>
  )
}
