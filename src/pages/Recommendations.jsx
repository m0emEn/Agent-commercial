import React, { useState, useEffect, useRef } from 'react'
import { Brain, Search } from 'lucide-react'
import Client from '../components/Client'
import Papa from 'papaparse'

const Recommendations = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const clientsPerPage = 10
  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const componentRef = useRef(null) // Create a ref for the component's root element

  // Load CSV from public folder
  useEffect(() => {
    const fetchCSV = async () => {
      setLoading(true)
      try {
        const response = await fetch('frontend_data.csv')
        const csvText = await response.text()
        const parsed = Papa.parse(csvText, { header: true, skipEmptyLines: true })
        
        const data = parsed.data.map((row, idx) => {
          // Convert REF_PERSONNE to number
          const clientId = parseInt(row.REF_PERSONNE, 10)
          
          // Convert stringified array in POLICE column to real array
          let LIB_PRODUIT = []
          if (row.LIB_PRODUIT) {
            try {
              LIB_PRODUIT = JSON.parse(row.LIB_PRODUIT.replace(/'/g, '"'))
              LIB_PRODUIT = LIB_PRODUIT.map(p =>
                p
                  .toLowerCase() // first make lowercase
                  .replace(/\b\w/g, char => char.toUpperCase()) // then capitalize first letter of each word
              )
            } catch {
              LIB_PRODUIT = [] // fallback in case parsing fails
            }
          }
  
          return {
            ...row,
            clientId,
            id: idx + 1,
            LIB_PRODUIT: LIB_PRODUIT
          }
        })
  
        setClients(data)
      } catch (err) {
        setError('Failed to load CSV')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchCSV()
  }, [])
  
  const filteredClients = clients.filter(c => {
    if (!searchTerm) return true
    const searchId = parseInt(searchTerm, 10)
    return !isNaN(searchId) && c.clientId === searchId
  })

  // Pagination logic
  const totalPages = Math.ceil(filteredClients.length / clientsPerPage)
  const startIdx = (currentPage - 1) * clientsPerPage
  const endIdx = Math.min(startIdx + clientsPerPage, filteredClients.length)
  const paginatedClients = filteredClients.slice(startIdx, endIdx)

  const handlePageChange = page => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page)
      if (componentRef.current) {
        componentRef.current.scrollIntoView({ behavior: 'smooth' }) 
      }
    }
  }

  if (loading) return (
    <div className="flex flex-col items-center justify-center h-64">
      <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p className="mt-4 text-blue-500 text-lg font-medium">Fetching data...</p>
    </div>
  )  
  if (error) return <p className="text-red-500">{error}</p>

  return (
    <div ref={componentRef} className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Recommendations</h1>
          <p className="text-gray-600 mt-1">Personalized insurance product suggestions powered by AI</p>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search by client ID..."
            value={searchTerm}
            onChange={e => {
              setSearchTerm(e.target.value)
              setCurrentPage(1) // reset to first page on search
            }}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Client List */}
      <div className="space-y-4">
        <div className="text-sm text-gray-600 mb-2">
          {filteredClients.length === 0
            ? 'No clients to show'
            : `Showing ${startIdx + 1}-${endIdx} of ${filteredClients.length} clients`}
        </div>

        {paginatedClients.map(rec => (
          <Client rec={rec} key={rec.clientId} />
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center space-x-2 mt-4">
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className={`px-3 py-1 rounded ${
              currentPage === 1
                ? 'bg-gray-200 text-gray-400'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Previous
          </button>

          {/* Show max 10 page buttons */}
          {Array.from({ length: totalPages }, (_, idx) => idx + 1)
            .slice(
              Math.max(0, currentPage - 5), // start 5 pages before current
              Math.min(totalPages, currentPage + 5) // end 5 pages after current
            )
            .map((page) => (
              <button
                key={page}
                onClick={() => handlePageChange(page)}
                className={`px-3 py-1 rounded ${
                  currentPage === page
                    ? 'bg-blue-500 text-white'
                    : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
                }`}
              >
                {page}
              </button>
            ))}

          <button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className={`px-3 py-1 rounded ${
              currentPage === totalPages
                ? 'bg-gray-200 text-gray-400'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Next
          </button>
        </div>
      )}

      {/* Empty State */}
      {filteredClients.length === 0 && (
        <div className="text-center py-12">
          <Brain className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No recommendations found</h3>
          <p className="text-gray-500 mb-4">
            {searchTerm
              ? 'Try adjusting your search or filter criteria.'
              : 'Generate new AI recommendations to get started.'}
          </p>
          <button
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-lg text-sm font-medium text-white hover:opacity-90"
            style={{ backgroundColor: '#DF2C27' }}
          >
            <Brain className="w-4 h-4 mr-2" />
            Generate Recommendations
          </button>
        </div>
      )}
    </div>
  )
}

export default Recommendations