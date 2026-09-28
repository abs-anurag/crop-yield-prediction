import styles from './Hero.module.css'
import HeroVisualization from './HeroVisualization'

export default function Hero({ onCTAClick }) {
  return (
    <section className={styles.hero} aria-labelledby="hero-heading">
      <div className={styles.grid}>
        <div className={styles.textColumn}>
          <h2 id="hero-heading" className={styles.heading}>
            <span className={styles.headingLine}>AI AGRICULTURAL</span>
            <span className={styles.headingLine}>INTELLIGENCE</span>
          </h2>
          <p className={styles.copy}>
            Predict crop yield from field conditions.
          </p>
          <p className={styles.copySecondary}>
            Understand how rainfall, temperature, soil, and crop type influence estimated yield.
          </p>
          <button
            className={styles.cta}
            onClick={onCTAClick}
            aria-label="Scroll to prediction form"
          >
            Predict yield
          </button>
        </div>
        <div className={styles.visualColumn} aria-hidden="true">
          <HeroVisualization />
        </div>
      </div>
    </section>
  )
}