import { useEffect, useCallback } from 'react'
import InputField from './InputField'
import styles from './PredictionForm.module.css'

const FIELD_CONFIG = [
  { id: 'crop', label: 'Crop', type: 'select', required: true },
  { id: 'soil_type', label: 'Soil type', type: 'select', required: true },
  { id: 'rainfall', label: 'Rainfall', type: 'number', unit: 'mm', required: true, min: 0, max: 5000, step: 1 },
  { id: 'temperature', label: 'Temperature', type: 'number', unit: '°C', required: true, min: -10, max: 60, step: 0.1 },
  { id: 'humidity', label: 'Humidity', type: 'number', unit: '%', required: true, min: 0, max: 100, step: 1 },
  { id: 'fertilizer', label: 'Fertilizer', type: 'number', unit: 'kg/ha', required: false, min: 0, max: 2000, step: 1, defaultValue: 0 },
  { id: 'area', label: 'Area', type: 'number', unit: 'ha', required: true, min: 0.1, max: 10000, step: 0.1 },
]

export default function PredictionForm({
  metadata,
  formData,
  formErrors,
  onChange,
  onBlur,
  onSubmit,
  loading,
  disabled,
  metadataError,
}) {
  const validateField = useCallback((name, value, meta) => {
    const field = FIELD_CONFIG.find(f => f.id === name)
    if (!field) return null

    if (field.required && (value === '' || value === null || value === undefined)) {
      return `${field.label} is required`
    }

    if (field.type === 'number' && value !== '' && value !== null && value !== undefined) {
      const num = Number(value)
      if (isNaN(num)) return `${field.label} must be a number`
      if (field.min !== undefined && num < field.min) {
        return `${field.label} must be at least ${field.min} ${field.unit || ''}`.trim()
      }
      if (field.max !== undefined && num > field.max) {
        return `${field.label} must be no more than ${field.max} ${field.unit || ''}`.trim()
      }
    }

    if (field.type === 'select' && meta) {
      const options = name === 'crop' ? meta.supported_crops : meta.supported_soil_types
      if (value && !options.includes(value)) {
        return `${field.label} must be one of: ${options.join(', ')}`
      }
    }

    return null
  }, [])

  const handleBlur = useCallback((value, name) => {
    const error = validateField(name, value, metadata)
    onBlur(name, value, error)
  }, [metadata, onBlur, validateField])

  const handleSubmit = (e) => {
    e.preventDefault()
    const newErrors = {}
    let hasErrors = false

    FIELD_CONFIG.forEach(field => {
      const value = formData[field.id]
      const error = validateField(field.id, value, metadata)
      if (error) {
        newErrors[field.id] = error
        hasErrors = true
      }
    })

    if (hasErrors) {
      onSubmit(newErrors)
      return
    }

    onSubmit(null)
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit} noValidate aria-busy={loading}>
      {metadataError && (
        <div className={styles.metaBanner} role="status" aria-live="polite">
          <span aria-hidden="true">⚠</span>
          <span>Using demo data — backend unavailable</span>
        </div>
      )}

      <h2 className={styles.sectionTitle}>AGRICULTURAL CONDITIONS</h2>

      <div className={styles.grid}>
        <InputField
          id="crop"
          label="Crop"
          type="select"
          value={formData.crop || ''}
          onChange={(v) => onChange('crop', v)}
          onBlur={handleBlur}
          error={formErrors.crop}
          required
          options={metadata?.supported_crops || []}
          disabled={disabled || loading}
          aria-describedby={formErrors.crop ? 'crop-error' : undefined}
        />

        <InputField
          id="soil_type"
          label="Soil type"
          type="select"
          value={formData.soil_type || ''}
          onChange={(v) => onChange('soil_type', v)}
          onBlur={handleBlur}
          error={formErrors.soil_type}
          required
          options={metadata?.supported_soil_types || []}
          disabled={disabled || loading}
          aria-describedby={formErrors.soil_type ? 'soil-error' : undefined}
        />

        <InputField
          id="rainfall"
          label="Rainfall"
          type="number"
          value={formData.rainfall !== undefined ? formData.rainfall : ''}
          onChange={(v) => onChange('rainfall', v === '' ? '' : Number(v))}
          onBlur={handleBlur}
          error={formErrors.rainfall}
          required
          unit="mm"
          min={0}
          max={5000}
          step={1}
          placeholder="1200"
          disabled={disabled || loading}
          aria-describedby={formErrors.rainfall ? 'rainfall-error' : undefined}
        />

        <InputField
          id="temperature"
          label="Temperature"
          type="number"
          value={formData.temperature !== undefined ? formData.temperature : ''}
          onChange={(v) => onChange('temperature', v === '' ? '' : Number(v))}
          onBlur={handleBlur}
          error={formErrors.temperature}
          required
          unit="°C"
          min={-10}
          max={60}
          step={0.1}
          placeholder="27.5"
          disabled={disabled || loading}
          aria-describedby={formErrors.temperature ? 'temp-error' : undefined}
        />

        <InputField
          id="humidity"
          label="Humidity"
          type="number"
          value={formData.humidity !== undefined ? formData.humidity : ''}
          onChange={(v) => onChange('humidity', v === '' ? '' : Number(v))}
          onBlur={handleBlur}
          error={formErrors.humidity}
          required
          unit="%"
          min={0}
          max={100}
          step={1}
          placeholder="72"
          disabled={disabled || loading}
          aria-describedby={formErrors.humidity ? 'humidity-error' : undefined}
        />

        <InputField
          id="fertilizer"
          label="Fertilizer"
          type="number"
          value={formData.fertilizer !== undefined ? formData.fertilizer : ''}
          onChange={(v) => onChange('fertilizer', v === '' ? '' : Number(v))}
          onBlur={handleBlur}
          error={formErrors.fertilizer}
          required={false}
          unit="kg/ha"
          min={0}
          max={2000}
          step={1}
          placeholder="150"
          disabled={disabled || loading}
          aria-describedby={formErrors.fertilizer ? 'fertilizer-error' : undefined}
        />

        <InputField
          id="area"
          label="Area"
          type="number"
          value={formData.area !== undefined ? formData.area : ''}
          onChange={(v) => onChange('area', v === '' ? '' : Number(v))}
          onBlur={handleBlur}
          error={formErrors.area}
          required
          unit="ha"
          min={0.1}
          max={10000}
          step={0.1}
          placeholder="10"
          disabled={disabled || loading}
          aria-describedby={formErrors.area ? 'area-error' : undefined}
        />
      </div>

      <div className={styles.submitWrapper}>
        <button
          type="submit"
          className={`${styles.submitBtn} ${loading ? styles.loading : ''}`}
          disabled={loading || disabled}
          aria-busy={loading}
        >
          {loading ? 'Analyzing…' : 'Predict yield →'}
        </button>
      </div>
    </form>
  )
}