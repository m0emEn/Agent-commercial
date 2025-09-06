import React, { useState, useEffect } from 'react'
import Papa from 'papaparse'

const CSVLoader = () => {
  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchCSV = async () => {
      setLoading(true)
      try {
        const response = await fetch('/clients.csv') // CSV path in public folder
        const csvText = await response.text()
        const parsed = Papa.parse(csvText, { header: true, skipEmptyLines: true })
        setClients(parsed.data)
      } catch (err) {
        setError('Failed to load CSV')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchCSV()
  }, [])

  if (loading) return <p>Loading CSV data...</p>
  if (error) return <p className="text-red-500">{error}</p>

  return (
    <div>
      <h2 className="font-bold mb-2">Clients</h2>
      <ul>
        {clients.map((c, idx) => (
          <li key={idx}>{Object.values(c).join(' | ')}</li>
        ))}
      </ul>
    </div>
  )
}

export default CSVLoader
