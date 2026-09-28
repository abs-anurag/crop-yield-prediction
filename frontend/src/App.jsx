import { useState, useEffect, useCallback, useRef } from 'react'
import { fetchMetadata, predictYield } from './services/api'
import Header from './components/Header'
import Hero from './components/Hero'
import PredictionForm from './components/PredictionForm'
import LoadingVisualization from './components/LoadingVisualization'
import PredictionResult from './components/PredictionResult'
import HowItWorks from './components/HowItWorks'
import ErrorMessage from './components/ErrorMessage'
import Footer from './components/Footer'
import styles from './App.module.css'

const INITIAL_FORM_DATA = {
  crop: '',
  soil_type: '',
  rainfall: '',
  temperature: '',
  humidity: '',
  fertilizer: 0,
  area: '',
}

function App() {
  const [metadata, setMetadata] = useState(null)
  const [metadataError, setMetadataError] = useState(false)
  const [formData, setFormData] = useState(INITIAL_FORM_DATA)
  const [formErrors, setFormErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [prediction, setPrediction] = useState(null)
  const [apiError, setApiError] = useState(null)
  const formRef = useRef(null)

  useEffect(() => {
    let mounted = true
    let timeoutId

    async function loadMetadata() {
      try {
        const data = await fetchMetadata()
        if (mounted) {
          setMetadata(data)
          setMetadataError(false)
        }
      } catch {
        if (mounted) {
          timeoutId = setTimeout(() => {
            if (mounted) {
              setMetadataError(true)
            }
          }, 3000)
        }
      }
    }

    loadMetadata()

    return () => {
      mounted = false
      clearTimeout(timeoutId)
    }
  }, [])

  const handleChange = useCallback((field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    if (formErrors[field]) {
      setFormErrors(prev => ({ ...prev, [field]: null }))
    }
  }, [formErrors])

  const handleBlur = useCallback((field, value, error) => {
    setFormErrors(prev => ({ ...prev, [field]: error }))
  }, [])

  const handleSubmit = useCallback(async (validationErrors) => {
    if (validationErrors) {
      setFormErrors(validationErrors)
      const firstErrorField = Object.keys(validationErrors)[0]
      const element = document.getElementById(firstErrorField)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' })
        element.focus()
      }
      return
    }

    setLoading(true)
    setApiError(null)

    try {
      const result = await predictYield(formData)
      setPrediction(result)
      formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    } catch (err) {
      setApiError(err)
    } finally {
      setLoading(false)
    }
  }, [formData])

  const handleNewPrediction = useCallback(() => {
    setPrediction(null)
    setFormData(INITIAL_FORM_DATA)
    setFormErrors({})
    setApiError(null)
    const formSection = document.getElementById('prediction-form')
    if (formSection) {
      formSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, [])

  const handleRetry = useCallback(() => {
    setApiError(null)
    handleSubmit(formErrors)
  }, [handleSubmit, formErrors])

  return (
    <div className={styles.app}>
      <Header />
      <main className={styles.main}>
        <Hero onCTAClick={() => {
          const formSection = document.getElementById('prediction-form')
          if (formSection) {
            formSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        }} />

        <section id="prediction-form" className={styles.formSection} aria-labelledby="form-heading">
          {apiError ? (
            <ErrorMessage error={apiError} onRetry={handleRetry} />
          ) : prediction ? (
            <PredictionResult
              prediction={prediction}
              formData={formData}
              onNewPrediction={handleNewPrediction}
            />
          ) : loading ? (
            <LoadingVisualization />
          ) : (
            <PredictionForm
              ref={formRef}
              metadata={metadata}
              formData={formData}
              formErrors={formErrors}
              onChange={handleChange}
              onBlur={handleBlur}
              onSubmit={handleSubmit}
              loading={loading}
              metadataError={metadataError}
            />
          )}
        </section>

        <HowItWorks />
      </main>
      <Footer />
    </div>
  )
}

export default App