# 🚀 Quick Start - 10 Minutes (Or Just 2 Minutes for Database!)

## New: Set Up Database in 2 Minutes (No Installation!)

Don't want to install anything? ⚡

1. Go to **https://console.neon.tech** → Your project
2. Click **SQL Editor**
3. Paste this file: [database.sql](database.sql)
4. Click **Run**
5. ✅ Done!

👉 **Detailed guide:** [NEON_SETUP.md](NEON_SETUP.md)

---

## Full Setup (With Backend + Frontend)

**Option A: Web-only (No installation needed!)**
- ✅ Neon account + database created
- ✅ Code editor (VS Code, etc.) - just to read files

**Option B: Full local development**
- ✅ Python 3.9+ (https://www.python.org/downloads/)
- ✅ Node.js 16+ (for frontend)
- ✅ Neon account + database
- ✅ Git (for deployment)

---

## 5-Step Setup

### Step 1️⃣: Clone & Backend Setup (2 min)
```bash
cd d:\propai\backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optional: NLP model (only if Phase 3+ testing needed)
python -m spacy download en_core_web_sm
```

### Step 2️⃣: Database Initialization (2 min)

**⚡ FASTEST: Use Neon SQL Editor (no Python needed!)**

1. Go to https://console.neon.tech → Click your project
2. Click **SQL Editor** (left sidebar)
3. Copy entire [database.sql](database.sql) file
4. Paste + click **Run**
5. Done! ✅

**OR: Use Python (if installed)**

```bash
# Create all tables
python -c "from models.database import init_db; init_db()"
echo ✅ Tables created

# Load sample data
python seeds/load_samples.py
echo ✅ Sample data loaded
```

👉 [Detailed database setup guide →](NEON_SETUP.md)

### Step 3️⃣: Run Verification Tests (1 min)
```bash
# Comprehensive test suite
python test_setup.py

# Expected output: "🎉 All tests passed! Ready to run backend."
```

### Step 4️⃣: Start Backend (1 min)
```bash
python main.py

# Expected output:
# 🚀 Starting PropAI Backend...
# ✅ Database initialized
# INFO: Uvicorn running on http://0.0.0.0:8000
```

**Keep terminal open** → Open new terminal for Step 5

### Step 5️⃣: Frontend Setup (4 min)
```bash
cd d:\propai\frontend

# Install dependencies (2 min)
npm install

# Start development server
npm run dev

# Expected: "➜ Local: http://localhost:5173/"
```

---

## ✅ Done! Test These URLs

| URL | Expected |
|-----|----------|
| **Frontend** | http://localhost:5173 → Home page loads |
| **Backend API** | http://localhost:8000/api/cities → JSON array of 3 cities |
| **API Docs** | http://localhost:8000/docs → Swagger UI |
| **Health Check** | http://localhost:8000/health → `{"status": "healthy"}` |

---

## Quick API Tests (Copy-Paste)

Open PowerShell/Terminal and run:

### Get all cities
```bash
curl http://localhost:8000/api/cities
```

### Get zones for Bangalore
```bash
curl "http://localhost:8000/api/zones?city_id=1"
```

### Get events
```bash
curl "http://localhost:8000/api/events?limit=5"
```

### Get city insights
```bash
curl http://localhost:8000/api/cities/Bangalore
```

---

## Troubleshooting

### "Python not found"
→ Install Python from https://www.python.org/downloads/  
→ Check "Add Python to PATH" during installation  
→ Restart terminal

### "Database connection failed"
→ Check `.env` DATABASE_URL is correct  
→ Verify Neon project exists in console  
→ Test: `psql $DATABASE_URL -c "SELECT 1"`

### "Module not found" error
→ Make sure venv is activated: `venv\Scripts\activate`  
→ Reinstall: `pip install -r requirements.txt --force-reinstall`

### Frontend shows blank page
→ Check browser console (F12)  
→ Check `.env` has `VITE_API_URL=http://localhost:8000/api`  
→ Clear cache: `npm run dev` and hard-refresh browser

### "npm ERR! peer dep missing"
→ Run: `npm install --legacy-peer-deps`

---

## What's Included

✅ **Backend (FastAPI)**
- 8 API endpoints for zones, cities, events
- PostgreSQL + PostGIS database
- ORM models + automatic table creation
- Sample data (3 cities, 5 events, 15 zones)

✅ **Frontend (React)**
- 4 pages: Home, Map, Events, City Insights
- Dark mode toggle
- Responsive design with Tailwind CSS
- Real-time API integration

✅ **Database (Neon PostgreSQL)**
- 7 tables with spatial indexing
- Automatic backups
- SSL encryption included
- 100 CU-hrs/month free

✅ **NLP Pipeline (headless)**
- Event scraping (RSS feeds)
- Location entity extraction (spaCy)
- Geocoding (geopy)
- Zone generation + scoring

---

## Documentation

- 📖 **Full Setup Guide**: `SETUP.md`
- 🧪 **Testing Guide**: `TESTING.md`
- 🚢 **Deployment Guide**: `DEPLOYMENT.md`
- 📜 **Project README**: `README.md`

---

## What's Next

After setup verification:
- 🎯 **Phase 2**: Real event scrapers (RSS feeds → database)
- 🧠 **Phase 3**: NLP extraction (locations, event types)
- 📊 **Phase 4**: Scoring engine (rule-based growth scores)
- 🌐 **Phase 5**: Full backend + API testing
- 🎨 **Phase 6**: 3D map integration (Mapbox GL JS)
- ⚙️ **Phase 7**: Automation + deployment

---

## File Locations

```
propai/
├── backend/          ← Backend (FastAPI) - START HERE
│   ├── main.py
│   ├── test_setup.py ← Run this after setup
│   ├── .env          ← Database config (already created)
│   └── requirements.txt
│
├── frontend/         ← Frontend (React)
│   ├── .env          ← API URL config (already created)
│   └── package.json
│
├── data-pipeline/    ← Data processing (Phase 2+)
├── sample-data/      ← Demo data (cities, events, zones)
└── TESTING.md        ← Detailed test procedures
```

---

## Important Files

✅ **Already configured:**
- `backend/.env` → Neon connection string
- `frontend/.env` → API URL
- `backend/requirements.txt` → All dependencies
- `backend/seeds/load_samples.py` → Demo data loader

---

## Verify Installation Completed

After running all 5 steps, you should see:

```
Backend Terminal:
  🚀 Starting PropAI Backend...
  ✅ Database initialized
  INFO: Uvicorn running on http://0.0.0.0:8000

Frontend Terminal:
  ➜ Local: http://localhost:5173/

Browser (localhost:5173):
  - Home page visible
  - 4 navigation links work
  - Dark mode toggle visible
  - No console errors (F12)

Browser Network (F12):
  - GET /api/cities → 200
  - GET /api/zones → 200
  - GET /api/events → 200
```

---

**Ready? Start with Step 1️⃣ above!**

*Estimated total time: 10-15 minutes*
