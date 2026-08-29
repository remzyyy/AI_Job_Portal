import { useEffect, useState } from 'react'
import { profileApi } from '../../services/api.js'
import { useApi } from '../../hooks/useApi.js'
import ErrorNotification from '../../components/ErrorNotification.jsx'
import FormField from '../../components/FormField.jsx'
import TagInput from '../../components/TagInput.jsx'
import LoadingSpinner from '../../components/LoadingSpinner.jsx'

export default function Profile() {
  const [exists, setExists] = useState(false)
  const [saved, setSaved] = useState(false)
  const { loading, error, run, clearError } = useApi()
  const [form, setForm] = useState({
    name: '',
    skills: [],
    education: [],
    project_summaries: [],
    preferred_location: '',
    role_type: '',
    domain_interest: '',
  })
  const [errors, setErrors] = useState({})

  useEffect(() => {
    run(() => profileApi.get())
      .then((res) => {
        setExists(true)
        setForm({
          name: res.data.name || '',
          skills: res.data.skills || [],
          education: res.data.education || [],
          project_summaries: res.data.project_summaries || [],
          preferred_location: res.data.preferred_location || '',
          role_type: res.data.role_type || '',
          domain_interest: res.data.domain_interest || '',
        })
      })
      .catch(() => setExists(false))
  }, [run])

  const validate = () => {
    const e = {}
    if (!form.name.trim()) e.name = 'Name is required'
    if (form.skills.length === 0) e.skills = 'Add at least one skill'
    if (form.education.length === 0) e.education = 'Add at least one education entry'
    setErrors(e)
    return Object.keys(e).length === 0
  }

  const submit = async (ev) => {
    ev.preventDefault()
    setSaved(false)
    if (!validate()) return
    try {
      if (exists) await run(() => profileApi.update(form))
      else {
        await run(() => profileApi.create(form))
        setExists(true)
      }
      setSaved(true)
    } catch {
      /* handled */
    }
  }

  return (
    <div>
      <ErrorNotification message={error} onDismiss={clearError} />
      <h1>My Profile</h1>
      {saved && <div className="success-banner">Profile saved successfully.</div>}

      <form onSubmit={submit} className="form-card">
        <FormField label="Name" error={errors.name}>
          <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
        </FormField>

        <FormField label="Skills (1-50)" error={errors.skills}>
          <TagInput tags={form.skills} onChange={(v) => setForm({ ...form, skills: v })} placeholder="e.g. Python" />
        </FormField>

        <FormField label="Education (1-20)" error={errors.education}>
          <TagInput tags={form.education} onChange={(v) => setForm({ ...form, education: v })} placeholder="e.g. BS Computer Science - MIT" />
        </FormField>

        <FormField label="Project Summaries (0-20)">
          <TagInput tags={form.project_summaries} onChange={(v) => setForm({ ...form, project_summaries: v })} placeholder="Short project description" />
        </FormField>

        <div className="form-row">
          <FormField label="Preferred Location">
            <input value={form.preferred_location} onChange={(e) => setForm({ ...form, preferred_location: e.target.value })} />
          </FormField>
          <FormField label="Role Type">
            <input value={form.role_type} onChange={(e) => setForm({ ...form, role_type: e.target.value })} />
          </FormField>
          <FormField label="Domain Interest">
            <input value={form.domain_interest} onChange={(e) => setForm({ ...form, domain_interest: e.target.value })} />
          </FormField>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? <LoadingSpinner size={16} /> : exists ? 'Update Profile' : 'Create Profile'}
          </button>
        </div>
      </form>
    </div>
  )
}
