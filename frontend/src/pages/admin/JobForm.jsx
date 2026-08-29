import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { jobApi } from '../../services/api.js'
import { useApi } from '../../hooks/useApi.js'
import ErrorNotification from '../../components/ErrorNotification.jsx'
import FormField from '../../components/FormField.jsx'
import TagInput from '../../components/TagInput.jsx'
import LoadingSpinner from '../../components/LoadingSpinner.jsx'
import { LEVELS, LOCATIONS, SKILLS } from '../../constants/options.js'

export default function JobForm() {
  const { id } = useParams()
  const isEdit = Boolean(id)
  const navigate = useNavigate()
  const { loading, error, run, clearError } = useApi()

  const [form, setForm] = useState({
    title: '',
    description: '',
    required_skills: [],
    experience_level: 'Mid',
    location: '',
  })
  const [errors, setErrors] = useState({})

  useEffect(() => {
    if (isEdit) {
      run(() => jobApi.get(id))
        .then((res) => setForm({
          title: res.data.title,
          description: res.data.description,
          required_skills: res.data.required_skills,
          experience_level: res.data.experience_level,
          location: res.data.location,
        }))
        .catch(() => {})
    }
  }, [id, isEdit, run])

  const validate = () => {
    const e = {}
    if (!form.title.trim()) e.title = 'Title is required'
    else if (form.title.length > 150) e.title = 'Title must be under 150 characters'
    if (!form.description.trim()) e.description = 'Description is required'
    else if (form.description.length > 5000) e.description = 'Description must be under 5000 characters'
    if (form.required_skills.length === 0) e.required_skills = 'Add at least one skill'
    else if (form.required_skills.length > 20) e.required_skills = 'Maximum 20 skills'
    if (!form.location.trim()) e.location = 'Location is required'
    setErrors(e)
    return Object.keys(e).length === 0
  }

  const submit = async (ev) => {
    ev.preventDefault()
    if (!validate()) return
    try {
      if (isEdit) await run(() => jobApi.update(id, form))
      else await run(() => jobApi.create(form))
      navigate('/admin/jobs')
    } catch {
      /* handled */
    }
  }

  return (
    <div>
      <ErrorNotification message={error} onDismiss={clearError} />
      <h1>{isEdit ? 'Edit Job' : 'Create Job'}</h1>

      <form onSubmit={submit} className="form-card">
        <FormField label="Title" error={errors.title}>
          <input
            value={form.title}
            maxLength={150}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
          />
        </FormField>

        <FormField label="Description" error={errors.description}>
          <textarea
            rows={6}
            value={form.description}
            maxLength={5000}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
        </FormField>

        <FormField label="Required Skills (1-20)" error={errors.required_skills}>
          <TagInput
            tags={form.required_skills}
            onChange={(skills) => setForm({ ...form, required_skills: skills })}
            placeholder="Type or pick a skill, then press Enter"
            suggestions={SKILLS}
          />
        </FormField>

        <FormField label="Experience Level">
          <select
            value={form.experience_level}
            onChange={(e) => setForm({ ...form, experience_level: e.target.value })}
          >
            {LEVELS.map((l) => (
              <option key={l} value={l}>{l}</option>
            ))}
          </select>
        </FormField>

        <FormField label="Location" error={errors.location}>
          <input
            list="location-options"
            value={form.location}
            placeholder="Search or pick a location (worldwide + all Indian states)"
            onChange={(e) => setForm({ ...form, location: e.target.value })}
          />
          <datalist id="location-options">
            {LOCATIONS.map((loc) => (
              <option key={loc} value={loc} />
            ))}
          </datalist>
        </FormField>

        <div className="form-actions">
          <button type="button" onClick={() => navigate('/admin/jobs')}>Cancel</button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? <LoadingSpinner size={16} /> : isEdit ? 'Save Changes' : 'Create Job'}
          </button>
        </div>
      </form>
    </div>
  )
}
