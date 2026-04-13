import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Globe, AlertCircle } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const MapPage = () => {
  const [cities, setCities] = useState([])
  const [selectedCity, setSelectedCity] = useState(null)
  const [zones, setZones] = useState([])
  const [selectedZone, setSelectedZone] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch cities on mount
  useEffect(() => {
    const fetchCities = async () => {
      try {
        const response = await axios.get(`${API_URL}/cities`)
        setCities(response.data)
        if (response.data.length > 0) {
          setSelectedCity(response.data[0])
        }
        setLoading(false)
      } catch (err) {
        setError('Failed to load cities')
        setLoading(false)
      }
    }
    fetchCities()
  }, [])

  // Fetch zones when city changes
  useEffect(() => {
    if (selectedCity) {
      const fetchZones = async () => {
        try {
          const response = await axios.get(`${API_URL}/zones`, {
            params: { city_id: selectedCity.id }
          })
          setZones(response.data)
        } catch (err) {
          console.error('Failed to load zones:', err)
        }
      }
      fetchZones()
    }
  }, [selectedCity])

  const getRiskColor = (riskLevel) => {
    const colors = {
      'Green': 'bg-green-100 text-green-800 border-green-300',
      'Yellow': 'bg-yellow-100 text-yellow-800 border-yellow-300',
      'Red': 'bg-red-100 text-red-800 border-red-300',
    }
    return colors[riskLevel] || colors['Red']
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-4rem)]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading map data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-[calc(100vh-4rem)] bg-gray-50 dark:bg-gray-900">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          <AlertCircle className="inline mr-2" size={16} />
          {error}
        </div>
      )}

      <div className="h-full flex flex-col gap-4 p-4">
        {/* Top Controls */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
            <label className="block">
              <span className="text-sm font-bold">Select City:</span>
              <select
                value={selectedCity?.id || ''}
                onChange={(e) => {
                  const city = cities.find(c => c.id === parseInt(e.target.value))
                  setSelectedCity(city)
                }}
                className="mt-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              >
                {cities.map(city => (
                  <option key={city.id} value={city.id}>
                    {city.name} ({city.tier})
                  </option>
                ))}
              </select>
            </label>

            {selectedCity && (
              <div className="text-sm text-gray-600 dark:text-gray-300 sm:ml-auto">
                <Globe className="inline mr-2" size={16} />
                {selectedCity.zone_count} zones tracked
              </div>
            )}
          </div>
        </div>

        {/* Map Placeholder & Zones List */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Map Container */}
          <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <div className="w-full h-full flex items-center justify-center bg-gray-200 dark:bg-gray-700">
              <div className="text-center">
                <Globe size={48} className="mx-auto text-gray-400 mb-4" />
                <p className="text-gray-600 dark:text-gray-300">
                  📍 Interactive 3D Map will render here with Mapbox GL JS<br/>
                  <span className="text-sm">Add your Mapbox token to .env</span>
                </p>
              </div>
            </div>
          </div>

          {/* Zone Details Panel */}
          <div className="lg:col-span-1 bg-white dark:bg-gray-800 rounded-lg shadow overflow-auto flex flex-col">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="font-bold text-lg">Zones in {selectedCity?.name}</h3>
            </div>

            <div className="flex-1 overflow-auto p-4 space-y-3">
              {zones.length === 0 ? (
                <p className="text-gray-600 dark:text-gray-300 text-center py-8">
                  No zones found for this city
                </p>
              ) : (
                zones.map(zone => (
                  <div
                    key={zone.id}
                    onClick={() => setSelectedZone(zone)}
                    className={`p-3 rounded-lg border-2 cursor-pointer transition ${
                      selectedZone?.id === zone.id
                        ? 'border-blue-500 bg-blue-50 dark:bg-blue-900'
                        : getRiskColor(zone.risk_level)
                    }`}
                  >
                    <h4 className="font-bold text-sm">{zone.name}</h4>
                    <div className="grid grid-cols-2 gap-2 mt-2 text-xs">
                      <div>
                        <span className="font-semibold">Score:</span> {zone.score_value}
                      </div>
                      <div>
                        <span className="font-semibold">Risk:</span> {zone.risk_level}
                      </div>
                      <div className="col-span-2">
                        <span className="font-semibold">Proximity:</span> Metro {zone.metro_proximity}km
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Selected Zone Details */}
            {selectedZone && (
              <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-blue-50 dark:bg-blue-900/20">
                <h4 className="font-bold mb-3">Zone Details</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Growth Score:</span>
                    <span className="font-bold">{selectedZone.score_value}/100</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Risk Level:</span>
                    <span className={`px-2 py-1 rounded text-xs font-bold ${getRiskColor(selectedZone.risk_level)}`}>
                      {selectedZone.risk_level}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Metro Proximity:</span>
                    <span>{selectedZone.metro_proximity}km</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Highway Proximity:</span>
                    <span>{selectedZone.highway_proximity}km</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default MapPage
