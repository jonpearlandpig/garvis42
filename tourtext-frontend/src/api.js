import axios from 'axios'

const BASE = '/api/tourtext'

function authHeaders() {
  const token = localStorage.getItem('tt_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

// Auth
export const signup = (data) =>
  axios.post(`${BASE}/auth/signup`, data).then((r) => r.data)

export const login = (data) =>
  axios.post(`${BASE}/auth/login`, data).then((r) => r.data)

export const getMe = () =>
  axios.get(`${BASE}/auth/me`, { headers: authHeaders() }).then((r) => r.data)

// Tours
export const getTours = () =>
  axios.get(`${BASE}/tours`, { headers: authHeaders() }).then((r) => r.data)

export const createTour = (data) =>
  axios.post(`${BASE}/tours`, data, { headers: authHeaders() }).then((r) => r.data)

// Files
export const uploadFile = (tourId, formData) =>
  axios
    .post(`${BASE}/tours/${tourId}/upload`, formData, {
      headers: { ...authHeaders(), 'Content-Type': 'multipart/form-data' },
    })
    .then((r) => r.data)

export const getFiles = (tourId) =>
  axios.get(`${BASE}/tours/${tourId}/files`, { headers: authHeaders() }).then((r) => r.data)

export const reprocessFile = (fileId) =>
  axios.post(`${BASE}/files/${fileId}/reprocess`, {}, { headers: authHeaders() }).then((r) => r.data)

// Query
export const submitQuery = (data) =>
  axios.post(`${BASE}/query`, data, { headers: authHeaders() }).then((r) => r.data)

// Truth records
export const getTruthRecords = (tourId) =>
  axios.get(`${BASE}/tours/${tourId}/truth-records`, { headers: authHeaders() }).then((r) => r.data)

// Escalations
export const getEscalations = (tourId) =>
  axios.get(`${BASE}/tours/${tourId}/escalations`, { headers: authHeaders() }).then((r) => r.data)

export const resolveEscalation = (taid) =>
  axios.patch(`${BASE}/escalations/${taid}/resolve`, {}, { headers: authHeaders() }).then((r) => r.data)

// Integration status
export const getIntegrationStatus = () =>
  axios.get(`${BASE}/integrations/status`, { headers: authHeaders() }).then((r) => r.data)
