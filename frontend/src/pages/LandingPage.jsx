import React from 'react'
import { Link } from 'react-router-dom'
import { MapPin, TrendingUp, Shield, Globe, ArrowRight, Check } from 'lucide-react'

const LandingPage = () => {
  const features = [
    {
      icon: <MapPin className="w-8 h-8 text-gray-600" />,
      title: "Advanced Zone Mapping",
      description: "Intelligent geospatial analysis to identify high-potential infrastructure zones"
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-gray-600" />,
      title: "Growth Analytics",
      description: "Data-driven scoring system for accurate growth potential assessment"
    },
    {
      icon: <Shield className="w-8 h-8 text-gray-600" />,
      title: "Risk Intelligence",
      description: "Comprehensive risk indicators for informed investment decisions"
    },
    {
      icon: <Globe className="w-8 h-8 text-gray-600" />,
      title: "Real-time Updates",
      description: "Live infrastructure event tracking across Indian markets"
    }
  ]

  const stats = [
    { number: "50+", label: "Cities Mapped" },
    { number: "100K+", label: "Infrastructure Events" },
    { number: "AI-Powered", label: "Analysis" },
    { number: "Real-time", label: "Updates" }
  ]

  return (
    <div className="min-h-screen bg-white text-gray-900 overflow-hidden">
      {/* Navigation */}
      <nav className="border-b border-gray-200 sticky top-0 z-50 bg-white/95 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="text-2xl font-light tracking-tight">
            Prop<span className="font-semibold">AI</span>
          </div>
          <div className="flex gap-6">
            <Link
              to="/map"
              className="text-sm text-gray-600 hover:text-gray-900 transition"
            >
              Platform
            </Link>
            <Link
              to="/map"
              className="text-sm px-5 py-2 rounded-lg bg-gray-900 text-white hover:bg-gray-800 transition"
            >
              Launch App →
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div className="space-y-8">
            <h1 className="text-6xl md:text-7xl font-light leading-tight tracking-tight">
              Infrastructure Intelligence
              <span className="block font-semibold text-gray-600">for Real Estate</span>
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed max-w-lg">
              Discover high-growth infrastructure zones with AI-powered geospatial analysis. Make data-driven real estate investment decisions.
            </p>
            <div className="flex gap-4 pt-4">
              <Link
                to="/map"
                className="px-8 py-3 rounded-lg bg-gray-900 text-white hover:bg-gray-800 transition font-medium flex items-center gap-2"
              >
                Explore Platform <ArrowRight size={18} />
              </Link>
              <Link
                to="/map"
                className="px-8 py-3 rounded-lg border border-gray-300 hover:border-gray-400 transition font-medium"
              >
                View Demo
              </Link>
            </div>
          </div>

          {/* Hero Visual */}
          <div className="relative">
            <div className="aspect-square rounded-2xl overflow-hidden border border-gray-200 bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center text-8xl">
              🗺️
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 border-y border-gray-200">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, idx) => (
              <div key={idx} className="text-center">
                <div className="text-4xl font-light mb-2">
                  {stat.number}
                </div>
                <p className="text-sm text-gray-600">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-light mb-4 tracking-tight">
            Powerful Features
          </h2>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Everything you need for intelligent real estate decision-making
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          {features.map((feature, idx) => (
            <div
              key={idx}
              className="group"
            >
              <div className="mb-4">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-t border-gray-200">
        <h2 className="text-5xl font-light text-center mb-16 tracking-tight">
          How it Works
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          {[
            { step: 1, title: "Data Collection", desc: "Real-time scraping from 50+ infrastructure news sources" },
            { step: 2, title: "NLP Processing", desc: "Entity extraction and event classification" },
            { step: 3, title: "Geospatial Analysis", desc: "Zone generation using PostGIS mapping" },
            { step: 4, title: "Risk Scoring", desc: "Growth potential assessment algorithm" }
          ].map((item, idx) => (
            <div key={idx} className="relative">
              <div className="border border-gray-200 rounded-lg p-6 text-center">
                <div className="text-3xl font-light text-gray-400 mb-3">{item.step}</div>
                <h4 className="font-semibold mb-2 text-sm">{item.title}</h4>
                <p className="text-xs text-gray-600">{item.desc}</p>
              </div>
              {idx < 3 && (
                <div className="hidden md:block absolute top-1/2 -right-3 transform -translate-y-1/2">
                  <ArrowRight className="text-gray-300" size={20} />
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-5xl font-light mb-6 tracking-tight">
            Ready to explore?
          </h2>
          <p className="text-xl text-gray-600 mb-10">
            Start analyzing infrastructure zones in your target markets today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/map"
              className="px-8 py-3 rounded-lg bg-gray-900 text-white hover:bg-gray-800 transition font-medium"
            >
              Launch Platform →
            </Link>
            <Link
              to="/map"
              className="px-8 py-3 rounded-lg border border-gray-300 hover:border-gray-400 transition font-medium"
            >
              View Live Data
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-semibold mb-4">PropAI</h3>
              <p className="text-sm text-gray-600">Infrastructure intelligence for Indian real estate</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Platform</h4>
              <div className="space-y-2 text-sm">
                <p><Link to="/map" className="text-gray-600 hover:text-gray-900 transition">Map</Link></p>
                <p><Link to="/map" className="text-gray-600 hover:text-gray-900 transition">Events</Link></p>
                <p><Link to="/map" className="text-gray-600 hover:text-gray-900 transition">Insights</Link></p>
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Resources</h4>
              <div className="space-y-2 text-sm">
                <p><a href="#" className="text-gray-600 hover:text-gray-900 transition">Documentation</a></p>
                <p><a href="#" className="text-gray-600 hover:text-gray-900 transition">Blog</a></p>
                <p><a href="#" className="text-gray-600 hover:text-gray-900 transition">FAQ</a></p>
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <div className="space-y-2 text-sm">
                <p><a href="#" className="text-gray-600 hover:text-gray-900 transition">About</a></p>
                <p><a href="#" className="text-gray-600 hover:text-gray-900 transition">Contact</a></p>
                <p><a href="#" className="text-gray-600 hover:text-gray-900 transition">Privacy</a></p>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-200 pt-8 flex justify-between items-center text-sm text-gray-600">
            <p>&copy; 2025 PropAI. All rights reserved.</p>
            <div className="flex gap-6">
              <a href="#" className="hover:text-gray-900 transition">Twitter</a>
              <a href="#" className="hover:text-gray-900 transition">LinkedIn</a>
              <a href="#" className="hover:text-gray-900 transition">GitHub</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage
