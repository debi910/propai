import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { AlertCircle, ExternalLink } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const EventsPage = () => {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [page, setPage] = useState(0)
  const [totalEvents, setTotalEvents] = useState(0)
  const pageSize = 20

  const fetchEvents = async (pageNum) => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/events`, {
        params: {
          skip: pageNum * pageSize,
          limit: pageSize
        }
      })
      setEvents(response.data.events)
      setTotalEvents(response.data.total)
      setError(null)
    } catch (err) {
      setError('Failed to load events')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEvents(page)
  }, [page])

  const eventTypeColors = {
    'Highway': 'bg-blue-100 text-blue-800',
    'Metro': 'bg-purple-100 text-purple-800',
    'Airport': 'bg-green-100 text-green-800',
    'Factory': 'bg-yellow-100 text-yellow-800',
    'Government_Regulation': 'bg-red-100 text-red-800',
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-4xl font-bold mb-8">Infrastructure Events</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 flex gap-2">
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <>
          {/* Events List */}
          <div className="space-y-4 mb-8">
            {events.length === 0 ? (
              <p className="text-gray-600 dark:text-gray-300 text-center py-8">
                No events found
              </p>
            ) : (
              events.map(event => (
                <div
                  key={event.id}
                  className="bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition p-6 border-l-4 border-blue-500"
                >
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold mb-2">{event.title}</h3>
                      <p className="text-gray-600 dark:text-gray-300 text-sm mb-3">
                        {event.description}
                      </p>
                      <div className="flex flex-wrap gap-2 items-center text-xs">
                        <span className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">
                          📰 {event.source_name}
                        </span>
                        <span className="text-gray-500 dark:text-gray-400">
                          {new Date(event.event_date).toLocaleDateString()}
                        </span>
                        {event.source_url && (
                          <a
                            href={event.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 dark:text-blue-400 flex items-center gap-1"
                          >
                            Read More <ExternalLink size={12} />
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Pagination */}
          {totalEvents > 0 && (
            <div className="flex justify-center items-center gap-4">
              <button
                onClick={() => setPage(Math.max(0, page - 1))}
                disabled={page === 0}
                className="px-4 py-2 bg-blue-600 text-white rounded disabled:bg-gray-400 disabled:cursor-not-allowed hover:bg-blue-700 transition"
              >
                ← Previous
              </button>
              <span className="text-sm text-gray-600 dark:text-gray-300">
                Page {page + 1} of {Math.ceil(totalEvents / pageSize)} ({totalEvents} events)
              </span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={(page + 1) * pageSize >= totalEvents}
                className="px-4 py-2 bg-blue-600 text-white rounded disabled:bg-gray-400 disabled:cursor-not-allowed hover:bg-blue-700 transition"
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default EventsPage
