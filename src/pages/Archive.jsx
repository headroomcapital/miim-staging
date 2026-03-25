import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import ObjectCard from '../components/ObjectCard'
import objects from '../data/objects'

const fade = { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } }

export default function Archive() {
  return (
    <motion.div {...fade} transition={{ duration: 0.3 }} className="page">

      {/* Header */}
      <section style={{
        padding: 'clamp(50px, 7vw, 90px) var(--gutter) clamp(30px, 4vw, 50px)',
        borderBottom: 'var(--rule)',
        maxWidth: 'var(--max)',
        margin: '0 auto',
      }}>
        <motion.span
          className="label"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4 }}
          style={{ display: 'block', marginBottom: 20 }}
        >
          Archive / I-Series / {objects.length} Objects
        </motion.span>
        <motion.h1
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          style={{
            fontSize: 'clamp(28px, 4vw, 48px)',
            fontWeight: 700,
            lineHeight: 1.1,
            maxWidth: 600,
          }}
        >
          The Object Archive
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          style={{
            fontSize: 14,
            color: 'var(--grey)',
            marginTop: 16,
            maxWidth: 440,
            lineHeight: 1.6,
          }}
        >
          MIIM objects are documented as part of a growing archive.{' '}
          Each object receives a fixed designation that remains with it across time, spaces, and owners. The archive records the progression of a series — how a single structural idea evolves through variation.{' '}
          New objects are added gradually as the series develops.
        </motion.p>
      </section>

      {/* Object index */}
      <section style={{ borderBottom: 'var(--rule)' }}>
        <div style={{ maxWidth: 'var(--max)', margin: '0 auto' }}>
          <div className="object-grid">
            {objects.map((obj, i) => (
              <ObjectCard key={obj.id} object={obj} index={i} border={i > 0} />
            ))}
          </div>
        </div>
      </section>

      {/* Series note */}
      <section style={{
        padding: 'clamp(50px, 7vw, 80px) var(--gutter)',
        borderBottom: 'var(--rule)',
      }}>
        <div style={{
          maxWidth: 'var(--max)',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: '1fr 2fr',
          gap: 'clamp(40px, 6vw, 100px)',
        }}>
          <span className="label" style={{ paddingTop: 3 }}>I-Series Note</span>
          <p style={{ fontSize: 'clamp(14px, 1.4vw, 16px)', lineHeight: 1.7, color: 'var(--grey)', maxWidth: 520 }}>
            {objects[0].seriesNote}
          </p>
        </div>
      </section>

      {/* Full image */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.7 }}
      >
        <div style={{ overflow: 'hidden' }}>
          <img
            src="/images/miim-i-cobalt-brass-home.png"
            alt="MIIM-I in cobalt with brass base"
            style={{ width: '100%', display: 'block', marginTop: '-12%' }}
            loading="lazy"
          />
        </div>
      </motion.section>

      {/* CTA */}
      <Link to="/inquiry" style={{ display: 'block' }}>
        <div style={{
          backgroundColor: 'var(--yellow)',
          padding: 'clamp(30px, 4vw, 50px) var(--gutter)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <span className="label">Looking for a specific configuration or commission?</span>
          <span className="label" style={{ color: 'var(--black)' }}>Request Inquiry →</span>
        </div>
      </Link>

    </motion.div>
  )
}
