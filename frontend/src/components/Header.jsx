import styles from './Header.module.css'

export default function Header() {
  return (
    <header className={styles.header} role="banner">
      <div className={styles.inner}>
        <div className={styles.brand}>
          <h1 className={styles.logo}>CropYield AI</h1>
          <span className={styles.tagline}>AGRICULTURAL INTELLIGENCE</span>
        </div>
        <nav className={styles.nav} aria-label="Main navigation">
          <a href="#prediction-form" className={styles.navLink}>Predict</a>
          <a href="#how-it-works" className={styles.navLink}>How it works</a>
        </nav>
      </div>
    </header>
  )
}