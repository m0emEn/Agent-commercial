import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Recommendations from './pages/Recommendations'
import './index.css'

function App() {
  return (
    <Router
    future={{
      v7_startTransition: true,
      v7_relativeSplatPath: true,

    }}
    >
      <div className="min-h-screen bg-gray-50">
          <Layout>
            <Routes>
              <Route path="/" element={<Recommendations />} />

            </Routes>
          </Layout>
        <Toaster position="top-right" />
      </div>
    </Router>
  )
}

export default App