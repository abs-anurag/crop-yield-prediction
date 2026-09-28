import styles from './Hero.module.css'
import HeroVisualization from './HeroVisualization'

export default function Hero({ onCTAClick }) {
  return (
    <section className={styles.hero} aria-labelledby="hero-heading">
      <div className={styles.grid}>
        <div className={styles.textColumn}>
          <span className={styles.eyebrow}>01 / CROP YIELD AI</span>
          <h2 id="hero-heading" className={styles.heading}>
            <span className={styles.headingLine}>Know your field.</span>
            <span className={styles.headingLine}>Estimate your yield.</span>
          </h2>
          <p className={styles.copy}>
            Estimate crop yield from agricultural and environmental conditions using data-driven machine learning.
          </p>
          <button
            className={styles.cta}
            onClick={onCTAClick}
            aria-label="Scroll to prediction form"
          >
            Predict yield
            <span className={styles.ctaArrow} aria-hidden="true">→</span>
          </button>
        </div>
        <div className={styles.visualColumn} aria-hidden="true">
          <HeroVisualization />
        </div>
      </div>
    </section>
  )
}