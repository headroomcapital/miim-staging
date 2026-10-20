import { useEffect } from 'react'

const RESPONSIVE_IMAGES = {
  '/images/miim-i-cobalt-brass-library-v2.jpg': {
    widths: [640, 1280, 1920, 2880],
    base: '/images/responsive/miim-i-cobalt-brass-library-v2',
  },
  '/images/miim-i-plum-brass-insitu-paris-v2.jpg': {
    widths: [640, 1280, 1920, 2880],
    base: '/images/responsive/miim-i-plum-brass-insitu-paris-v2',
  },
  '/images/miim-i-series-group.jpg': {
    widths: [640, 1280, 1920],
    base: '/images/responsive/miim-i-series-group',
  },
}

// Map routes to images that should be preloaded
const ROUTE_IMAGES = {
  '/inquiry': ['/images/miim-i-series-group.jpg'],
  '/studio': ['/images/miim-i-cobalt-brass-library-v2.jpg'],
  '/archive': ['/images/miim-i-plum-brass-insitu-paris-v2.jpg'],
}

function getOptimalWidth() {
  const dpr = window.devicePixelRatio || 1
  const vw = window.innerWidth
  const effective = vw * dpr

  if (effective <= 768) return 640
  if (effective <= 1440) return 1280
  return 1920
}

function supportsWebP() {
  const canvas = document.createElement('canvas')
  canvas.width = 1
  canvas.height = 1
  return canvas.toDataURL('image/webp').startsWith('data:image/webp')
}

const webpSupported = typeof document !== 'undefined' ? supportsWebP() : false

function getPreloadUrl(originalSrc) {
  const config = RESPONSIVE_IMAGES[originalSrc]
  if (!config) return originalSrc

  const targetWidth = getOptimalWidth()
  const bestWidth = config.widths.reduce((prev, w) =>
    w <= targetWidth ? w : prev, config.widths[0]
  )
  // Pick the largest width that doesn't exceed target, or the smallest available
  const width = bestWidth || config.widths[0]
  const ext = webpSupported ? 'webp' : 'jpg'

  return `${config.base}-${width}.${ext}`
}

export default function usePreloadImages(routeImages) {
  useEffect(() => {
    const srcs = routeImages || []
    const links = []

    srcs.forEach(src => {
      const url = getPreloadUrl(src)
      const type = url.endsWith('.webp') ? 'image/webp' : 'image/jpeg'

      // Avoid duplicate preloads
      if (document.querySelector(`link[href="${url}"]`)) return

      const link = document.createElement('link')
      link.rel = 'preload'
      link.as = 'image'
      link.href = url
      link.type = type
      document.head.appendChild(link)
      links.push(link)
    })

    return () => links.forEach(l => l.remove())
  }, [routeImages])
}

// Preload images for adjacent routes (called from nav/layout)
export function usePreloadAdjacentRoutes(currentPath) {
  useEffect(() => {
    const timer = setTimeout(() => {
      // Preload images for routes the user is likely to visit next
      Object.entries(ROUTE_IMAGES).forEach(([route, images]) => {
        if (route === currentPath) return
        images.forEach(src => {
          const url = getPreloadUrl(src)
          if (document.querySelector(`link[href="${url}"]`)) return

          const link = document.createElement('link')
          link.rel = 'prefetch'
          link.as = 'image'
          link.href = url
          document.head.appendChild(link)
        })
      })
    }, 2000) // Wait 2s after page load before prefetching other routes

    return () => clearTimeout(timer)
  }, [currentPath])
}

export { ROUTE_IMAGES }
