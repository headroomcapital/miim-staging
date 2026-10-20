import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useState } from 'react'
import objects from '../data/objects'
import ResponsiveImage from '../components/ResponsiveImage'


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

  const bases = object.bases ?? [{ key: 'steel', label: 'Steel' }, { key: 'brass', label: 'Brushed Brass' }]
  const [activeBase, setActiveBase] = useState(bases[0].key)
  const baseLabel = bases.find(b => b.key === activeBase)?.label

  const activeKey = activeColor ?? object.colors[0].key
  const imgKey = (color, base) => base === bases[0].key ? color : `${color}_${base}`
  const hasBrass = bases.length > 1 && !!object.images[imgKey(object.colors[0].key, bases[1].key)]
  const imageKey = imgKey(activeKey, activeBase)
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
        {/* Wide variant (backdrop extended) fills any screen shape; height never exceeds the
            original photo's proportion, so cropping only ever removes backdrop, not the table. */}
        <picture>
          {/* Portrait screens show the original framing, so they get the regular photo */}
          <source
            media="(max-aspect-ratio: 1/1)"
            type="image/webp"
            sizes="100vw"
            srcSet={[640, 1280, 1920].map(w => `${heroImage.replace('/images/', '/images/responsive/').replace(/\.jpg$/, '')}-${w}.webp ${w}w`).join(', ')}
          />
          <source
            type="image/webp"
            sizes="170vw"
            srcSet={[1280, 1920, 2880].map(w => `${heroImage.replace('/images/', '/images/responsive/').replace(/\.jpg$/, '')}-wide-${w}.webp ${w}w`).join(', ')}
          />
          <img
            src={heroImage.replace(/\.jpg$/, '-wide.jpg')}
            alt={`${object.name} — ${activeKey}`}
            style={{
              width: '100%',
              height: 'min(calc(100svh - 160px), calc(100vw / 1.4222))',
              minHeight: 260,
              objectFit: 'cover',
              display: 'block',
            }}
          />
        </picture>
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

          {/* Right: colors + base + specs */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.15 }}
          >
            {/* Color variants */}
            <div style={{ marginBottom: 32 }}>
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
              <div style={{ marginBottom: 40 }}>
                <span className="label" style={{ display: 'block', marginBottom: 16 }}>Base</span>
                <div style={{ display: 'flex', gap: 0, borderTop: 'var(--rule)' }}>
                  {bases.map(({ key: base, label }, i) => {
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
                        {label}
                      </button>
                    )
                  })}
                </div>
              </div>
            )}

            {/* Specifications */}
            <span className="label" style={{ display: 'block', marginBottom: 4 }}>Specifications</span>
            <SpecRow label="Series" value={object.series} />
            <SpecRow label="Year" value={object.year} />
            <SpecRow label="Dimensions" value={object.dimensions} />
            <SpecRow label="Weight" value={object.weight} />
            <SpecRow label="Materials" value={object.materials} />
            <SpecRow label="Base Materials" value={object.baseMaterials} />
            <SpecRow label="Status" value={object.status} />
            <SpecRow label="Edition" value={object.edition} />
          </motion.div>
        </div>
      </section>

      {/* ── Detail shots (follow selected color + base) ── */}
      {object.details && (
        <section style={{
          borderTop: 'var(--rule)',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: 1,
          background: 'var(--border)',
        }}>
          {object.details.views.map((view, i) => {
            const color = object.colors.find(c => c.key === activeKey)
            const src = object.details.src(activeKey, activeBase, view.key)
            return (
              <div key={view.key} style={{ backgroundColor: 'var(--white)' }}>
                <motion.div
                  key={src}
                  initial={{ opacity: 0.6 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.35 }}
                >
                  <ResponsiveImage
                    src={src}
                    widths={[640, 1280, 1920]}
                    sizes="(max-width: 700px) 100vw, 50vw"
                    alt={`${object.name} detail, ${view.label.toLowerCase()} — ${color?.name}, ${activeBase}`}
                    style={{ width: '100%', aspectRatio: '1 / 1', objectFit: 'cover', display: 'block' }}
                    loading="lazy"
                  />
                </motion.div>
                <div style={{
                  padding: '10px 14px',
                  borderTop: 'var(--rule)',
                  display: 'flex',
                  flexWrap: 'wrap',
                  justifyContent: 'space-between',
                  gap: '4px 16px',
                }}>
                  <span className="label" style={{ whiteSpace: 'nowrap' }}>Detail — {view.label}</span>
                  <span className="label" style={{ opacity: 0.6, whiteSpace: 'nowrap' }}>
                    {color?.name} · {baseLabel?.replace('Brushed ', '')}
                  </span>
                </div>
              </div>
            )
          })}
        </section>
      )}

      {/* ── In situ ───────────────────────────────────── */}
      {object.inSitu && (
        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="object-insitu"
          style={{ borderTop: 'var(--rule)' }}
        >
          <div style={{
            padding: '14px var(--gutter)',
            display: 'flex',
            flexDirection: 'column',
            gap: 6,
          }}>
            <span className="label">In situ — {object.inSitu.caption}</span>
            <span className="label" style={{ opacity: 0.6 }}>{object.inSitu.credit}</span>
          </div>
          <ResponsiveImage
            src={object.inSitu.src}
            widths={[640, 1280, 1920, 2880]}
            sizes="(max-width: 900px) 100vw, 50vw"
            alt={object.inSitu.alt}
            style={{ width: '100%', aspectRatio: '4 / 3', objectFit: 'cover', display: 'block' }}
            loading="lazy"
          />
        </motion.section>
      )}

      {/* ── Dimensions table ───────────────────────────── */}
      {object.dimensionDetails && (
        <section style={{
          borderTop: 'var(--rule)',
          padding: 'clamp(40px, 5vw, 70px) var(--gutter)',
        }}>
          <div style={{
            maxWidth: 'var(--max)',
            margin: '0 auto',
            display: 'grid',
            gridTemplateColumns: '1fr 2fr',
            gap: 'clamp(40px, 6vw, 100px)',
          }}>
            <div>
              <span className="label" style={{ display: 'block', marginBottom: 8 }}>
                Dimensions
              </span>
              <p style={{ fontSize: 12, color: 'var(--grey)', lineHeight: 1.6, maxWidth: 220 }}>
                {object.name} — full dimensional breakdown
              </p>
            </div>
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-60px' }}
              transition={{ duration: 0.4 }}
              style={{ maxWidth: 560 }}
            >
              <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr auto',
                paddingBottom: 8,
                borderBottom: 'var(--rule)',
              }}>
                <span className="label">Element</span>
                <span className="label">Measurement</span>
              </div>
              {object.dimensionDetails.map((row, i) => (
                <motion.div
                  key={row.label}
                  initial={{ opacity: 0 }}
                  whileInView={{ opacity: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.3, delay: i * 0.04 }}
                  style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr auto',
                    alignItems: 'baseline',
                    padding: '14px 0',
                    borderBottom: 'var(--rule)',
                    gap: 24,
                  }}
                >
                  <span style={{ fontSize: 14, fontWeight: 500 }}>{row.label}</span>
                  <span style={{
                    fontSize: 13,
                    letterSpacing: '0.03em',
                    color: 'var(--grey)',
                    fontVariantNumeric: 'tabular-nums',
                  }}>
                    {row.value}
                  </span>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>
      )}

      {/* ── Variant image strip ────────────────────────── */}
      <section className="variant-strip" style={{ borderTop: 'var(--rule)' }}>
        {object.colors.map((color, i) => (
          <motion.div
            key={color.key}
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: i * 0.07 }}
            style={{
              cursor: 'pointer',
              backgroundColor: 'var(--white)',
              opacity: activeKey === color.key ? 1 : 0.6,
              transition: 'opacity 0.3s',
            }}
            onClick={() => setActiveColor(color.key)}
          >
            <img
              src={object.images[imgKey(color.key, activeBase)] ?? object.images[color.key]}
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

    </motion.div>
  )
}
