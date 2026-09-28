import styles from './HowItWorks.module.css'

const steps = [
  {
    number: '01',
    title: 'INPUT',
    description: 'Agricultural and environmental conditions: crop, soil, rainfall, temperature, humidity, fertilizer, and area.',
  },
  {
    number: '02',
    title: 'ANALYSIS',
    description: 'A Random Forest regression model trained on historical agricultural data processes your inputs.',
  },
  {
    number: '03',
    title: 'ESTIMATE',
    description: 'The model returns an estimated crop yield in tonnes per hectare.',
  },
]

export default function HowItWorks() {
  return (
    <section className={styles.section} id="how-it-works" aria-labelledby="how-it-works-heading">
      <h2 id="how-it-works-heading" className={styles.title}>HOW IT WORKS</h2>
      <div className={styles.grid}>
        {steps.map((step, index) => (
          <article key={step.number} className={styles.card}>
            <span className={styles.number}>{step.number}</span>
            <h3 className={styles.stepTitle}>{step.title}</h3>
            <p className={styles.stepDescription}>{step.description}</p>
          </article>
        ))}
      </div>
    </section>
  )
}