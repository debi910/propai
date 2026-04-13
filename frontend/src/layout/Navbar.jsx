import React from 'react'
import { Link } from 'react-router-dom'
import { Menu, X, Moon, Sun } from 'lucide-react'

const Navbar = ({ darkMode, toggleDarkMode }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false)

  return (
    <nav className="bg-white dark:bg-gray-800 shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              📍 PropAI
            </div>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/map" className="hover:text-blue-600 dark:hover:text-blue-400 transition">
              Map
            </Link>
            <Link to="/events" className="hover:text-blue-600 dark:hover:text-blue-400 transition">
              Events
            </Link>
            <Link to="/insights" className="hover:text-blue-600 dark:hover:text-blue-400 transition">
              Insights
            </Link>
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition"
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center space-x-4">
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700"
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700"
            >
              {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <Link to="/map" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
              Map
            </Link>
            <Link to="/events" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
              Events
            </Link>
            <Link to="/insights" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
              Insights
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
