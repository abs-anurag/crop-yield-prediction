import styles from './LoadingVisualization.module.css'

const loadingFields = [
  { label: 'Rainfall', delay: 0 },
  { label: 'Temperature', delay: 0.15 },
  { label: 'Humidity', delay: 0.3 },
  { label: 'Soil type', delay: 0.45 },
  { label: 'Crop', delay: 0.6 },
]

export default function LoadingVisualization() {
  return (
    <div className={styles.container} role="status" aria-live="polite" aria-busy="true">
      <header className={styles.header}>
        <span className={styles.stepNumber}>02</span>
        <h3 className={styles.title}>ANALYZE</h3>
      </header>
      <p className={styles.subtitle}>Processing agricultural conditions</p>
      <div className={styles.bars}>
        {loadingFields.map((field, index) => (
          <div key={field.label} className={styles.barWrapper} style={{ '--delay': `${field.delay}s` }}>
            <span className={styles.barLabel}>{field.label}</span>
            <div className={styles.barTrack}>
              <div className={styles.barFill}>
                <span className={styles.barEnd} aria-hidden="true">●</span>
              </div>
            </div>
          </div>
        ))}
      </div>
      <p className={styles.processing}>PROCESSING</p>
    </div>
  )
}