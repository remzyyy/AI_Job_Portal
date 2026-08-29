import { useEffect, useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { applicationApi, jobApi } from '../../services/api.js'
import { useApi } from '../../hooks/useApi.js'
import ErrorNotification from '../../components/ErrorNotification.jsx'
import Pagination from '../../components/Pagination.jsx'
import LoadingSpinner from '../../components/LoadingSpinner.jsx'

const STATUSES = ['Applied', 'Shortlisted', 'Rejected']

export default function ApplicationReview() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [apps, setApps] = useState([])
  const [jobTitle, setJobTitle] = useState('')
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const { loading, error, run, clearError } = useApi()

  const load = useCallback(() => {
    run(() => applicationApi.forJob(id, page))
      .then((res) => {
        setApps(res.data.items)
        setTotalPages(res.data.total_pages)
      })
      .catch(() => {})
    jobApi.get(id).then((res) => setJobTitle(res.data.title)).catch(() => {})
  }, [run, id, page])

  useEffect(() => {
    load()
  }, [load])

  const changeStatus = async (appId, status) => {
    try {
      await run(() => applicationApi.updateStatus(appId, status))
      load()
    } catch {
      /* handled */
    }
  }

  return (
    <div>
      <ErrorNotification message={error} onDismiss={clearError} />
      <button className="btn-link" onClick={() => navigate('/admin/jobs')}>&larr; Back to Jobs</button>
      <h1>Applications: {jobTitle}</h1>

      {loading && <LoadingSpinner size={32} />}
      {!loading && apps.length === 0 && <p className="muted">No applications yet.</p>}

      <div className="app-list">
        {apps.map((app) => (
          <div key={app.id} className="app-card">
            <div className="app-info">
              <strong>{app.candidate_name}</strong>
              <div className="skill-tags">
                {(app.candidate_skills || []).map((s) => (
                  <span key={s} className="tag readonly">{s}</span>
                ))}
              </div>
              <span className="muted">Applied {new Date(app.applied_at).toLocaleDateString()}</span>
            </div>
            <select
              value={app.status}
              className={`status-select ${app.status.toLowerCase()}`}
              onChange={(e) => changeStatus(app.id, e.target.value)}
            >
              {STATUSES.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
        ))}
      </div>

      <Pagination page={page} totalPages={totalPages} onChange={setPage} />
    </div>
  )
}
