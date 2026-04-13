import React from 'react'

const Footer = () => {
  return (
    <footer className="bg-gray-100 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-lg font-bold mb-4">PropAI</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              AI-Powered Real Estate Intelligence Platform for India
            </p>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
              <li><a href="/map" className="hover:text-blue-600">Explore Map</a></li>
              <li><a href="/events" className="hover:text-blue-600">View Events</a></li>
              <li><a href="/insights" className="hover:text-blue-600">City Insights</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">About</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Built with open-source technologies. Free and transparent real estate analysis.
            </p>
          </div>
        </div>

        {/* Legal Disclaimer */}
        <div className="border-t border-gray-300 dark:border-gray-600 pt-6 mt-6">
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
            ⚠️ Legal Disclaimer: This platform provides AI-based insights for informational purposes only.
            It does not guarantee returns, predict actual property values, or constitute investment advice.
            Always consult with qualified real estate professionals before making investment decisions.
          </p>
        </div>

        <div className="text-center mt-6 text-xs text-gray-500 dark:text-gray-400">
          <p>&copy; 2026 PropAI. All rights reserved. Open Source Project.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
