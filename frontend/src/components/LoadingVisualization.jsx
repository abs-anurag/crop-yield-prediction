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
      <h3 className={styles.title}>ANALYZING AGRICULTURAL CONDITIONS</h3>
      <div className={styles.bars}>
        {loadingFields.map((field, index) => (
          <div key={field.label} className={styles.barWrapper} style={{ '--delay': `${field.delay}s` }}>
            <div className={styles.barTrack}>
              <div className={styles.barFill}>
                <span className={styles.barEnd} aria-hidden="true">●</span>
              </div>
            </div>
            <span className={styles.barLabel}>{field.label}</span>
          </div>
        ))}
      </div>
      <p className={styles.processing}>PROCESSING</p>
    </div>
  )
}