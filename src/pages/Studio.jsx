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
            MIIM is a studio exploring objects through series. Rather than designing isolated pieces, we work with systems — defining what repeats and what changes across a family of objects.
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
          label="Objects within a system"
          heading="Each object is part of a series, not a standalone piece."
          body="We start by defining the system — what stays fixed, and what can vary. The object follows from that logic. This produces work that is related across iterations without being repetitive."
        />
        <Section
          index={1}
          label="Beginning with structure"
          heading="Form comes after the rule, not before it."
          body="Before anything is drawn, the structural logic is established. What holds what. What scales and what doesn't. The I-Series began with a single proposition: a horizontal surface supported by two vertical cylinders. From that, three objects follow."
        />
        <Section
          index={2}
          label="Materials that hold the form"
          heading="Materials are chosen for how they behave, not what they suggest."
          body="Brass keeps its geometry over time. Lacquered MDF holds a precise surface. These are the right materials for the I-Series because they perform consistently. Any association with luxury or craft is secondary."
        />
        <Section
          index={3}
          label="Numbered objects"
          heading="Each object receives a fixed number that stays with it."
          body="The number is not a edition marker. It records when an object entered the archive — and that record doesn't change. Object 001 is always 001, regardless of where it is or who has it."
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
