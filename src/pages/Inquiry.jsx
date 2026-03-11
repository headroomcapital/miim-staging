import { useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useState } from 'react'

const fade = { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } }

const inputStyle = {
  width: '100%',
  padding: '12px 0',
  fontSize: 14,
  fontFamily: 'var(--font)',
  fontWeight: 700,
  border: 'none',
  borderBottom: 'var(--rule)',
  background: 'transparent',
  outline: 'none',
  transition: 'border-color 0.2s',
  color: 'var(--black)',
  letterSpacing: '0.02em',
}

export default function Inquiry() {
  const location = useLocation()
  const objectName = location.state?.object || null
  const [submitted, setSubmitted] = useState(false)

  return (
    <motion.div {...fade} transition={{ duration: 0.3 }} className="page">
      <section style={{
        maxWidth: 'var(--max)',
        margin: '0 auto',
        padding: 'clamp(50px, 7vw, 90px) var(--gutter)',
        borderBottom: 'var(--rule)',
      }}>
        <div className="col-2" style={{ alignItems: 'start' }}>

          {/* Left */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <span className="label" style={{ display: 'block', marginBottom: 20 }}>Inquiry</span>
            <h1 style={{
              fontSize: 'clamp(24px, 3.5vw, 44px)',
              fontWeight: 700,
              lineHeight: 1.15,
              maxWidth: 420,
              marginBottom: 24,
            }}>
              {objectName
                ? `Inquiry: ${objectName}`
                : 'Studio Access'}
            </h1>
            <p style={{ fontSize: 14, lineHeight: 1.7, color: 'var(--grey)', maxWidth: 360, marginBottom: 48 }}>
              For information about objects, commissions, or collaborations, please contact the studio.{' '}
              All inquiries are reviewed and answered directly.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <div>
                <span className="label" style={{ display: 'block', marginBottom: 6 }}>Email</span>
                <a href="mailto:info@miim.nu" style={{ fontSize: 15, fontWeight: 700, letterSpacing: '0.02em' }}>
                  info@miim.nu
                </a>
              </div>
              <div>
                <span className="label" style={{ display: 'block', marginBottom: 6 }}>Studio</span>
                <span style={{ fontSize: 15, fontWeight: 700, letterSpacing: '0.02em' }}>
                  Amsterdam, Netherlands
                </span>
              </div>
            </div>
          </motion.div>

          {/* Right: form */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.12 }}
            style={{ paddingTop: 52 }}
          >
            {submitted ? (
              <div style={{ paddingTop: 20 }}>
                <p style={{ fontSize: 16, fontWeight: 700, marginBottom: 8 }}>Received.</p>
                <p style={{ fontSize: 13, color: 'var(--grey)' }}>The studio will respond shortly.</p>
              </div>
            ) : (
              <form
                onSubmit={e => { e.preventDefault(); setSubmitted(true) }}
                style={{ display: 'flex', flexDirection: 'column', gap: 28, maxWidth: 480 }}
              >
                <input
                  type="text"
                  name="name"
                  placeholder="Name"
                  required
                  style={inputStyle}
                  onFocus={e => e.target.style.borderBottomColor = 'var(--black)'}
                  onBlur={e => e.target.style.borderBottomColor = 'var(--border)'}
                />
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  required
                  style={inputStyle}
                  onFocus={e => e.target.style.borderBottomColor = 'var(--black)'}
                  onBlur={e => e.target.style.borderBottomColor = 'var(--border)'}
                />
                {objectName ? (
                  <input
                    type="text"
                    name="subject"
                    defaultValue={`Inquiry: ${objectName}`}
                    readOnly
                    style={{ ...inputStyle, color: 'var(--grey)' }}
                  />
                ) : (
                  <input
                    type="text"
                    name="subject"
                    placeholder="Subject — object number, commission, collaboration"
                    style={inputStyle}
                    onFocus={e => e.target.style.borderBottomColor = 'var(--black)'}
                    onBlur={e => e.target.style.borderBottomColor = 'var(--border)'}
                  />
                )}
                <textarea
                  name="message"
                  placeholder="Message"
                  rows={5}
                  style={{ ...inputStyle, resize: 'vertical' }}
                  onFocus={e => e.target.style.borderBottomColor = 'var(--black)'}
                  onBlur={e => e.target.style.borderBottomColor = 'var(--border)'}
                />
                <button
                  type="submit"
                  style={{
                    alignSelf: 'flex-start',
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
                  Send Inquiry
                </button>
              </form>
            )}
          </motion.div>
        </div>
      </section>
    </motion.div>
  )
}
