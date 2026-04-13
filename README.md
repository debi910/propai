# PropAI - AI-Powered Real Estate Intelligence Platform for India

## 🎯 Project Overview

A web platform that detects future real estate growth zones using AI analysis of infrastructure news, government announcements, and development signals. Displays results on a 3D interactive map with AI-based risk scoring.

**Status:** Phase 1 Complete ✅ (Project Bootstrap)  
**Next Phase:** Phase 2 (Event Scrapers)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                FRONTEND (React + Vite)                  │
│        (3D Map + Pages + Dark Mode Support)             │
│        Deployed on: Vercel                               │
├─────────────────────────────────────────────────────────┤
│              BACKEND API (FastAPI)                       │
│    (6 REST endpoints, CORS enabled, async)              │
│        Deployed on: Railway free tier                   │
├─────────────────────────────────────────────────────────┤
│          DATA PIPELINE (Headless Python)                │
│  (RSS scrapers → NLP extraction → Scoring → DB)         │
│  Runs on: GitHub Actions (free) or Railway worker       │
├─────────────────────────────────────────────────────────┤
│    DATABASE (PostgreSQL + PostGIS on Neon)              │
│      (100 CU-hrs/month free, scales to zero)            │
│  Tables: cities, events, zones, scores, classifications │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
propai/
├── backend/                      # FastAPI backend
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py            # 6 API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── orm.py               # SQLAlchemy models (7 tables)
│   │   └── database.py          # DB connection & session
│   ├── services/
│   ├── seeds/
│   │   └── load_samples.py      # Load demo data
│   ├── main.py                  # FastAPI app entry point
│   ├── database.sql             # SQL schema (manual setup)
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/                     # React + Vite app
│   ├── src/
│   │   ├── components/
│   │   ├── pages/               # 4 pages: Home, Map, Events, Insights
│   │   ├── layout/
│   │   │   ├── Navbar.jsx
│   │   │   └── Footer.jsx
│   │   ├── hooks/
│   │   ├── styles/
│   │   ├── App.jsx              # Router setup
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json             # React deps
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.example
│   └── .gitignore
│
├── data-pipeline/               # Headless processing
│   ├── scrapers/
│   │   ├── base_scraper.py     # Abstract base class
│   │   ├── rss_fetcher.py      # RSS feed parser (Economic Times, Moneycontrol)
│   │   └── __init__.py
│   ├── nlp/
│   │   ├── entity_extractor.py # Location + event type extraction (spaCy)
│   │   ├── geocoder.py         # Convert location → lat/long (geopy)
│   │   └── __init__.py
│   ├── geospatial/
│   │   ├── zone_generator.py   # Create zone polygons from events (PostGIS buffers)
│   │   └── __init__.py
│   ├── scoring/
│   │   ├── scorer.py           # Rule-based scoring engine (0-100 scale)
│   │   └── __init__.py
│   ├── orchestrator.py         # Coordinates full pipeline
│   ├── requirements.txt
│   └── Dockerfile (for cron job)
│
├── sample-data/                 # Pre-populated demo data
│   ├── cities.json             # 3 cities: Bangalore, Bhubaneswar, Hyderabad
│   ├── events.json             # 5 sample infrastructure events
│   └── zones.geojson           # 15 sample zones (3 cities × 5 zones each)
│
├── .gitignore
└── package.json                # Root scripts
```

---

## 🚀 Quick Start

👉 **New users**: Start here → [QUICKSTART.md](QUICKSTART.md) (10 minutes)

📊 **Project Status**: [COMPLETION_REPORT.md](COMPLETION_REPORT.md) (Phase 1 ✅ Complete)

🔥 **Data Pipeline Ready**: [PHASES_2_4_SUMMARY.md](PHASES_2_4_SUMMARY.md) (Phases 2-4 ✅ Complete!)

For detailed setup: [SETUP.md](SETUP.md)

---

## 📊 Database Schema

### Tables (7)
1. **cities** - City metadata + location
2. **events** - Raw news events (headline, content, source, date)
3. **event_classifications** - NLP extraction (event_type, status, location, lat/long, confidence)
4. **zones** - Geographic polygons with growth potential (shape, center_point)
5. **scores** - Scoring breakdown (growth_score 0-100, risk_level, time_horizon)
6. **zone_events** - Pivot table linking zones to triggering events
7. *(Users table reserved for future auth)*

### Spatial Indexes
- GIST index on `zones.shape` for fast polygon queries
- GIST index on `event_classifications` point geometry

---

## 🔌 API Endpoints (6)

All endpoints return JSON. Base URL: `http://localhost:8000/api`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/cities` | GET | List all cities with zone counts |
| `/cities/{city_name}` | GET | City insights (stats, avg score) |
| `/zones?city_id=1&risk_level=Green&score_min=50&score_max=100` | GET | Filter zones |
| `/zones/{zone_id}` | GET | Zone details (score breakdown, events) |
| `/events?city_id=1&event_type=Highway&skip=0&limit=20` | GET | Events with pagination |
| `/events/{event_id}` | GET | Event full details |
| `/map/data?city_id=1` | GET | GeoJSON for map rendering |

### Example Request
```bash
curl http://localhost:8000/api/cities
```

---

## 🎨 Frontend Pages (4)

1. **Home** (`/`)
   - Hero section with CTA buttons
   - Feature highlights + stats
   - Legal disclaimer

2. **Map** (`/map`)
   - 3D interactive map (Mapbox GL JS placeholder)
   - City selector dropdown
   - Zone list panel (color-coded by risk)
   - Click zone → show details

3. **Events** (`/events`)
   - Latest infrastructure events (paginated)
   - Filters: city, event type, date
   - Click to expand + source link

