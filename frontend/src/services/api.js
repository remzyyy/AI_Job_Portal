import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

// Attach token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Normalize error messages
api.interceptors.response.use(
  (response) => response,
  (error) => {
    let message = 'An unexpected error occurred'
    if (error.response) {
      const data = error.response.data
      if (data.error) message = data.error
      else if (data.detail) message = data.detail
      if (data.details && Array.isArray(data.details)) {
        message = data.details.map((d) => `${d.field}: ${d.message}`).join(', ')
      }
    } else if (error.request) {
      message = 'Connection failed. Is the backend running?'
    }
    return Promise.reject(new Error(message))
  }
)

export default api

// Auth
export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
}

// Jobs
export const jobApi = {
  create: (data) => api.post('/jobs', data),
  search: (params) => api.get('/jobs', { params }),
  get: (id) => api.get(`/jobs/${id}`),
  update: (id, data) => api.put(`/jobs/${id}`, data),
  updateStatus: (id, status) => api.patch(`/jobs/${id}/status`, { status }),
}

// Candidate profile
export const profileApi = {
  create: (data) => api.post('/candidates/profile', data),
  get: () => api.get('/candidates/profile'),
  update: (data) => api.put('/candidates/profile', data),
}

// Applications
export const applicationApi = {
  apply: (jobId) => api.post(`/jobs/${jobId}/apply`),
  forJob: (jobId, page = 1) => api.get(`/jobs/${jobId}/applications`, { params: { page } }),
  updateStatus: (appId, status) => api.patch(`/applications/${appId}/status`, { status }),
  mine: (page = 1) => api.get('/candidates/applications', { params: { page } }),
}

// Matching
export const matchApi = {
  match: (query) => api.post('/matching', { query }),
}

// Analytics
export const analyticsApi = {
  dashboard: () => api.get('/admin/dashboard'),
}
