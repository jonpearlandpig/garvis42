import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getEscalations, resolveEscalation, submitQuery, getTruthRecords, getIntegrationStatus } from '../../api'

const POLICY_COLOR = {
  truth_record: 'text-green-400',
  normalized: 'text-yellow-400',
  escalate: 'text-orange-400',
  refusal: 'text-red-400',
  raw: 'text-tt-muted',
}

const CONFIDENCE_LABEL = (c) => {
  if (c >= 0.9) return { label: 'High', cls: 'text-green-400' }
  if (c >= 0.7) return { label: 'Med', cls: 'text-yellow-400' }
  return { label: 'Low', cls: 'text-red-400' }
}

const SEV_COLOR = { high: 'text-red-400', medium: 'text-yellow-400', low: 'text-tt-muted' }

export default function LiveStatus({ tour }) {
  const nav = useNavigate()
  const [tab, setTab] = useState('queries')
  const [escalations, setEscalations] = useState([])
  const [records, setRecords] = useState([])
  const [status, setStatus] = useState(null)
  const [query, setQuery] = useState('')
  const [phone, setPhone] = useState('')
  const [testResult, setTestResult] = useState(null)
  const [testing, setTesting] = useState(false)
  const [error, setError] = useState('')

  function refresh() {
    getEscalations(tour.tour_id).then(setEscalations).catch(() => {})
    getTruthRecords(tour.tour_id).then(setRecords).catch(() => {})
    getIntegrationStatus().then(setStatus).catch(() => {})
  }

  useEffect(() => {
    refresh()
    const interval = setInterval(refresh, 10000)
    return () => clearInterval(interval)
  }, [tour.tour_id])

  async function handleTest(e) {
    e.preventDefault()
    if (!query.trim()) return
    setTesting(true)
    setTestResult(null)
    setError('')
    try {
      const result = await submitQuery({ tour_code: tour.tour_code, query, phone: phone || undefined })
      setTestResult(result)
      refresh()
    } catch (err) {
      setError(err.response?.data?.detail || 'Query failed.')
    } finally {
      setTesting(false)
    }
  }

  async function handleResolve(taid) {
    try {
      await resolveEscalation(taid)
      setEscalations((prev) => prev.map((e) => e.taid === taid ? { ...e, status: 'resolved' } : e))
    } catch {}
  }

  const openEscalations = escalations.filter((e) => e.status === 'open')

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <button onClick={() => nav('/admin')} className="text-tt-muted hover:text-white text-sm">← Tours</button>
            <span className="text-tt-muted">›</span>
            <span className="text-tt-blue font-mono text-sm">{tour.tour_code}</span>
          </div>
          <h1 className="text-2xl font-bold text-white">{tour.name}</h1>
        </div>
        <div className="text-right">
          <div className="text-tt-muted text-xs mb-1">SMS number</div>
          <div className="text-white font-mono text-lg">888-340-0564</div>
          <div className="text-tt-muted text-xs">tour code: <span className="text-tt-blue">{tour.tour_code}</span></div>
        </div>
      </div>

      {/* Integration status bar */}
      {status && (
        <div className="bg-tt-card border border-tt-border rounded-lg px-5 py-3 mb-6 flex flex-wrap gap-4 text-xs font-mono">
          {Object.entries(status.integrations).map(([k, v]) => (
            <span key={k}>
              <span className="text-tt-muted">{k}: </span>
              <span className={v.includes('not_configured') ? 'text-yellow-400' : 'text-green-400'}>{v}</span>
            </span>
          ))}
          <span className="ml-auto text-tt-muted">
            {status.stats.truth_records} records · {status.stats.total_invocations} queries
          </span>
        </div>
      )}

      <div className="grid lg:grid-cols-5 gap-6">
        {/* Left: test query */}
        <div className="lg:col-span-2">
          <div className="bg-tt-card border border-tt-border rounded-lg p-5 mb-4">
            <h2 className="text-white font-semibold mb-4 text-sm">Test a query</h2>
            <form onSubmit={handleTest} className="space-y-3">
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full bg-tt-dark border border-tt-border rounded px-3 py-2.5 text-white text-sm focus:outline-none focus:border-tt-blue"
                placeholder="e.g. where is load-in tomorrow?"
              />
              <input
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full bg-tt-dark border border-tt-border rounded px-3 py-2.5 text-tt-muted text-sm focus:outline-none focus:border-tt-blue"
                placeholder="+1 phone (optional)"
              />
              <button
                type="submit"
                disabled={testing || !query.trim()}
                className="w-full bg-tt-blue hover:bg-blue-500 disabled:opacity-40 text-white text-sm font-semibold py-2.5 rounded-lg"
              >
                {testing ? 'Processing…' : 'Send query'}
              </button>
            </form>

            {error && <p className="text-red-400 text-xs mt-3">{error}</p>}

            {testResult && (
              <div className="mt-4 bg-tt-dark border border-tt-border rounded p-4 space-y-2">
                <div className="text-white text-sm">{testResult.answer}</div>
                <div className="flex gap-4 text-xs font-mono">
                  <span className={POLICY_COLOR[testResult.answer_policy] || 'text-tt-muted'}>
                    {testResult.answer_policy}
                  </span>
                  <span className={CONFIDENCE_LABEL(testResult.confidence).cls}>
                    {CONFIDENCE_LABEL(testResult.confidence).label} ({Math.round(testResult.confidence * 100)}%)
                  </span>
                </div>
                {testResult.escalation_taid && (
                  <div className="text-orange-400 text-xs font-mono">
                    Ticket: {testResult.escalation_taid}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Truth records summary */}
          <div className="bg-tt-card border border-tt-border rounded-lg p-5">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-white font-semibold text-sm">Truth records</h2>
              <span className="text-tt-blue text-xs font-mono">{records.length}</span>
            </div>
            {records.length === 0
              ? <p className="text-tt-muted text-xs">No records yet. Upload documents first.</p>
              : (
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {records.slice(0, 20).map((r) => (
                    <div key={r.record_id || r.taid} className="text-xs font-mono">
                      <span className="text-tt-blue mr-2">{r.record_type}</span>
                      <span className="text-tt-muted">{JSON.stringify(r.content).slice(0, 60)}…</span>
                    </div>
                  ))}
                  {records.length > 20 && <p className="text-tt-muted text-xs">+{records.length - 20} more</p>}
                </div>
              )}
          </div>
        </div>

        {/* Right: tabs */}
        <div className="lg:col-span-3">
          <div className="flex border-b border-tt-border mb-4">
            {['queries', 'escalations'].map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-5 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
                  tab === t ? 'border-tt-blue text-white' : 'border-transparent text-tt-muted hover:text-white'
                }`}
              >
                {t === 'queries' ? 'Recent queries' : `Escalations${openEscalations.length ? ` (${openEscalations.length})` : ''}`}
              </button>
            ))}
          </div>

          {tab === 'queries' && (
            <div className="space-y-2">
              {escalations.length === 0 && records.length === 0 ? (
                <p className="text-tt-muted text-sm text-center py-12">No queries yet. Test one on the left!</p>
              ) : (
                <p className="text-tt-muted text-xs text-center py-6">
                  Query history stored in <span className="font-mono">tt_invocations</span> collection.
                  Visible here once invocations are fetched (wire up <code className="font-mono">/api/tourtext/invocations</code> endpoint to display them).
                </p>
              )}
            </div>
          )}

          {tab === 'escalations' && (
            <div className="space-y-3">
              {escalations.length === 0 ? (
                <p className="text-tt-muted text-sm text-center py-12">No escalations.</p>
              ) : escalations.map((esc) => (
                <div key={esc.taid} className="bg-tt-card border border-tt-border rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <span className="text-white text-sm font-semibold">{esc.description}</span>
                    <span className={`text-xs font-mono ml-3 ${SEV_COLOR[esc.severity] || 'text-tt-muted'}`}>
                      {esc.severity}
                    </span>
                  </div>
                  <div className="text-tt-muted text-xs font-mono mb-3">{esc.original_query}</div>
                  <div className="flex items-center justify-between">
                    <span className={`text-xs font-mono ${esc.status === 'open' ? 'text-orange-400' : 'text-green-400'}`}>
                      {esc.status} · {esc.assigned_role}
                    </span>
                    {esc.status === 'open' && (
                      <button
                        onClick={() => handleResolve(esc.taid)}
                        className="text-xs text-tt-muted hover:text-white underline"
                      >
                        Resolve
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
