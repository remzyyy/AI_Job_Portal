import { Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext.jsx'

import Login from './pages/Login.jsx'
import Dashboard from './pages/admin/Dashboard.jsx'
import JobManager from './pages/admin/JobManager.jsx'
import JobForm from './pages/admin/JobForm.jsx'
import ApplicationReview from './pages/admin/ApplicationReview.jsx'
import Profile from './pages/candidate/Profile.jsx'
import JobSearch from './pages/candidate/JobSearch.jsx'
import AIMatching from './pages/candidate/AIMatching.jsx'
import MyApplications from './pages/candidate/MyApplications.jsx'

function NavBar() {
  const { auth, logout } = useAuth()
  const navigate = useNavigate()

  if (!auth) return null

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-brand">AI Job Board</div>
      <div className="navbar-links">
        {auth.role === 'admin' ? (
          <>
            <Link to="/admin/dashboard">Dashboard</Link>
            <Link to="/admin/jobs">Jobs</Link>
          </>
        ) : (
          <>
            <Link to="/candidate/search">Browse Jobs</Link>
            <Link to="/candidate/match">AI Match</Link>
            <Link to="/candidate/profile">Profile</Link>
            <Link to="/candidate/applications">My Applications</Link>
          </>
        )}
        <span className="navbar-role">{auth.role}</span>
        <button className="btn-link" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  )
}

function RequireRole({ role, children }) {
  const { auth } = useAuth()
  if (!auth) return <Navigate to="/login" replace />
  if (auth.role !== role) {
    return <Navigate to={auth.role === 'admin' ? '/admin/dashboard' : '/candidate/search'} replace />
  }
  return children
}

function HomeRedirect() {
  const { auth } = useAuth()
  if (!auth) return <Navigate to="/login" replace />
  return <Navigate to={auth.role === 'admin' ? '/admin/dashboard' : '/candidate/search'} replace />
}

export default function App() {
  return (
    <>
      <NavBar />
      <main className="container">
        <Routes>
          <Route path="/login" element={<Login />} />

          {/* Admin routes */}
          <Route path="/admin/dashboard" element={<RequireRole role="admin"><Dashboard /></RequireRole>} />
          <Route path="/admin/jobs" element={<RequireRole role="admin"><JobManager /></RequireRole>} />
          <Route path="/admin/jobs/new" element={<RequireRole role="admin"><JobForm /></RequireRole>} />
          <Route path="/admin/jobs/:id/edit" element={<RequireRole role="admin"><JobForm /></RequireRole>} />
          <Route path="/admin/jobs/:id/applications" element={<RequireRole role="admin"><ApplicationReview /></RequireRole>} />

          {/* Candidate routes */}
          <Route path="/candidate/profile" element={<RequireRole role="candidate"><Profile /></RequireRole>} />
          <Route path="/candidate/search" element={<RequireRole role="candidate"><JobSearch /></RequireRole>} />
          <Route path="/candidate/match" element={<RequireRole role="candidate"><AIMatching /></RequireRole>} />
          <Route path="/candidate/applications" element={<RequireRole role="candidate"><MyApplications /></RequireRole>} />

          <Route path="/" element={<HomeRedirect />} />
          <Route path="*" element={<HomeRedirect />} />
        </Routes>
      </main>
    </>
  )
}
