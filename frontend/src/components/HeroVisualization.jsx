import styles from './HeroVisualization.module.css'

export default function HeroVisualization() {
  return (
    <svg
      className={styles.svg}
      viewBox="0 0 400 300"
      aria-hidden="true"
      role="img"
    >
      <defs>
        <linearGradient id={styles.gridGradient} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="var(--color-border)" stop-opacity="0.3" />
          <stop offset="100%" stop-color="var(--color-border)" stop-opacity="0.1" />
        </linearGradient>
        <linearGradient id={styles.lineGradient} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="var(--color-border-strong)" stop-opacity="0.4" />
          <stop offset="100%" stop-color="var(--color-accent)" stop-opacity="0.6" />
        </linearGradient>
      </defs>

      <rect className={styles.gridBase} x="0" y="240" width="400" height="60" fill="url(#gridGradient)" />

      <g className={styles.gridLines}>
        <line x1="0" y1="240" x2="400" y2="240" stroke="var(--color-border)" stroke-width="0.5" />
        <line x1="0" y1="200" x2="400" y2="200" stroke="var(--color-border)" stroke-width="0.5" opacity="0.4" />
        <line x1="0" y1="160" x2="400" y2="160" stroke="var(--color-border)" stroke-width="0.5" opacity="0.2" />
        <line x1="0" y1="120" x2="400" y2="120" stroke="var(--color-border)" stroke-width="0.5" opacity="0.15" />
        <line x1="0" y1="80" x2="400" y2="80" stroke="var(--color-border)" stroke-width="0.5" opacity="0.1" />
      </g>

      <g className={styles.inputNodes}>
        <circle className={styles.node} cx="60" cy="160" r="4" fill="var(--color-text-secondary)" />
        <circle className={styles.node} cx="150" cy="130" r="4" fill="var(--color-text-secondary)" />
        <circle className={styles.node} cx="250" cy="145" r="4" fill="var(--color-text-secondary)" />
        <circle className={styles.node} cx="340" cy="120" r="4" fill="var(--color-text-secondary)" />
      </g>

      <g className={styles.connectingLines}>
        <line className={styles.line} x1="60" y1="160" x2="200" y2="80" stroke="url(#lineGradient)" stroke-width="1" stroke-dasharray="6 4" />
        <line className={styles.line} x1="150" y1="130" x2="200" y2="80" stroke="url(#lineGradient)" stroke-width="1" stroke-dasharray="6 4" />
        <line className={styles.line} x1="250" y1="145" x2="200" y2="80" stroke="url(#lineGradient)" stroke-width="1" stroke-dasharray="6 4" />
        <line className={styles.line} x1="340" y1="120" x2="200" y2="80" stroke="url(#lineGradient)" stroke-width="1" stroke-dasharray="6 4" />
      </g>

      <circle
        className={`${styles.centralNode} ${styles.pulse}`}
        cx="200"
        cy="80"
        r="6"
        fill="var(--color-accent)"
      />

      <line
        className={`${styles.outputLine} ${styles.dash}`}
        x1="200"
        y1="80"
        x2="200"
        y2="240"
        stroke="var(--color-accent)"
        stroke-width="1"
        stroke-dasharray="4 4"
        stroke-opacity="0.5"
      />

      <circle
        className={`${styles.outputNode} ${styles.pulse}`}
        cx="200"
        cy="240"
        r="4"
        fill="var(--color-accent)"
      />

      <g className={styles.labels} font-family="var(--font-body)" font-size="9" fill="var(--color-text-secondary)">
        <text x="50" y="178" text-anchor="middle">RAINFALL</text>
        <text x="135" y="148" text-anchor="middle">TEMP</text>
        <text x="254" y="163" text-anchor="middle">HUMIDITY</text>
        <text x="325" y="138" text-anchor="middle">SOIL</text>
      </g>

      <text
        className={styles.aiLabel}
        x="200"
        y="72"
        text-anchor="middle"
        font-family="var(--font-mono)"
        font-size="9"
        fill="var(--color-accent)"
      >
        AI
      </text>

      <text
        className={styles.yieldLabel}
        x="200"
        y="258"
        text-anchor="middle"
        font-family="var(--font-mono)"
        font-size="9"
        fill="var(--color-accent)"
      >
        YIELD
      </text>
    </svg>
  )
}