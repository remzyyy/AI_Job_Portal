import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authApi } from '../services/api.js'
import { useAuth } from '../context/AuthContext.jsx'
import { useApi } from '../hooks/useApi.js'
import ErrorNotification from '../components/ErrorNotification.jsx'
import LoadingSpinner from '../components/LoadingSpinner.jsx'

export default function Login() {
  const [mode, setMode] = useState('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('candidate')
  const { login } = useAuth()
  const { loading, error, run, clearError } = useApi()
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    try {
      const res = await run(() =>
        mode === 'login'
          ? authApi.login({ email, password })
          : authApi.register({ email, password, role })
      )
      login(res.data)
      navigate(res.data.role === 'admin' ? '/admin/dashboard' : '/candidate/search')
    } catch {
      /* error shown via notification */
    }
  }

  return (
    <div className="auth-page">
      <ErrorNotification message={error} onDismiss={clearError} />
      <div className="auth-card">
        <h1>AI Job Board</h1>
        <div className="auth-tabs">
          <button className={mode === 'login' ? 'active' : ''} onClick={() => setMode('login')}>
            Login
          </button>
          <button className={mode === 'register' ? 'active' : ''} onClick={() => setMode('register')}>
            Register
          </button>
        </div>
        <form onSubmit={submit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            required
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            required
            onChange={(e) => setPassword(e.target.value)}
          />
          {mode === 'register' && (
            <select value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="candidate">Candidate</option>
              <option value="admin">Company Admin</option>
            </select>
          )}
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? <LoadingSpinner size={16} /> : mode === 'login' ? 'Login' : 'Register'}
          </button>
        </form>
        <div className="auth-hint">
          <p>Demo accounts:</p>
          <p>admin@example.com / admin123</p>
          <p>candidate@example.com / candidate123</p>
        </div>
      </div>
    </div>
  )
}
