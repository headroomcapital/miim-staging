import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer style={{
      borderTop: 'var(--rule)',
      padding: '28px var(--gutter)',
    }}>
      <div style={{
        maxWidth: 'var(--max)',
        margin: '0 auto',
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: 20,
        alignItems: 'center',
      }}>
        <span className="label">MIIM — Object Archive</span>
        <span className="label">Amsterdam, NL</span>
        <a href="mailto:info@miim.nu" className="label" style={{ color: 'var(--grey)', transition: 'color 0.2s' }}
          onMouseEnter={e => e.target.style.color = 'var(--black)'}
          onMouseLeave={e => e.target.style.color = 'var(--grey)'}
        >
          info@miim.nu
        </a>
        <span className="label" style={{ textAlign: 'right' }}>© 2026</span>
      </div>
    </footer>
  )
}
