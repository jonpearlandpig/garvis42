import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function PublicSite() {
  const nav = useNavigate()
  return (
    <div className="min-h-screen bg-tt-dark text-slate-100">
      {/* Nav */}
      <nav className="border-b border-tt-border px-6 py-4 flex items-center justify-between">
        <span className="text-tt-blue font-bold tracking-widest text-lg">TOURTEXT™</span>
        <div className="flex gap-3">
          <button onClick={() => nav('/login')} className="text-tt-muted hover:text-white text-sm px-4 py-2">Sign in</button>
          <button onClick={() => nav('/signup')} className="bg-tt-blue text-white text-sm px-4 py-2 rounded hover:bg-blue-500">Get started</button>
        </div>
      </nav>

      {/* Hero */}
      <div className="max-w-4xl mx-auto px-6 py-20 text-center">
        <div className="inline-block bg-blue-900/30 border border-blue-500/40 text-blue-400 text-xs px-3 py-1 rounded-full mb-6 tracking-widest">
          v4.1 — INFRASTRUCTURE-GRADE TOUR INFORMATION
        </div>
        <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
          Tour information.<br />
          <span className="text-tt-blue">Instantly usable under pressure.</span>
        </h1>
        <p className="text-tt-muted text-lg mb-10 max-w-2xl mx-auto">
          Crew texts a question to <span className="text-white font-mono">888-340-0564</span>. TourText returns a verified answer in seconds — from documents you already have.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button onClick={() => nav('/signup')} className="bg-tt-blue hover:bg-blue-500 text-white font-semibold px-8 py-4 rounded-lg text-lg">
            Start your tour →
          </button>
          <button onClick={() => nav('/login')} className="border border-tt-border hover:border-slate-400 text-tt-muted hover:text-white px-8 py-4 rounded-lg text-lg">
            Sign in
          </button>
        </div>
      </div>

      {/* 3-step activation */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        <h2 className="text-center text-tt-muted text-sm tracking-widest uppercase mb-10">60-second activation</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { n: '01', title: 'Export', body: 'Export from Master Tour, Eventbrite, or your routing sheet. CSV, XLSX, or PDF.' },
            { n: '02', title: 'Upload', body: 'Drag and drop into your TourText dashboard. Processing starts immediately.' },
            { n: '03', title: 'Text', body: `Crew texts 888-340-0564 with your tour code. Verified answers, instantly.` },
          ].map(({ n, title, body }) => (
            <div key={n} className="bg-tt-card border border-tt-border rounded-lg p-6">
              <div className="text-tt-blue font-mono text-sm mb-3">{n}</div>
              <div className="font-semibold text-white mb-2">{title}</div>
              <div className="text-tt-muted text-sm">{body}</div>
            </div>
          ))}
        </div>
      </div>

      {/* What it is not */}
      <div className="max-w-4xl mx-auto px-6 py-12 border-t border-tt-border">
        <div className="bg-tt-card border border-tt-border rounded-lg p-8 text-center">
          <div className="text-slate-400 text-sm mb-2">NOT A CHATBOT</div>
          <p className="text-white text-lg">TourText <strong>retrieves verified information</strong>, not guesses. It activates your existing systems — it does not replace them.</p>
        </div>
      </div>

      {/* Use cases */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        <h2 className="text-center text-tt-muted text-sm tracking-widest uppercase mb-10">Real-world queries</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { time: '2:47 AM', q: '"Where is the loading dock?"', a: 'Stage Door, 14th St side. Code 4477. — answered in 3s' },
            { time: 'Day-of-show', q: '"ADA entrance for VIP guests?"', a: 'East gate, elevator to suite level 3. Capacity 12.' },
            { time: 'After show', q: '"Settlement terms for tonight?"', a: 'Finance queries escalated to Tour Manager per guardrail.' },
          ].map(({ time, q, a }) => (
            <div key={time} className="bg-tt-card border border-tt-border rounded-lg p-6">
              <div className="text-tt-muted text-xs font-mono mb-3">{time}</div>
              <div className="text-slate-300 text-sm mb-3 italic">{q}</div>
              <div className="text-green-400 text-sm font-mono">{a}</div>
            </div>
          ))}
        </div>
      </div>

      <footer className="border-t border-tt-border px-6 py-8 text-center text-tt-muted text-xs">
        TourText™ v4.1 — Infrastructure-grade tour information system
      </footer>
    </div>
  )
}
