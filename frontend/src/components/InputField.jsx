import { forwardRef } from 'react'
import styles from './InputField.module.css'

const InputField = forwardRef(function InputField({
  id,
  label,
  type = 'text',
  value,
  onChange,
  onBlur,
  error,
  disabled,
  required,
  unit,
  options,
  placeholder,
  'aria-describedby': ariaDescribedBy,
  ...props
}, ref) {
  const hasError = !!error
  const isSelect = !!options

  const handleChange = (e) => {
    onChange?.(e.target.value)
  }

  const handleBlur = (e) => {
    onBlur?.(e.target.value, id)
  }

  return (
    <div className={styles.wrapper}>
      <label htmlFor={id} className={styles.label}>
        {label}
        {required && <span className={styles.required} aria-hidden="true">*</span>}
      </label>
      <div className={styles.inputWrapper}>
        {isSelect ? (
          <select
            ref={ref}
            id={id}
            className={`${styles.input} ${styles.select}`}
            value={value}
            onChange={handleChange}
            onBlur={handleBlur}
            disabled={disabled}
            required={required}
            aria-invalid={hasError}
            aria-describedby={ariaDescribedBy}
            {...props}
          >
            <option value="" disabled>Select {label.toLowerCase()}</option>
            {options.map((opt) => (
              <option key={opt} value={opt}>{opt}</option>
            ))}
          </select>
        ) : (
          <input
            ref={ref}
            id={id}
            type={type}
            className={`${styles.input} ${hasError ? styles.invalid : ''} ${disabled ? styles.disabled : ''}`}
            value={value}
            onChange={handleChange}
            onBlur={handleBlur}
            disabled={disabled}
            required={required}
            placeholder={placeholder}
            aria-invalid={hasError}
            aria-describedby={ariaDescribedBy}
            {...props}
          />
        )}
        {unit && <span className={styles.unit} aria-hidden="true">{unit}</span>}
      </div>
      {hasError && (
        <p id={ariaDescribedBy} className={styles.errorMessage} role="alert">
          {error}
        </p>
      )}
    </div>
  )
})

InputField.displayName = 'InputField'

export default InputField