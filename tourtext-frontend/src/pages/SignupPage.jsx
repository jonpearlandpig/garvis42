import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { signup } from '../api'
import { useAuth } from '../AuthContext'

export default function SignupPage() {
  const nav = useNavigate()
  const { saveAuth } = useAuth()
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (form.password.length < 8) {
      setError('Password must be at least 8 characters.')
      return
    }
    setLoading(true)
    try {
      const data = await signup(form)
      saveAuth(data.token, { user_id: data.user_id, email: data.email, name: data.name })
      nav('/admin')
    } catch (err) {
      setError(err.response?.data?.detail || 'Signup failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-tt-dark flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <span className="text-tt-blue font-bold tracking-widest text-xl">TOURTEXT™</span>
          <p className="text-tt-muted text-sm mt-2">Create your account</p>
        </div>

        <div className="bg-tt-card border border-tt-border rounded-lg p-8">
          {error && (
            <div className="bg-red-900/30 border border-red-500/50 text-red-400 text-sm px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm text-tt-muted mb-2">Full name</label>
              <input
                type="text"
                required
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                className="w-full bg-tt-dark border border-tt-border rounded px-4 py-3 text-white focus:outline-none focus:border-tt-blue"
                placeholder="Your name"
              />
            </div>
            <div>
              <label className="block text-sm text-tt-muted mb-2">Email</label>
              <input
                type="email"
                required
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="w-full bg-tt-dark border border-tt-border rounded px-4 py-3 text-white focus:outline-none focus:border-tt-blue"
                placeholder="you@tourcompany.com"
              />
            </div>
            <div>
              <label className="block text-sm text-tt-muted mb-2">Password</label>
              <input
                type="password"
                required
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className="w-full bg-tt-dark border border-tt-border rounded px-4 py-3 text-white focus:outline-none focus:border-tt-blue"
                placeholder="Min. 8 characters"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-tt-blue hover:bg-blue-500 disabled:opacity-50 text-white font-semibold py-3 rounded-lg mt-2"
            >
              {loading ? 'Creating account…' : 'Create account'}
            </button>
          </form>

          <p className="text-tt-muted text-sm text-center mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-tt-blue hover:underline">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
