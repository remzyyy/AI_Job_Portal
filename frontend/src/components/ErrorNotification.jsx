import { useEffect } from 'react'

export default function ErrorNotification({ message, onDismiss }) {
  useEffect(() => {
    if (!message) return
    const timer = setTimeout(onDismiss, 5000)
    return () => clearTimeout(timer)
  }, [message, onDismiss])

  if (!message) return null

  return (
    <div className="error-toast" role="alert">
      <span>{message}</span>
      <button className="error-toast-close" onClick={onDismiss}>
        &times;
      </button>
    </div>
  )
}
