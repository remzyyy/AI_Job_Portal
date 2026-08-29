import { useState } from 'react'
import { matchApi, applicationApi } from '../../services/api.js'
import { useApi } from '../../hooks/useApi.js'
import ErrorNotification from '../../components/ErrorNotification.jsx'
import LoadingSpinner from '../../components/LoadingSpinner.jsx'

export default function AIMatching() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState(null)
  const [message, setMessage] = useState('')
  const [applied, setApplied] = useState({})
  const { loading, error, run, clearError } = useApi()

  const submit = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    setResults(null)
    setMessage('')
    try {
      const res = await run(() => matchApi.match(query))
      setResults(res.data.results)
      if (res.data.message) setMessage(res.data.message)
    } catch {
      /* handled */
    }
  }

  const applyToJob = async (jobId) => {
    try {
      await run(() => applicationApi.apply(jobId))
      setApplied({ ...applied, [jobId]: true })
    } catch {
      /* handled */
    }
  }

  const scoreColor = (score) => {
    if (score >= 70) return 'high'
    if (score >= 40) return 'mid'
    return 'low'
  }

  return (
    <div>
      <ErrorNotification message={error} onDismiss={clearError} />
      <div className="hero">
        <h1>✨ AI Job Matching</h1>
        <p>
          Describe your ideal role in plain English and let AI rank the best matches for you.
          Try: <em>"I want a Python backend role in a startup that does healthcare."</em>
        </p>
      </div>

      <form onSubmit={submit} className="match-form">
        <textarea
          rows={3}
          maxLength={1000}
          value={query}
          placeholder="Describe what you're looking for..."
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" className="btn-primary" disabled={loading || !query.trim()}>
          {loading ? <LoadingSpinner size={16} /> : 'Find Matches'}
        </button>
      </form>

      {message && <p className="muted">{message}</p>}

      {results && results.length > 0 && (
        <div className="match-results">
          {results.map((r) => (
            <div key={r.job_id} className="match-card">
              <div className="match-header">
                <h3>{r.title}</h3>
                <span className={`score-badge ${scoreColor(r.score)}`}>{r.score}% match</span>
              </div>
              <p className="match-explanation">{r.explanation}</p>
              <button
                className="btn-primary"
                disabled={applied[r.job_id]}
                onClick={() => applyToJob(r.job_id)}
              >
                {applied[r.job_id] ? 'Applied' : 'Apply'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
