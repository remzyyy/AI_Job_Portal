import { useEffect, useState, useCallback } from 'react'
import { jobApi, applicationApi } from '../../services/api.js'
import { useApi } from '../../hooks/useApi.js'
import ErrorNotification from '../../components/ErrorNotification.jsx'
import Pagination from '../../components/Pagination.jsx'
import LoadingSpinner from '../../components/LoadingSpinner.jsx'
import { LEVELS, LOCATIONS, SKILLS } from '../../constants/options.js'

const LEVEL_OPTIONS = ['', ...LEVELS]

export default function JobSearch() {
  const [jobs, setJobs] = useState([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [filters, setFilters] = useState({ skill: '', location: '', experience_level: '' })
  const [applied, setApplied] = useState({})
  const [message, setMessage] = useState('')
  const { loading, error, run, clearError } = useApi()

  const search = useCallback(() => {
    const params = { page }
    if (filters.skill) params.skill = filters.skill
    if (filters.location) params.location = filters.location
    if (filters.experience_level) params.experience_level = filters.experience_level
    run(() => jobApi.search(params))
      .then((res) => {
        setJobs(res.data.items)
        setTotalPages(res.data.total_pages)
      })
      .catch(() => {})
  }, [run, page, filters])

  useEffect(() => {
    search()
  }, [page])

  const applyToJob = async (jobId) => {
    setMessage('')
    try {
      await run(() => applicationApi.apply(jobId))
      setApplied({ ...applied, [jobId]: true })
      setMessage('Application submitted!')
    } catch {
      /* handled */
    }
  }

  return (
    <div>
      <ErrorNotification message={error} onDismiss={clearError} />
      <h1>Browse Jobs</h1>
      {message && <div className="success-banner">{message}</div>}

      <div className="filter-bar">
        <input
          list="skill-filter-options"
          placeholder="Skill"
          value={filters.skill}
          onChange={(e) => setFilters({ ...filters, skill: e.target.value })}
        />
        <datalist id="skill-filter-options">
          {SKILLS.map((s) => (
            <option key={s} value={s} />
          ))}
        </datalist>
        <input
          list="location-filter-options"
          placeholder="Location"
          value={filters.location}
          onChange={(e) => setFilters({ ...filters, location: e.target.value })}
        />
        <datalist id="location-filter-options">
          {LOCATIONS.map((loc) => (
            <option key={loc} value={loc} />
          ))}
        </datalist>
        <select
          value={filters.experience_level}
          onChange={(e) => setFilters({ ...filters, experience_level: e.target.value })}
        >
          {LEVEL_OPTIONS.map((l) => (
            <option key={l} value={l}>{l || 'Any level'}</option>
          ))}
        </select>
        <button className="btn-primary" onClick={() => { setPage(1); search() }}>Search</button>
      </div>

      {loading && <LoadingSpinner size={32} />}
      {!loading && jobs.length === 0 && <p className="muted">No matching jobs found.</p>}

      <div className="job-grid">
        {jobs.map((job) => (
          <div key={job.id} className="job-card">
            <h3>{job.title}</h3>
            <p className="muted">{job.experience_level} · {job.location}</p>
            <p className="job-desc">{job.description.slice(0, 150)}...</p>
            <div className="skill-tags">
              {job.required_skills.map((s) => (
                <span key={s} className="tag readonly">{s}</span>
              ))}
            </div>
            <button
              className="btn-primary"
              disabled={applied[job.id]}
              onClick={() => applyToJob(job.id)}
            >
              {applied[job.id] ? 'Applied' : 'Apply'}
            </button>
          </div>
        ))}
      </div>

      <Pagination page={page} totalPages={totalPages} onChange={setPage} />
    </div>
  )
}
