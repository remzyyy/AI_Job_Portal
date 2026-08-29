import { useEffect, useState, useCallback } from 'react'
import { applicationApi } from '../../services/api.js'
import { useApi } from '../../hooks/useApi.js'
import ErrorNotification from '../../components/ErrorNotification.jsx'
import Pagination from '../../components/Pagination.jsx'
import LoadingSpinner from '../../components/LoadingSpinner.jsx'

export default function MyApplications() {
  const [apps, setApps] = useState([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const { loading, error, run, clearError } = useApi()

  const load = useCallback(() => {
    run(() => applicationApi.mine(page))
      .then((res) => {
        setApps(res.data.items)
        setTotalPages(res.data.total_pages)
      })
      .catch(() => {})
  }, [run, page])

  useEffect(() => {
    load()
  }, [load])

  return (
    <div>
      <ErrorNotification message={error} onDismiss={clearError} />
      <h1>My Applications</h1>

      {loading && <LoadingSpinner size={32} />}
      {!loading && apps.length === 0 && <p className="muted">You haven't applied to any jobs yet.</p>}

      <div className="app-list">
        {apps.map((app) => (
          <div key={app.id} className="app-card">
            <div className="app-info">
              <strong>{app.job_title}</strong>
              <span className="muted">Applied {new Date(app.applied_at).toLocaleDateString()}</span>
            </div>
            <span className={`badge status ${app.status.toLowerCase()}`}>{app.status}</span>
          </div>
        ))}
      </div>

      <Pagination page={page} totalPages={totalPages} onChange={setPage} />
    </div>
  )
}
