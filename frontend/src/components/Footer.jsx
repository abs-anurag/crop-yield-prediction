import styles from './Footer.module.css'

export default function Footer() {
  return (
    <footer className={styles.footer} role="contentinfo">
      <div className={styles.inner}>
        <p className={styles.text}>
          CropYield AI — AI-Based Crop Yield Prediction
          <span className={styles.separator} aria-hidden="true">—</span>
          Academic demonstration project
        </p>
      </div>
    </footer>
  )
}