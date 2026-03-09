import { Link, useLocation } from 'react-router-dom'
import { motion, useScroll } from 'framer-motion'
import { useState, useEffect } from 'react'

const nav = [
  { label: 'Archive', path: '/archive' },
  { label: 'Studio', path: '/studio' },
  { label: 'Inquiry', path: '/inquiry' },
]

const NavItem = ({ label, path, isActive }) => {
  const [hovered, setHovered] = useState(false)
  return (
    <div
      style={{ position: 'relative' }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <Link
        to={path}
        className="label"
        style={{
          color: (hovered || isActive) ? 'var(--black)' : 'var(--grey)',
          transition: 'color 0.15s',
        }}
      >
        {label}
      </Link>
      <motion.span
        animate={{ scaleX: hovered ? 1 : 0 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        style={{
          position: 'absolute',
          bottom: -3, left: 0, right: 0,
          height: 1,
          backgroundColor: 'var(--black)',
          display: 'block',
          originX: 0,
        }}
      />
    </div>
  )
}

export default function Header() {
  const { scrollY } = useScroll()
  const location = useLocation()
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => scrollY.on('change', y => setScrolled(y > 50)), [scrollY])

  return (
    <header style={{
      position: 'fixed',
      top: 0, left: 0, right: 0,
      zIndex: 100,
      height: 'var(--header-h)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 var(--gutter)',
      backgroundColor: scrolled ? 'rgba(247,247,242,0.97)' : 'transparent',
      borderBottom: scrolled ? 'var(--rule)' : '1px solid transparent',
      transition: 'background-color 0.25s, border-color 0.25s',
    }}>
      <Link to="/" style={{ display: 'flex', alignItems: 'baseline', gap: 10 }}>
        <span style={{
          fontFamily: 'var(--font-display)',
          fontSize: 15,
          fontWeight: 500,
          letterSpacing: '0.02em',
          color: 'var(--yellow)',
        }}>
          MIIM
        </span>
        <span className="label hide-mobile" style={{ color: 'var(--grey)' }}>
          Objects in series
        </span>
      </Link>

      <nav style={{ display: 'flex', gap: 28 }}>
        {nav.map(({ label, path }) => (
          <NavItem
            key={path}
            label={label}
            path={path}
            isActive={location.pathname.startsWith(path)}
          />
        ))}
      </nav>
    </header>
  )
}