4. **City Insights** (`/insights`)
   - Per-city dashboard
   - Zone distribution chart
   - Top 10 growth opportunities (table)

---

## 🧠 Data Pipeline Overview

### Phase 2: Scraping
- **RSS Fetcher** pulls news from Economic Times, Moneycontrol, PIB
- Filters by infrastructure keywords
- Stores raw_text + metadata in `events` table

### Phase 3: NLP
- **Entity Extractor** (spaCy) extracts locations, event types, status
- **Geocoder** (geopy + Nominatim) converts location → lat/long
- Stores parsed data in `event_classifications` table

### Phase 4: Scoring
- **Zone Generator** creates polygon buffers around events
- **Scorer** applies rule-based weights:
  - Highway +30, Metro +40, Airport +15, Factory +25, Regulation +10
  - Approved status +20, Tier-1 city +10
  - Growth Score (0-100) → Risk Level (Green/Yellow/Red) → Time Horizon

### Automation
- Cron job daily at 02:00 UTC (minimal load)
- Runs full pipeline: scrape → NLP → geocode → score → store
- Fallback: GitHub Actions (free 20K min/month)

---

## 🎯 Scoring Rules

**Rule-Based Weights:**
```
Event Type      | Weight | Status          | Bonus
────────────────┼────────┼─────────────────┼────────
Highway         | +30    | Approved        | +20
Metro           | +40    | Under Const.    | +15
Airport         | +15    | Proposed        | +5
Factory         | +25    | Completed       | +25
Government Reg. | +10    |                 |
────────────────┴────────┴─────────────────┴────────
Tier-1 City Bonus: +10

Growth Score Mapping:
  ≥70   → 🟢 Green   (High growth, 3-5 years)
  50-69 → 🟡 Yellow  (Medium growth, 5-8 years)
  <50   → 🔴 Red     (Low growth, 8-12 years)
```

---

## 📦 Sample Data

Pre-loaded demo data includes:

**Cities:** Bangalore, Bhubaneswar, Hyderabad (3)  
**Events:** Metro, Highway, Airport, Factory, Government approvals (5)  
**Zones:** 15 total (3 cities × 5 zones each) with computed scores

Load sample data:
```bash
cd backend
python seeds/load_samples.py
```

---

## 🚢 Deployment (Free Tier)

### Backend (Railway)
```bash
# Push to GitHub
git push origin main

# Railway auto-deploys on push
# Set environment variables in Railway dashboard:
# - DATABASE_URL (Neon connection)
# - FRONTEND_URL (Vercel domain)
```

### Frontend (Vercel)
```bash
# Option 1: Git push (auto-deploy)
npm run build
git push origin main

# Option 2: Vercel CLI
npm i -g vercel
vercel
```

### Database (Neon PostgreSQL)
1. Create free account: neon.tech
2. Create project + database
3. Copy connection string → Railway + local .env
4. Run migrations

---

## 📋 Phase Checklist

- [x] **Phase 1:** Project setup, DB schema, ORM models, basic API, frontend structure
- [ ] **Phase 2:** RSS scrapers, event ingestion
- [ ] **Phase 3:** NLP extraction, geocoding
- [ ] **Phase 4:** Zone generation, scoring engine
- [ ] **Phase 5:** API integration, deploy backend
- [ ] **Phase 6:** 3D map integration, frontend polish
- [ ] **Phase 7:** Automation (cron), documentation, testing

---

## ⚖️ Legal & Disclaimer

⚠️ **Important:** This platform provides AI-based insights for **informational purposes only**. It does not:
- Guarantee property returns or valuations
- Constitute investment advice
- Make price predictions

Always conduct thorough due diligence and consult qualified real estate professionals.

---

## 🛠️ Tech Stack

| Layer | Tech | Cost |
|-------|------|------|
| Frontend | React 18, Vite, Tailwind CSS, Mapbox GL JS | Free |
| Backend | FastAPI, Uvicorn, SQLAlchemy | Free |
| Database | PostgreSQL + PostGIS (Neon) | Free (100 CU-hrs/mo) |
| NLP | spaCy, geopy (Nominatim) | Free |
| Scraping | Scrapy, Playwright, feedparser | Free |
| Deployment | Vercel, Railway, Neon | Free tier MVP |

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | ⚡ 10-minute setup (start here!) |
| [NEON_SETUP.md](NEON_SETUP.md) | 🗄️ Direct SQL database setup (no Python needed!) |
| [PHASES_2_4_SUMMARY.md](PHASES_2_4_SUMMARY.md) | 🔥 **Data Pipeline Complete!** Event scraper → NLP → Scoring |
| [SETUP.md](SETUP.md) | 📋 Detailed local setup instructions |
| [TESTING.md](TESTING.md) | 🧪 Comprehensive testing & validation |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 🚢 Free-tier deployment (Railway, Vercel, Neon) |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | ✅ Pre-deployment verification & live launch |
| [PHASE2_SCRAPERS.md](PHASE2_SCRAPERS.md) | 📰 RSS event scraper details |
| [PHASE3_NLP.md](PHASE3_NLP.md) | 🧠 NLP & geocoding pipeline |
| [PHASE4_SCORING.md](PHASE4_SCORING.md) | 🎯 Geospatial zones & risk scoring |

---

## 🤝 Contributing

This is an open-source MVP. Contributions welcome:
- Add new event sources
- Improve NLP models
- Extend scoring rules
- Fix bugs / improve UI

---

## 📜 License

Open Source. See LICENSE file.

---

**Built with ❤️ for transparency in Indian real estate intelligence.**
