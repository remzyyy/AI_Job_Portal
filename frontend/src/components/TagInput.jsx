import { useState, useId } from 'react'

// A multi-value input: type and press Enter (or pick a suggestion) to add a tag.
// Optional `suggestions` provides an autocomplete datalist.
export default function TagInput({ tags, onChange, placeholder, suggestions = [] }) {
  const [value, setValue] = useState('')
  const listId = useId()

  const addTag = (raw) => {
    const trimmed = (raw ?? value).trim()
    if (trimmed && !tags.includes(trimmed)) {
      onChange([...tags, trimmed])
    }
    setValue('')
  }

  const removeTag = (tag) => {
    onChange(tags.filter((t) => t !== tag))
  }

  // Suggestions not already selected
  const available = suggestions.filter((s) => !tags.includes(s))

  return (
    <div className="tag-input">
      <div className="tag-list">
        {tags.map((tag) => (
          <span key={tag} className="tag">
            {tag}
            <button type="button" onClick={() => removeTag(tag)}>
              &times;
            </button>
          </span>
        ))}
      </div>
      <input
        type="text"
        value={value}
        list={suggestions.length ? listId : undefined}
        placeholder={placeholder || 'Type and press Enter'}
        onChange={(e) => {
          const v = e.target.value
          setValue(v)
          // If the typed value exactly matches a suggestion (datalist pick), add it.
          if (suggestions.includes(v)) addTag(v)
        }}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            e.preventDefault()
            addTag()
          }
        }}
        onBlur={() => addTag()}
      />
      {suggestions.length > 0 && (
        <datalist id={listId}>
          {available.map((s) => (
            <option key={s} value={s} />
          ))}
        </datalist>
      )}
    </div>
  )
}
