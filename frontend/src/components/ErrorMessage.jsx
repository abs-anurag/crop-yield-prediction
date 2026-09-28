import styles from './ErrorMessage.module.css'

const errorMessages = {
  MODEL_NOT_READY: 'The prediction model is not currently loaded. Please try again shortly.',
  422: 'Some inputs are outside the expected range. Check the highlighted fields.',
  default: 'Something went wrong. Please check your connection and try again.',
}

export default function ErrorMessage({ error, onRetry }) {
  const getMessage = (err) => {
    if (!err) return errorMessages.default
    if (err.error === 'MODEL_NOT_READY') return errorMessages.MODEL_NOT_READY
    if (err.status === 422 || err.detail) return errorMessages[422]
    return err.message || errorMessages.default
  }

  return (
    <section className={styles.section} aria-live="assertive" role="alert">
      <div className={styles.content}>
        <h2 className={styles.title}>PREDICTION UNAVAILABLE</h2>
        <p className={styles.description}>{getMessage(error)}</p>
        <button
          className={styles.retryBtn}
          onClick={onRetry}
          type="button"
        >
          Try again
        </button>
      </div>
    </section>
  )
}