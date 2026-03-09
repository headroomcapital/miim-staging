import { Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Header from './components/Header'
import Footer from './components/Footer'
import ScrollToTop from './components/ScrollToTop'
import Home from './pages/Home'
import Studio from './pages/Studio'
import Archive from './pages/Archive'
import ObjectPage from './pages/ObjectPage'
import Inquiry from './pages/Inquiry'

export default function App() {
  const location = useLocation()

  return (
    <>
      <ScrollToTop />
      <Header />
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={<Home />} />
          <Route path="/studio" element={<Studio />} />
          <Route path="/archive" element={<Archive />} />
          <Route path="/archive/:id" element={<ObjectPage />} />
          <Route path="/inquiry" element={<Inquiry />} />
        </Routes>
      </AnimatePresence>
      <Footer />
    </>
  )
}
