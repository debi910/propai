# Setup Instructions for PropAI

## Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL database (Neon recommended for free tier)
- Git

---

## Backend Setup

### 1. Install Python
**If Python is not installed, download from:** https://www.python.org/downloads/

When installing:
- ✅ Check: "Add Python to PATH"
- ✅ Check: "Install pip"
- Restart terminal after installation

Verify:
```bash
python --version
```

### 2. Virtual Environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt

# Optional: Download spaCy model for NLP
python -m spacy download en_core_web_sm
```

### 3. Database Configuration
✅ **Already done!** Your `.env` file is configured with:
```
DATABASE_URL=postgresql://neondb_owner:npg_Bd9LNy2PutYe@ep-cool-lab-anobxnbc.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development
```

This connects directly to your Neon PostgreSQL instance.

### 4. Initialize Database
```bash
# Create all tables in Neon
python -c "from models.database import init_db; init_db()"

# Expected output: ✅ Database tables initialized
```

⚠️ **If you get connection errors:**
- Verify .env DATABASE_URL is correct
- Check internet connection (Neon is cloud-hosted)
- Test: `psql $DATABASE_URL -c "SELECT 1"` (if psql installed)

### 5. Load Sample Data
```bash
python seeds/load_samples.py

# Expected output:
# 🌱 Starting database seed...
# ✅ Database tables initialized
# ✅ Loaded 3 cities
# ✅ Loaded 5 events
# ✅ Loaded 7 zones with scores
# 🎉 Database seeding complete!
```

### 6. Run Backend Server
```bash
python main.py

# Expected output:
# 🚀 Starting PropAI Backend...
# ✅ Database initialized
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Then visit: http://localhost:8000/docs
```

**Keep this terminal open.** Open a new terminal for the frontend.

---

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
Create `.env` from `.env.example`:
```bash
VITE_API_URL=http://localhost:8000/api
VITE_MAPBOX_TOKEN=your_mapbox_token_here
```

**Note:** Mapbox is optional for MVP. Map will show placeholder without token.

### 3. Run Development Server
```bash
npm run dev
# Opens at http://localhost:5173
```

### 4. Build for Production
```bash
npm run build
# Creates optimized bundle in dist/
```

---

## Data Pipeline Setup

### 1. Install Dependencies
```bash
cd data-pipeline
pip install -r requirements.txt

# Optional: Install spaCy model locally
python -m spacy download en_core_web_sm
```

### 2. Test Scrapers
```bash
cd scrapers
python rss_fetcher.py
# Should fetch and display recent news articles
```

### 3. Test NLP
```bash
cd ../nlp
python entity_extractor.py
# Should extract locations and event types from sample text
```

### 4. Test Full Pipeline
```bash
cd ..
python orchestrator.py
# Runs: scrape → NLP → geocode → score → store
```

---

## Database (Neon Setup)

### 1. Create Free Account
- Visit: https://console.neon.tech
- Sign up with GitHub or email
- Create new project

### 2. Get Connection String
```
postgresql://[user]:[password]@[host]/[database]
```

### 3. Enable PostGIS
```sql
-- Connect to your database and run:
CREATE EXTENSION IF NOT EXISTS postgis;
```

### 4. Initialize Schema
```bash
# From backend directory:
psql $DATABASE_URL < database.sql
```

---

## Verify Installation

### Backend Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "service": "propai-api"}
```

### API Test
```bash
curl http://localhost:8000/api/cities
# Should return sample cities JSON
```

### Frontend Check
- Open http://localhost:5173 in browser
- Should see home page without errors
- Network tab should show API calls to backend

---

## Troubleshooting

### "Database connection error"
- Check DATABASE_URL in .env
- Verify Neon connection string format
- Test: `psql $DATABASE_URL -c "SELECT 1"`

### "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### "CORS errors in frontend"
- Ensure FRONTEND_URL in backend .env matches your frontend domain
- Check browser console for specific origin errors

### "Port 8000 already in use"
```bash
# Change port in .env
API_PORT=8001
# Or kill existing process on port 8000
```

### "npm ERR! peer dep missing"
```bash
npm install --legacy-peer-deps
```

---

## Environment Variables Reference

### Backend (.env)
```
DATABASE_URL=postgresql://...  # Neon connection string
FRONTEND_URL=http://localhost:3000  # For CORS
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
VITE_MAPBOX_TOKEN=pk_xxxxx  # Optional, get from mapbox.com
```

---

## Next Steps

1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:5173
3. ✅ Database connected with sample data
4. → Proceed to Phase 2 (Event Scrapers & NLP)

---

## Quick Reference

| Component | URL | Status Check |
|-----------|-----|--------------|
| Backend | http://localhost:8000 | `curl localhost:8000/health` |
| Frontend | http://localhost:5173 | Browser navigation works |
| API Docs | http://localhost:8000/docs | Swagger UI visible |
| Database | Neon | `psql $DATABASE_URL -c "SELECT 1"` |

---

For next phase setup instructions, see DEPLOYMENT.md
