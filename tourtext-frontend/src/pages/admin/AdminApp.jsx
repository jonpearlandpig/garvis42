import React, { useState } from 'react'
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import { useAuth } from '../../AuthContext'
import TourSelect from './TourSelect'
import Upload from './Upload'
import LiveStatus from './LiveStatus'

export default function AdminApp() {
  const [currentTour, setCurrentTour] = useState(null)
  const { user, logout } = useAuth()
  const nav = useNavigate()

  function handleLogout() {
    logout()
    nav('/')
  }

  return (
    <div className="min-h-screen bg-tt-dark">
      {/* Top bar */}
      <header className="border-b border-tt-border px-6 py-4 flex items-center justify-between">
        <button onClick={() => nav('/admin')} className="text-tt-blue font-bold tracking-widest">TOURTEXT™</button>
        <div className="flex items-center gap-4">
          {currentTour && (
            <span className="text-tt-muted text-sm font-mono">
              {currentTour.name} <span className="text-tt-blue">[{currentTour.tour_code}]</span>
            </span>
          )}
          <span className="text-tt-muted text-sm">{user?.name}</span>
          <button onClick={handleLogout} className="text-tt-muted hover:text-white text-sm">Sign out</button>
        </div>
      </header>

      <Routes>
        <Route
          path="/"
          element={<TourSelect onTourSelected={(t) => { setCurrentTour(t); nav('/admin/upload') }} />}
        />
        <Route
          path="/upload"
          element={currentTour
            ? <Upload tour={currentTour} onNext={() => nav('/admin/live')} />
            : <Navigate to="/admin" replace />}
        />
        <Route
          path="/live"
          element={currentTour
            ? <LiveStatus tour={currentTour} />
            : <Navigate to="/admin" replace />}
        />
        <Route path="*" element={<Navigate to="/admin" replace />} />
      </Routes>
    </div>
  )
}
