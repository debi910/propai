import React from 'react'
import { Link } from 'react-router-dom'
import { Map, TrendingUp, AlertCircle } from 'lucide-react'

const Home = () => {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 min-h-[calc(100vh-16rem)]">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
          🏘️ Real Estate Intelligence for India
        </h1>
        <p className="text-xl md:text-2xl text-gray-700 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
          Discover emerging growth zones powered by AI analysis of infrastructure news, government announcements, and development signals
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/map"
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-bold transition flex items-center justify-center gap-2"
          >
            <Map size={20} />
            Explore Interactive Map
          </Link>
          <Link
            to="/events"
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 rounded-lg font-bold transition flex items-center justify-center gap-2"
          >
            <TrendingUp size={20} />
            Latest Events
          </Link>
        </div>
      </section>

      {/* Stats Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-700 rounded-lg p-6 shadow">
            <div className="text-4xl font-bold text-green-600 mb-2">15+</div>
            <div className="text-gray-600 dark:text-gray-300">Growth Zones Tracked</div>
          </div>
          <div className="bg-white dark:bg-gray-700 rounded-lg p-6 shadow">
            <div className="text-4xl font-bold text-blue-600 mb-2">3</div>
            <div className="text-gray-600 dark:text-gray-300">Major Cities Covered</div>
          </div>
          <div className="bg-white dark:bg-gray-700 rounded-lg p-6 shadow">
            <div className="text-4xl font-bold text-purple-600 mb-2">100+</div>
            <div className="text-gray-600 dark:text-gray-300">Infrastructure Events</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 className="text-3xl font-bold mb-12 text-center">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white dark:bg-gray-700 rounded-lg p-6 shadow">
            <h3 className="text-xl font-bold mb-3">🗺️ 3D Interactive Map</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Visualize growth zones with 3D buildings and terrain. Color-coded risk levels: Green (high growth), Yellow (medium), Red (low).
            </p>
          </div>
          <div className="bg-white dark:bg-gray-700 rounded-lg p-6 shadow">
            <h3 className="text-xl font-bold mb-3">📰 Real-time News Feed</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Track infrastructure announcements, metro expansions, airport projects, and government regulations instantly.
            </p>
          </div>
          <div className="bg-white dark:bg-gray-700 rounded-lg p-6 shadow">
            <h3 className="text-xl font-bold mb-3">🤖 AI-Powered Analysis</h3>
            <p className="text-gray-600 dark:text-gray-300">
              NLP-based extraction of locations, event types, and status. Rule-based scoring for growth potential.
            </p>
          </div>
          <div className="bg-white dark:bg-gray-700 rounded-lg p-6 shadow">
            <h3 className="text-xl font-bold mb-3">📊 City Insights</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Detailed analysis per city with zone distribution, average scores, and top opportunities.
            </p>
          </div>
        </div>
      </section>

      {/* Legal Notice */}
      <section className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 rounded mt-12 max-w-7xl mx-auto mx-4 mb-12">
        <div className="flex gap-4 p-6">
          <AlertCircle className="text-yellow-700 dark:text-yellow-400 mt-1 flex-shrink-0" size={20} />
          <div>
            <h3 className="font-bold text-yellow-800 dark:text-yellow-200 mb-2">Important Disclaimer</h3>
            <p className="text-sm text-yellow-700 dark:text-yellow-300">
              This platform provides AI-based insights for informational purposes only. It does not guarantee property returns,
              predict market values, or constitute investment advice. Real estate investments involve risks. Always conduct thorough
              due diligence and consult with qualified professionals before making any investment decisions.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
