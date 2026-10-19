const RESPONSIVE_IMAGES = {
  '/images/miim-i-cobalt-brass-studio.png': {
    widths: [640, 1280, 1920],
    base: '/images/responsive/miim-i-cobalt-brass-studio',
  },
  '/images/miim-i-cobalt-brass-canal.jpg': {
    widths: [640, 1280, 1920, 2880],
    base: '/images/responsive/miim-i-cobalt-brass-canal',
  },
  '/images/miim-i-series-group.jpg': {
    widths: [640, 1280, 1920],
    base: '/images/responsive/miim-i-series-group',
  },
}

// Images with generated variants in /images/responsive/ can opt in by passing `widths`
export default function ResponsiveImage({ src, alt, style, loading, widths: ownWidths, sizes = '100vw', ...rest }) {
  const config = RESPONSIVE_IMAGES[src] ?? (ownWidths && {
    widths: ownWidths,
    base: src.replace('/images/', '/images/responsive/').replace(/\.(jpg|png)$/, ''),
  })

  if (!config) {
    return <img src={src} alt={alt} style={style} loading={loading} {...rest} />
  }

  const { widths, base } = config
  const webpSrcSet = widths.map(w => `${base}-${w}.webp ${w}w`).join(', ')
  const jpgSrcSet = widths.map(w => `${base}-${w}.jpg ${w}w`).join(', ')

  return (
    <picture>
      <source type="image/webp" srcSet={webpSrcSet} sizes={sizes} />
      <source type="image/jpeg" srcSet={jpgSrcSet} sizes={sizes} />
      <img
        src={`${base}-${widths[widths.length - 1]}.jpg`}
        alt={alt}
        style={style}
        loading={loading}
        {...rest}
      />
    </picture>
  )
}
