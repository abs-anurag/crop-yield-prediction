import styles from './YieldChart.module.css'

export default function YieldChart({ value, min = 0, max = 15, unit = 't/ha' }) {
  const clampedValue = Math.max(min, Math.min(max, value))
  const percentage = ((clampedValue - min) / (max - min)) * 100

  return (
    <div className={styles.container} role="img" aria-label={`Yield gauge showing ${value.toFixed(2)} ${unit}`}>
      <svg className={styles.svg} viewBox="0 0 400 80" aria-hidden="true">
        <defs>
          <linearGradient id={styles.trackGradient} x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="var(--color-border)" />
            <stop offset="100%" stop-color="var(--color-border)" />
          </linearGradient>
        </defs>

        <rect
          className={styles.track}
          x="0"
          y="30"
          width="400"
          height="4"
          rx="0"
          fill="url(#trackGradient)"
        />

        <line
          className={styles.markerLine}
          x1={percentage * 4}
          y1="20"
          x2={percentage * 4}
          y2="50"
          stroke="var(--color-accent)"
          stroke-width="2"
          stroke-linecap="round"
        />

        <circle
          className={styles.marker}
          cx={percentage * 4}
          cy="35"
          r="6"
          fill="var(--color-accent)"
        />
      </svg>

      <div className={styles.labels}>
        <span className={styles.minLabel}>{min} {unit}</span>
        <span className={styles.valueLabel}>{value.toFixed(2)} {unit}</span>
        <span className={styles.maxLabel}>{max} {unit}</span>
      </div>

      <p className={styles.markerLabel}>your prediction</p>
    </div>
  )
}