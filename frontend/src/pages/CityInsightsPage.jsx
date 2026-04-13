import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { AlertCircle, BarChart3 } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const CityInsightsPage = () => {
  const [cities, setCities] = useState([])
  const [selectedCity, setSelectedCity] = useState(null)
  const [insights, setInsights] = useState(null)
  const [zones, setZones] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

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

  useEffect(() => {
    if (selectedCity) {
      const fetchInsights = async () => {
        try {
          const [insightRes, zonesRes] = await Promise.all([
            axios.get(`${API_URL}/cities/${selectedCity.name}`),
            axios.get(`${API_URL}/zones`, { params: { city_id: selectedCity.id } })
          ])
          setInsights(insightRes.data)
          const sortedZones = zonesRes.data.sort((a, b) => b.score_value - a.score_value)
          setZones(sortedZones)
        } catch (err) {
          setError('Failed to load insights')
          console.error(err)
        }
      }
      fetchInsights()
    }
  }, [selectedCity])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-4rem)]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading city insights...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-4xl font-bold mb-8">City Insights</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 flex gap-2">
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      {/* City Selector */}
      <div className="mb-8">
        <label className="block mb-2">
          <span className="font-bold">Select City:</span>
          <select
            value={selectedCity?.id || ''}
            onChange={(e) => {
              const city = cities.find(c => c.id === parseInt(e.target.value))
              setSelectedCity(city)
            }}
            className="mt-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 w-full sm:w-64"
          >
            {cities.map(city => (
              <option key={city.id} value={city.id}>
                {city.name}
              </option>
            ))}
          </select>
        </label>
      </div>

      {insights && (
        <>
          {/* City Header & Stats */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8 mb-8">
            <div>
              <h2 className="text-3xl font-bold mb-2">{insights.name}</h2>
              <p className="text-gray-600 dark:text-gray-300 mb-6">
                {insights.state} • {insights.tier}
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                <div className="text-3xl font-bold text-green-600">{insights.green_zones}</div>
                <div className="text-sm text-gray-600 dark:text-gray-300">🟢 High Growth Zones</div>
              </div>
              <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
                <div className="text-3xl font-bold text-yellow-600">{insights.yellow_zones}</div>
                <div className="text-sm text-gray-600 dark:text-gray-300">🟡 Medium Growth Zones</div>
              </div>
              <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
                <div className="text-3xl font-bold text-red-600">{insights.red_zones}</div>
                <div className="text-sm text-gray-600 dark:text-gray-300">🔴 Low Growth Zones</div>
              </div>
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <div className="text-3xl font-bold text-blue-600">{insights.zone_count}</div>
                <div className="text-sm text-gray-600 dark:text-gray-300">Total Zones</div>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                <div className="text-3xl font-bold text-purple-600">{insights.average_score.toFixed(1)}</div>
                <div className="text-sm text-gray-600 dark:text-gray-300">Avg Growth Score</div>
              </div>
            </div>
          </div>

          {/* Zone Distribution Chart (Simple Bar Chart) */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8 mb-8">
            <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <BarChart3 size={24} />
              Zone Distribution by Risk Level
            </h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span>🟢 High Growth (Green)</span>
                  <span className="font-bold">{insights.green_zones} zones</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                  <div
                    className="bg-green-500 h-full"
                    style={{ width: `${(insights.green_zones / Math.max(insights.zone_count, 1)) * 100}%` }}
                  ></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span>🟡 Medium Growth (Yellow)</span>
                  <span className="font-bold">{insights.yellow_zones} zones</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                  <div
                    className="bg-yellow-500 h-full"
                    style={{ width: `${(insights.yellow_zones / Math.max(insights.zone_count, 1)) * 100}%` }}
                  ></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span>🔴 Low Growth (Red)</span>
                  <span className="font-bold">{insights.red_zones} zones</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                  <div
                    className="bg-red-500 h-full"
                    style={{ width: `${(insights.red_zones / Math.max(insights.zone_count, 1)) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Top Growth Opportunities */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
            <h3 className="text-2xl font-bold mb-6">Top Growth Opportunities</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b border-gray-200 dark:border-gray-700">
                  <tr className="text-left text-sm">
                    <th className="pb-3 font-bold">Zone Name</th>
                    <th className="pb-3 font-bold">Growth Score</th>
                    <th className="pb-3 font-bold">Risk Level</th>
                    <th className="pb-3 font-bold">Time Horizon</th>
                  </tr>
                </thead>
                <tbody>
                  {zones.slice(0, 10).map(zone => {
                    const riskColors = {
                      'Green': 'bg-green-100 text-green-800',
                      'Yellow': 'bg-yellow-100 text-yellow-800',
                      'Red': 'bg-red-100 text-red-800',
                    }
                    return (
                      <tr key={zone.id} className="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50">
                        <td className="py-3">{zone.name}</td>
                        <td className="py-3">
                          <span className="font-bold text-lg">{zone.score_value}</span>/100
                        </td>
                        <td className="py-3">
                          <span className={`px-3 py-1 rounded-full text-xs font-bold ${riskColors[zone.risk_level]}`}>
                            {zone.risk_level}
                          </span>
                        </td>
                        <td className="py-3">{zone.metro_proximity}km to Metro</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default CityInsightsPage
