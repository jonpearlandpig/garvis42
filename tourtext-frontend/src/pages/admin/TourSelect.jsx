import React, { useEffect, useState } from 'react'
import { getTours, createTour } from '../../api'

export default function TourSelect({ onTourSelected }) {
  const [tours, setTours] = useState([])
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [form, setForm] = useState({ name: '', start_date: '', tour_code: '' })
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    getTours()
      .then(setTours)
      .catch(() => setError('Could not load tours.'))
      .finally(() => setLoading(false))
  }, [])

  async function handleCreate(e) {
    e.preventDefault()
    setError('')
    setCreating(true)
    try {
      const payload = {
        name: form.name,
        start_date: form.start_date || null,
        multi_tour_access: false,
      }
      const tour = await createTour(payload)
      onTourSelected(tour)
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not create tour.')
    } finally {
      setCreating(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32 text-tt-muted">Loading tours…</div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Your tours</h1>
          <p className="text-tt-muted text-sm mt-1">Select a tour to manage or create a new one.</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-tt-blue hover:bg-blue-500 text-white text-sm font-semibold px-5 py-2.5 rounded-lg"
        >
          + New tour
        </button>
      </div>

      {error && (
        <div className="bg-red-900/30 border border-red-500/50 text-red-400 text-sm px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {/* Create form */}
      {showForm && (
        <div className="bg-tt-card border border-tt-border rounded-lg p-6 mb-8">
          <h2 className="text-white font-semibold mb-5">Create new tour</h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-tt-muted text-sm mb-1.5">Tour name *</label>
              <input
                required
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                className="w-full bg-tt-dark border border-tt-border rounded px-4 py-2.5 text-white focus:outline-none focus:border-tt-blue"
                placeholder="e.g. Summer Headline Tour 2026"
              />
            </div>
            <div>
              <label className="block text-tt-muted text-sm mb-1.5">Start date</label>
              <input
                type="date"
                value={form.start_date}
                onChange={(e) => setForm({ ...form, start_date: e.target.value })}
                className="w-full bg-tt-dark border border-tt-border rounded px-4 py-2.5 text-white focus:outline-none focus:border-tt-blue"
              />
            </div>
            <div className="flex gap-3 pt-2">
              <button
                type="submit"
                disabled={creating}
                className="bg-tt-blue hover:bg-blue-500 disabled:opacity-50 text-white text-sm font-semibold px-6 py-2.5 rounded-lg"
              >
                {creating ? 'Creating…' : 'Create tour'}
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="text-tt-muted hover:text-white text-sm px-4 py-2.5"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Tour list */}
      {tours.length === 0 ? (
        <div className="text-center py-20 text-tt-muted">
          <p className="text-lg mb-2">No tours yet.</p>
          <p className="text-sm">Click "+ New tour" to get started.</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-4">
          {tours.map((t) => (
            <button
              key={t.tour_id}
              onClick={() => onTourSelected(t)}
              className="bg-tt-card border border-tt-border hover:border-tt-blue rounded-lg p-5 text-left transition-colors"
            >
              <div className="flex items-start justify-between mb-3">
                <span className="text-white font-semibold">{t.name}</span>
                <span className="bg-blue-900/40 text-tt-blue text-xs font-mono px-2 py-1 rounded">
                  {t.tour_code}
                </span>
              </div>
              {t.start_date && (
                <div className="text-tt-muted text-xs font-mono">
                  {new Date(t.start_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                </div>
              )}
              <div className="text-tt-muted text-xs mt-2 font-mono truncate">TID: {t.taid}</div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
