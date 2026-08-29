import { useEffect, useState } from 'react'
import { analyticsApi } from '../../services/api.js'
import { useApi } from '../../hooks/useApi.js'
import ErrorNotification from '../../components/ErrorNotification.jsx'
import LoadingSpinner from '../../components/LoadingSpinner.jsx'

export default function Dashboard() {
  const [data, setData] = useState(null)
  const { loading, error, run, clearError } = useApi()

  useEffect(() => {
    run(() => analyticsApi.dashboard()).then((res) => setData(res.data)).catch(() => {})
  }, [run])

  if (loading) return <LoadingSpinner size={40} />
  if (!data) return <ErrorNotification message={error} onDismiss={clearError} />

  const maxJobCount = Math.max(1, ...data.applications_per_job.map((j) => j.count))
  const maxSkillCount = Math.max(1, ...data.skills_distribution.map((s) => s.count))

  return (
    <div>
      <ErrorNotification message={error} onDismiss={clearError} />
      <h1>Dashboard</h1>

      <div className="dashboard-grid">
        <div className="card">
          <h2>Pipeline Status</h2>
          <div className="status-counts">
            <div className="status-pill applied">
              <span className="num">{data.status_breakdown.Applied}</span>
              <span>Applied</span>
            </div>
            <div className="status-pill shortlisted">
              <span className="num">{data.status_breakdown.Shortlisted}</span>
              <span>Shortlisted</span>
            </div>
            <div className="status-pill rejected">
              <span className="num">{data.status_breakdown.Rejected}</span>
              <span>Rejected</span>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Applications per Job</h2>
          {data.applications_per_job.length === 0 ? (
            <p className="muted">No jobs yet</p>
          ) : (
            data.applications_per_job.map((j) => (
              <div key={j.job_id} className="bar-row">
                <span className="bar-label">{j.title}</span>
                <div className="bar-track">
                  <div className="bar-fill" style={{ width: `${(j.count / maxJobCount) * 100}%` }} />
                </div>
                <span className="bar-value">{j.count}</span>
              </div>
            ))
          )}
        </div>

        <div className="card">
          <h2>Skill Distribution</h2>
          {data.skills_distribution.length === 0 ? (
            <p className="muted">No applicants yet</p>
          ) : (
            data.skills_distribution.map((s) => (
              <div key={s.skill} className="bar-row">
                <span className="bar-label">{s.skill}</span>
                <div className="bar-track">
                  <div className="bar-fill skill" style={{ width: `${(s.count / maxSkillCount) * 100}%` }} />
                </div>
                <span className="bar-value">{s.count}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
