import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'

const fade = { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } }

const Section = ({ label, heading, body, index = 0 }) => (
  <motion.div
    initial={{ opacity: 0, y: 16 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: '-60px' }}
    transition={{ duration: 0.4, delay: index * 0.08 }}
    style={{
      display: 'grid',
      gridTemplateColumns: '1fr 2fr',
      gap: 'clamp(40px, 6vw, 100px)',
      padding: 'clamp(40px, 5vw, 60px) 0',
      borderTop: 'var(--rule)',
    }}
  >
    <div>
      <span className="label">{label}</span>
    </div>
    <div>
      {heading && (
        <p style={{
          fontSize: 'clamp(18px, 2vw, 22px)',
          lineHeight: 1.4,
          marginBottom: body ? 20 : 0,
        }}>
          {heading}
        </p>
      )}
      {body && (
        <p style={{
          fontSize: 'clamp(14px, 1.4vw, 16px)',
          lineHeight: 1.7,
          color: 'var(--grey)',
        }}>
          {body}
        </p>
      )}
    </div>
  </motion.div>
)

export default function Studio() {
  return (
    <motion.div {...fade} transition={{ duration: 0.3 }} className="page">

      {/* Opening */}
      <section style={{
        minHeight: '60vh',
        display: 'flex',
        alignItems: 'flex-end',
        padding: 'clamp(60px, 8vw, 100px) var(--gutter)',
        borderBottom: 'var(--rule)',
      }}>
        <div style={{ maxWidth: 'var(--max)', margin: '0 auto', width: '100%' }}>
          <motion.span
            className="label"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4 }}
            style={{ display: 'block', marginBottom: 28 }}
          >
            Studio
          </motion.span>
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            style={{
              fontSize: 'clamp(28px, 4.5vw, 56px)',
              fontWeight: 700,
              lineHeight: 1.15,
              maxWidth: 820,
            }}
          >
            MIIM is a design studio based in Amsterdam exploring furniture through proportion, material, and spatial balance. Objects are developed as part of systems rather than isolated pieces.
          </motion.h1>
        </div>
      </section>

      {/* Full-width image */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.7 }}
      >
        <img
          src="https://miim.nu/wp-content/uploads/2025/08/miim1-1.jpg"
          alt="MIIM studio"
          style={{ width: '100%', height: 'auto', display: 'block' }}
        />
      </motion.section>

      {/* Four conceptual sections */}
      <section style={{
        maxWidth: 'var(--max)',
        margin: '0 auto',
        padding: 'clamp(40px, 6vw, 80px) var(--gutter)',
      }}>
        <Section
          index={0}
          label="Spatial Harmony"
          heading="Furniture should not transform a space — it should complete it."
          body="MIIM objects are designed to exist in balance with their surroundings. Through proportion, structure, and restraint, they create a sense of spatial harmony."
        />
        <Section
          index={1}
          label="Irrational Minimalism"
          heading="The studio's approach combines calculation with intuition."
          body="Dimensions are carefully considered, yet the final object is shaped by instinct. This balance produces forms that feel simple without becoming rigid."
        />
        <Section
          index={2}
          label="Built with Respect"
          heading="Every MIIM object is created with respect for material, craftsmanship, and its future owner."
          body="Objects are produced using responsibly sourced materials and built to last for generations."
        />
        <Section
          index={3}
          label="Materials with Integrity"
          heading="Materials are chosen for their structural clarity and durability."
          body="Solid brass maintains precise geometry over time. Lacquered surfaces create a stable spatial plane. Used in their purest form, these materials allow the structure of the object to remain visible."
        />
      </section>

      {/* Second image */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.7 }}
      >
        <img
          src="https://miim.nu/wp-content/uploads/2023/10/e8ef286b296160a025cc5457765769fa4b416311-2000x1406.jpg"
          alt="MIIM object detail"
          style={{ width: '100%', height: 'auto', display: 'block' }}
          loading="lazy"
        />
      </motion.section>

      {/* CTA */}
      <Link to="/archive" style={{ display: 'block' }}>
        <div style={{
          borderTop: 'var(--rule)',
          padding: 'clamp(30px, 4vw, 50px) var(--gutter)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          transition: 'background-color 0.2s',
        }}
          onMouseEnter={e => e.currentTarget.style.backgroundColor = '#EEEEE8'}
          onMouseLeave={e => e.currentTarget.style.backgroundColor = 'transparent'}
        >
          <span className="label">Object Archive</span>
          <span className="label" style={{ color: 'var(--black)' }}>View Archive →</span>
        </div>
      </Link>

    </motion.div>
  )
}
