import { useEffect, useState, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { jobApi } from '../../services/api.js'
import { useAuth } from '../../context/AuthContext.jsx'
import { useApi } from '../../hooks/useApi.js'
import ErrorNotification from '../../components/ErrorNotification.jsx'
import Pagination from '../../components/Pagination.jsx'
import LoadingSpinner from '../../components/LoadingSpinner.jsx'

export default function JobManager() {
  const [jobs, setJobs] = useState([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const { auth } = useAuth()
  const { loading, error, run, clearError, setError } = useApi()
  const navigate = useNavigate()

  const loadJobs = useCallback(() => {
    run(() => jobApi.search({ page }))
      .then((res) => {
        // Admin sees only their own jobs
        const owned = res.data.items.filter((j) => String(j.admin_id) === String(auth.userId))
        setJobs(owned)
        setTotalPages(res.data.total_pages)
      })
      .catch(() => {})
  }, [run, page, auth.userId])

  useEffect(() => {
    loadJobs()
  }, [loadJobs])

  const toggleStatus = async (job) => {
    const newStatus = job.status === 'open' ? 'closed' : 'open'
    try {
      await run(() => jobApi.updateStatus(job.id, newStatus))
      loadJobs()
    } catch {
      /* handled */
    }
  }

  return (
    <div>
      <ErrorNotification message={error} onDismiss={clearError} />
      <div className="page-header">
        <h1>Job Listings</h1>
        <Link to="/admin/jobs/new" className="btn-primary">
          + New Job
        </Link>
      </div>

      {loading && <LoadingSpinner size={32} />}

      {!loading && jobs.length === 0 && <p className="muted">No jobs posted yet. Create your first listing.</p>}

      <div className="job-table">
        {jobs.map((job) => (
          <div key={job.id} className="job-row">
            <div className="job-row-main">
              <strong>{job.title}</strong>
              <span className={`badge ${job.status}`}>{job.status}</span>
              <span className="muted">{job.experience_level} · {job.location}</span>
            </div>
            <div className="job-row-actions">
              <button onClick={() => navigate(`/admin/jobs/${job.id}/applications`)}>
                Applications
              </button>
              <button onClick={() => navigate(`/admin/jobs/${job.id}/edit`)}>Edit</button>
              <button onClick={() => toggleStatus(job)}>
                {job.status === 'open' ? 'Close' : 'Reopen'}
              </button>
            </div>
          </div>
        ))}
      </div>

      <Pagination page={page} totalPages={totalPages} onChange={setPage} />
    </div>
  )
}
