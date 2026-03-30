import React, { createContext, useContext, useEffect, useState } from 'react'
import { getMe } from './api'

const AuthCtx = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('tt_token')
    if (token) {
      getMe()
        .then(setUser)
        .catch(() => localStorage.removeItem('tt_token'))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  function saveAuth(token, userData) {
    localStorage.setItem('tt_token', token)
    setUser(userData)
  }

  function logout() {
    localStorage.removeItem('tt_token')
    setUser(null)
  }

  return (
    <AuthCtx.Provider value={{ user, loading, saveAuth, logout }}>
      {children}
    </AuthCtx.Provider>
  )
}

export const useAuth = () => useContext(AuthCtx)
