import { useEffect, useRef, useState } from 'react'
import styles from './PredictionResult.module.css'
import YieldChart from './YieldChart'

function animateNumber(from, to, duration, onUpdate) {
  const start = performance.now()
  function step(now) {
    const progress = Math.min((now - start) / duration, 1)
    const eased = progress < 0.5
      ? 2 * progress * progress
      : 1 - Math.pow(-2 * progress + 2, 2) / 2
    onUpdate(from + (to - from) * eased)
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}

function formatNumber(num) {
  return num.toFixed(2)
}

function PredictionNumber({ value }) {
  const [displayValue, setDisplayValue] = useState(0)
  const prevValueRef = useRef(0)
  const animatingRef = useRef(false)

  useEffect(() => {
    if (animatingRef.current) return
    animatingRef.current = true
    animateNumber(prevValueRef.current, value, 800, setDisplayValue)
    prevValueRef.current = value
    setTimeout(() => { animatingRef.current = false }, 800)
  }, [value])

  return (
    <span className={styles.number} aria-live="polite">
      {formatNumber(displayValue)}
    </span>
  )
}

export default function PredictionResult({ prediction, formData, onNewPrediction }) {
  if (!prediction) return null

  const yieldValue = prediction.predicted_yield
  const unit = prediction.unit || 'tons/hectare'
  const crop = prediction.crop || formData.crop

  const inputSummary = [
    formData.crop,
    formData.soil_type,
    `${formData.temperature}°C`,
    `${formData.humidity}%`,
    `${formData.rainfall}mm`,
  ].filter(Boolean).join(' · ')

  return (
    <section className={styles.section} aria-labelledby="result-heading">
      <div className={styles.content}>
        <h2 id="result-heading" className={styles.title}>PREDICTED YIELD</h2>

        <div className={styles.yieldDisplay}>
          <PredictionNumber value={yieldValue} />
          <span className={styles.unit}>{unit.toUpperCase()}</span>
        </div>

        <div className={styles.divider} aria-hidden="true" />

        <YieldChart
          value={yieldValue}
          min={0}
          max={15}
          unit="t/ha"
        />

        <div className={styles.divider} aria-hidden="true" />

        <p className={styles.summary}>{inputSummary}</p>

        <button
          className={styles.newPredictionBtn}
          onClick={onNewPrediction}
          type="button"
        >
          New prediction
        </button>
      </div>
    </section>
  )
}