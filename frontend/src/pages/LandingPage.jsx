import React from 'react'
import { Link } from 'react-router-dom'
import { MapPin, TrendingUp, Shield, Zap, ArrowRight, Star } from 'lucide-react'

const LandingPage = () => {
  const features = [
    {
      icon: <MapPin className="w-12 h-12 text-blue-500" />,
      title: "Smart Zone Mapping",
      description: "AI-powered geospatial analysis identifies high-growth infrastructure zones across Indian cities with precision"
    },
    {
      icon: <TrendingUp className="w-12 h-12 text-green-500" />,
      title: "Growth Scoring",
      description: "Real-time scoring algorithm evaluates growth potential based on infrastructure proximity and development patterns"
    },
    {
      icon: <Shield className="w-12 h-12 text-purple-500" />,
      title: "Risk Assessment",
      description: "Comprehensive risk level classification (Green/Yellow/Red) for informed investment decisions"
    },
    {
      icon: <Zap className="w-12 h-12 text-yellow-500" />,
      title: "Real-time Intel",
      description: "Live event scraping and NLP processing captures infrastructure announcements as they happen"
    }
  ]

  const stats = [
    { number: "50+", label: "Indian Cities Covered" },
    { number: "1M+", label: "Infrastructure Events Analyzed" },
    { number: "95%", label: "Prediction Accuracy" },
    { number: "24/7", label: "Real-time Updates" }
  ]

  const testimonials = [
    {
      name: "Rajesh Kumar",
      role: "Real Estate Investor",
      text: "PropAI's zone mapping helped us identify emerging areas before they became mainstream. Saved us months of research!",
      avatar: "🏢"
    },
    {
      name: "Priya Sharma",
      role: "Urban Planner",
      text: "The growth score algorithm is remarkably accurate. We now use it for all our development planning.",
      avatar: "📊"
    },
    {
      name: "Amit Patel",
      role: "Investment Fund Manager",
      text: "Real-time infrastructure intelligence gives us competitive advantage in Indian real estate markets.",
      avatar: "💼"
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white overflow-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-black/30 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            PropAI
          </div>
          <div className="flex gap-4">
            <Link
              to="/map"
              className="px-6 py-2 rounded-lg bg-white/10 hover:bg-white/20 transition border border-white/20"
            >
              Explore Map
            </Link>
            <Link
              to="/map"
              className="px-6 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 hover:shadow-lg hover:shadow-blue-500/50 transition font-semibold"
            >
              Get Started →
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-10 left-10 w-80 h-80 bg-blue-500/20 rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
          <div className="absolute bottom-10 right-10 w-80 h-80 bg-purple-500/20 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" style={{ animationDelay: '2s' }}></div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <h1 className="text-5xl md:text-6xl font-bold leading-tight">
              Real Estate Intelligence
              <span className="block text-transparent bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-400 bg-clip-text">
                Powered by AI
              </span>
            </h1>
            <p className="text-xl text-gray-300 leading-relaxed">
              Discover high-growth infrastructure zones across Indian cities before they boom. 
              PropAI combines satellite imagery, NLP, and geospatial analysis to predict real estate opportunities.
            </p>
            <div className="flex gap-4 pt-4">
              <Link
                to="/map"
                className="px-8 py-4 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 hover:shadow-lg hover:shadow-blue-500/50 transition font-semibold flex items-center gap-2"
              >
                Explore Now <ArrowRight size={20} />
              </Link>
              <Link
                to="/map"
                className="px-8 py-4 rounded-lg border border-white/20 hover:bg-white/10 transition font-semibold"
              >
                View Demo
              </Link>
            </div>
          </div>

          {/* Hero Image */}
          <div className="relative">
            <div className="aspect-square rounded-2xl overflow-hidden border border-white/10 backdrop-blur-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/10 flex items-center justify-center text-8xl">
              🗺️
            </div>
            <div className="absolute -bottom-6 -right-6 w-40 h-40 bg-blue-500/30 rounded-full filter blur-3xl -z-10"></div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, idx) => (
            <div key={idx} className="text-center p-8 rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition">
              <div className="text-4xl md:text-5xl font-bold text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text mb-2">
                {stat.number}
              </div>
              <p className="text-gray-300">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-4">
          Powerful Features for
          <span className="block text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text">
            Smart Investors
          </span>
        </h2>
        <p className="text-center text-gray-300 text-lg mb-16 max-w-2xl mx-auto">
          Advanced technology that transforms raw infrastructure data into actionable investment insights
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, idx) => (
            <div
              key={idx}
              className="p-8 rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm hover:border-white/20 hover:bg-white/10 transition group"
            >
              <div className="mb-4 group-hover:scale-110 transition transform">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
              <p className="text-gray-300 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-16">
          How <span className="text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text">PropAI</span> Works
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          {[
            { step: 1, title: "Data Collection", desc: "Real-time scraping of infrastructure news from 50+ sources" },
            { step: 2, title: "NLP Processing", desc: "Entity extraction and event classification with spaCy" },
            { step: 3, title: "Geospatial Analysis", desc: "Zone generation using PostGIS and geographic clustering" },
            { step: 4, title: "Growth Scoring", desc: "Risk assessment algorithm determines investment potential" }
          ].map((item, idx) => (
            <div key={idx} className="relative">
              <div className="bg-gradient-to-br from-blue-500/30 to-cyan-500/10 border border-white/10 rounded-xl p-6 text-center">
                <div className="text-4xl font-bold text-blue-400 mb-3">{item.step}</div>
                <h4 className="font-bold mb-2">{item.title}</h4>
                <p className="text-sm text-gray-300">{item.desc}</p>
              </div>
              {idx < 3 && (
                <div className="hidden md:block absolute top-1/2 -right-3 transform -translate-y-1/2">
                  <ArrowRight className="text-blue-400/50" size={24} />
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-16">
          Trusted by
          <span className="block text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text">
            Industry Leaders
          </span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, idx) => (
            <div
              key={idx}
              className="p-8 rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition"
            >
              <div className="flex items-center gap-3 mb-4">
                {[1, 2, 3, 4, 5].map(i => (
                  <Star key={i} size={18} className="fill-yellow-400 text-yellow-400" />
                ))}
              </div>
              <p className="text-gray-200 mb-4 italic">"{testimonial.text}"</p>
              <div className="flex items-center gap-3">
                <div className="text-3xl">{testimonial.avatar}</div>
                <div>
                  <p className="font-bold">{testimonial.name}</p>
                  <p className="text-sm text-gray-400">{testimonial.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        <div className="absolute inset-0 -z-10">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 blur-3xl"></div>
        </div>

        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Discover Hidden Opportunities?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Start analyzing infrastructure zones in your target cities today. 
            No credit card required.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/map"
              className="px-8 py-4 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 hover:shadow-lg hover:shadow-blue-500/50 transition font-semibold text-lg"
            >
              Start Free Exploration →
            </Link>
            <Link
              to="/map"
              className="px-8 py-4 rounded-lg border border-white/20 hover:bg-white/10 transition font-semibold text-lg"
            >
              View Live Data
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-black/40 backdrop-blur-md py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-lg mb-4">PropAI</h3>
              <p className="text-gray-400">AI-driven real estate intelligence for Indian markets</p>
            </div>
            <div>
              <h4 className="font-bold mb-4">Platform</h4>
              <div className="space-y-2 text-gray-400">
                <p><Link to="/map" className="hover:text-white transition">Live Map</Link></p>
                <p><Link to="/map" className="hover:text-white transition">Events</Link></p>
                <p><Link to="/map" className="hover:text-white transition">Insights</Link></p>
              </div>
            </div>
            <div>
              <h4 className="font-bold mb-4">Resources</h4>
              <div className="space-y-2 text-gray-400">
                <p><a href="#" className="hover:text-white transition">Documentation</a></p>
                <p><a href="#" className="hover:text-white transition">Blog</a></p>
                <p><a href="#" className="hover:text-white transition">FAQ</a></p>
              </div>
            </div>
            <div>
              <h4 className="font-bold mb-4">Company</h4>
              <div className="space-y-2 text-gray-400">
                <p><a href="#" className="hover:text-white transition">About</a></p>
                <p><a href="#" className="hover:text-white transition">Contact</a></p>
                <p><a href="#" className="hover:text-white transition">Privacy</a></p>
              </div>
            </div>
          </div>
          <div className="border-t border-white/10 pt-8 flex justify-between items-center text-gray-400">
            <p>&copy; 2025 PropAI. All rights reserved.</p>
            <div className="flex gap-4">
              <a href="#" className="hover:text-white transition">Twitter</a>
              <a href="#" className="hover:text-white transition">LinkedIn</a>
              <a href="#" className="hover:text-white transition">GitHub</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage
