import styles from './HowItWorks.module.css'

const steps = [
  {
    number: '01',
    title: 'INPUT',
    description: 'Agricultural and environmental conditions — crop, soil, rainfall, temperature, humidity, fertilizer, and area — are provided.',
  },
  {
    number: '02',
    title: 'ANALYZE',
    description: 'A trained Random Forest regression model processes the inputs using patterns learned from historical agricultural data.',
  },
  {
    number: '03',
    title: 'ESTIMATE',
    description: 'The system returns an estimated crop yield in tonnes per hectare.',
  },
]

export default function HowItWorks() {
  return (
    <section className={styles.section} id="how-it-works" aria-labelledby="how-it-works-heading">
      <header className={styles.header}>
        <h2 id="how-it-works-heading" className={styles.title}>HOW IT WORKS</h2>
      </header>
      <div className={styles.grid}>
        {steps.map((step, index) => (
          <article key={step.number} className={styles.card}>
            <div className={styles.cardHeader}>
              <span className={styles.number}>{step.number}</span>
              <h3 className={styles.stepTitle}>{step.title}</h3>
            </div>
            <p className={styles.stepDescription}>{step.description}</p>
          </article>
        ))}
      </div>
    </section>
  )
}