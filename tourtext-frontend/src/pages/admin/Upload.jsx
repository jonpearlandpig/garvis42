import React, { useCallback, useEffect, useState } from 'react'
import { uploadFile, getFiles, reprocessFile } from '../../api'

const FILE_TYPES = {
  mastertour: 'Master Tour Export',
  eventbrite: 'Eventbrite',
  routing: 'Routing Sheet',
  onesheet: 'One Sheet / PDF',
  settlement: 'Settlement Record',
  techpack: 'Tech Pack',
  other: 'Other',
}

function detectFileType(filename) {
  const f = filename.toLowerCase()
  if (f.includes('master') || f.includes('mastertour')) return 'mastertour'
  if (f.includes('eventbrite')) return 'eventbrite'
  if (f.includes('routing') || f.includes('route')) return 'routing'
  if (f.includes('settlement')) return 'settlement'
  if (f.includes('tech') || f.includes('pack')) return 'techpack'
  return 'other'
}

const STATUS_COLOR = {
  completed: 'text-green-400',
  processing: 'text-yellow-400',
  pending: 'text-tt-muted',
  failed: 'text-red-400',
  duplicate: 'text-slate-500',
}

export default function Upload({ tour, onNext }) {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    getFiles(tour.tour_id).then(setFiles).catch(() => {})
    const interval = setInterval(() => {
      getFiles(tour.tour_id).then(setFiles).catch(() => {})
    }, 5000)
    return () => clearInterval(interval)
  }, [tour.tour_id])

  async function handleFiles(fileList) {
    setError('')
    setUploading(true)
    for (const file of Array.from(fileList)) {
      try {
        const fd = new FormData()
        fd.append('file', file)
        fd.append('file_type', detectFileType(file.name))
        const result = await uploadFile(tour.tour_id, fd)
        setFiles((prev) => {
          const existing = prev.find((f) => f.file_id === result.file_id)
          if (existing) return prev
          return [...prev, { file_id: result.file_id, filename: file.name, processing_status: result.status, record_count: 0 }]
        })
      } catch (err) {
        setError(`Upload failed for ${file.name}: ${err.response?.data?.detail || err.message}`)
      }
    }
    setUploading(false)
  }

  const onDrop = useCallback((e) => {
    e.preventDefault()
    setDragOver(false)
    handleFiles(e.dataTransfer.files)
  }, [tour.tour_id])

  async function handleReprocess(fileId) {
    try {
      await reprocessFile(fileId)
      setFiles((prev) => prev.map((f) => f.file_id === fileId ? { ...f, processing_status: 'pending' } : f))
    } catch (err) {
      setError('Reprocess failed.')
    }
  }

  const readyCount = files.filter((f) => f.processing_status === 'completed').length

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-1">
          <span className="text-tt-blue font-mono text-sm">{tour.tour_code}</span>
          <span className="text-tt-muted text-sm">›</span>
          <span className="text-white font-semibold">{tour.name}</span>
        </div>
        <h1 className="text-2xl font-bold text-white">Upload tour documents</h1>
        <p className="text-tt-muted text-sm mt-1">
          CSV, XLSX, or PDF. Master Tour exports and Eventbrite downloads work best.
        </p>
      </div>

      {error && (
        <div className="bg-red-900/30 border border-red-500/50 text-red-400 text-sm px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors mb-6 ${
          dragOver ? 'border-tt-blue bg-blue-900/10' : 'border-tt-border hover:border-slate-500'
        }`}
      >
        <div className="text-4xl mb-4">📂</div>
        <p className="text-white font-semibold mb-2">
          {uploading ? 'Uploading…' : 'Drop files here'}
        </p>
        <p className="text-tt-muted text-sm mb-4">CSV, XLSX, PDF — or</p>
        <label className="cursor-pointer bg-tt-card border border-tt-border hover:border-slate-400 text-white text-sm px-5 py-2.5 rounded-lg">
          Browse files
          <input
            type="file"
            multiple
            accept=".csv,.xlsx,.xls,.pdf"
            className="hidden"
            onChange={(e) => handleFiles(e.target.files)}
          />
        </label>
      </div>

      {/* File list */}
      {files.length > 0 && (
        <div className="bg-tt-card border border-tt-border rounded-lg overflow-hidden mb-8">
          <div className="px-5 py-3 border-b border-tt-border flex items-center justify-between">
            <span className="text-white text-sm font-semibold">Uploaded files</span>
            <span className="text-tt-muted text-xs">{readyCount}/{files.length} ready</span>
          </div>
          {files.map((f) => (
            <div key={f.file_id} className="px-5 py-4 border-b border-tt-border last:border-0 flex items-center justify-between">
              <div>
                <div className="text-white text-sm">{f.filename}</div>
                <div className="text-tt-muted text-xs font-mono mt-0.5">
                  {FILE_TYPES[f.file_type] || f.file_type} •{' '}
                  {f.record_count > 0 ? `${f.record_count} records extracted` : 'processing…'}
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span className={`text-xs font-mono capitalize ${STATUS_COLOR[f.processing_status] || 'text-tt-muted'}`}>
                  {f.processing_status}
                </span>
                {f.processing_status === 'failed' && (
                  <button
                    onClick={() => handleReprocess(f.file_id)}
                    className="text-tt-muted hover:text-white text-xs underline"
                  >
                    Retry
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Recommended sources */}
      <div className="bg-tt-card border border-tt-border rounded-lg p-5 mb-8">
        <div className="text-tt-muted text-xs tracking-widest uppercase mb-3">Recommended sources</div>
        <ul className="text-sm text-slate-300 space-y-1.5">
          <li>• <strong>Master Tour</strong> — Export as CSV from Shows view</li>
          <li>• <strong>Eventbrite</strong> — Download attendee/event report as CSV</li>
          <li>• <strong>Routing sheet</strong> — XLSX with stop #, city, venue, date</li>
          <li>• <strong>Venue PDFs</strong> — Tech packs, load-in sheets</li>
        </ul>
      </div>

      {/* Next */}
      <div className="flex items-center justify-between">
        <p className="text-tt-muted text-sm">
          Crew texts <span className="text-white font-mono">888-340-0564</span> with your tour code{' '}
          <span className="text-tt-blue font-mono">{tour.tour_code}</span> to query this tour.
        </p>
        <button
          onClick={onNext}
          disabled={readyCount === 0}
          className="bg-tt-blue hover:bg-blue-500 disabled:opacity-40 text-white text-sm font-semibold px-6 py-2.5 rounded-lg"
        >
          Live dashboard →
        </button>
      </div>
    </div>
  )
}
