import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { login } from '../api'
import { useAuth } from '../AuthContext'

export default function LoginPage() {
  const nav = useNavigate()
  const { saveAuth } = useAuth()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await login(form)
      saveAuth(data.token, { user_id: data.user_id, email: data.email, name: data.name })
      nav('/admin')
    } catch (err) {
      setError(err.response?.data?.detail || 'Sign-in failed. Check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-tt-dark flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <span className="text-tt-blue font-bold tracking-widest text-xl">TOURTEXT™</span>
          <p className="text-tt-muted text-sm mt-2">Sign in to your account</p>
        </div>

        <div className="bg-tt-card border border-tt-border rounded-lg p-8">
          {error && (
            <div className="bg-red-900/30 border border-red-500/50 text-red-400 text-sm px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
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
                placeholder="Password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-tt-blue hover:bg-blue-500 disabled:opacity-50 text-white font-semibold py-3 rounded-lg mt-2"
            >
              {loading ? 'Signing in…' : 'Sign in'}
            </button>
          </form>

          <p className="text-tt-muted text-sm text-center mt-6">
            Don't have an account?{' '}
            <Link to="/signup" className="text-tt-blue hover:underline">Sign up free</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
