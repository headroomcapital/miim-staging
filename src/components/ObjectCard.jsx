import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function ObjectCard({ object, index = 0, border = true }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-60px' }}
      transition={{ duration: 0.4, delay: index * 0.07 }}
      style={{ borderLeft: border ? 'var(--rule)' : 'none' }}
    >
      <Link
        to={`/archive/${object.id}`}
        style={{ display: 'block' }}
        onMouseEnter={e => e.currentTarget.querySelector('img').style.transform = 'scale(1.03)'}
        onMouseLeave={e => e.currentTarget.querySelector('img').style.transform = 'scale(1)'}
      >
        {/* Image */}
        <div style={{ overflow: 'hidden', aspectRatio: '4/3', backgroundColor: '#E8E8E4' }}>
          <img
            src={object.thumbnail}
            alt={object.name}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              display: 'block',
              transition: 'transform 0.6s ease',
            }}
            loading="lazy"
          />
        </div>

        {/* Archive record */}
        <div style={{ borderTop: 'var(--rule)', padding: '12px 14px 16px' }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'baseline',
            marginBottom: 6,
          }}>
            <span className="label mono">{object.number}</span>
            <span className="label">{object.series} · {object.year}</span>
          </div>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'baseline',
          }}>
            <span style={{ fontSize: 14, letterSpacing: '0.02em' }}>{object.name}</span>
            <span className="label mono">{object.dimensions}</span>
          </div>
        </div>
      </Link>
    </motion.div>
  )
}
