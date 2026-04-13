# 🧪 Testing & Verification Guide

## Quick Start Testing (60 seconds)

### Step 1: Verify Database
```bash
cd backend

# Activate venv (Windows)
venv\Scripts\activate

# Test connection
python -c "from models.database import SessionLocal; db = SessionLocal(); db.execute('SELECT 1'); print('✅ Database connected')"
```

**Expected Output:** `✅ Database connected`

### Step 2: Run Comprehensive Tests
```bash
cd backend
python test_setup.py
```

**Expected Output:**
```
============================================================
PropAI Setup Verification Test Suite
============================================================

[TEST 1/6] Testing imports...
✅ All imports successful

[TEST 2/6] Testing database connection...
✅ Database connection successful

[TEST 3/6] Testing database tables...
✅ Table counts:
   • Cities: 3
   • Events: 5
   • Zones: 15
   • Scores: 15
✅ Sample data successfully loaded

[TEST 4/6] Testing API routes...
✅ Found 8 API routes:
   • /cities
   • /cities/{city_name}
   • /zones
   • /zones/{zone_id}
   • /events
   • /events/{event_id}
   • /health
   • /map/data
✅ All critical routes present

[TEST 5/6] Testing NLP components...
✅ NLP Components:
   • EntityExtractor: Found 1 locations
   • Event type detected: Metro
   • Geocoder: Bangalore → (12.9716, 77.5946)
   • Scorer: Test score = 70/100 (Green)
✅ All NLP components working

[TEST 6/6] Testing sample data quality...
✅ Sample data quality:
   • Total zones: 15
   • Average growth score: 61.3/100
   • Risk levels present: Green, Red, Yellow
   • Bangalore: 3 zones
   • Bhubaneswar: 2 zones
   • Hyderabad: 2 zones
✅ Sample data looks good

============================================================
TEST SUMMARY
============================================================
✅ PASS - Imports
✅ PASS - Database Connection
✅ PASS - Database Tables
✅ PASS - API Routes
✅ PASS - NLP Components
✅ PASS - Sample Data Quality

Result: 6/6 tests passed

🎉 All tests passed! Ready to run backend.
Next: python main.py
```

---

## Backend API Testing

### Step 3: Start Backend Server
```bash
# In backend directory, venv activated
python main.py
```

**Expected Output:**
```
🚀 Starting PropAI Backend...
✅ Database initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Keep this running and open a **new terminal** for testing.

### Step 4: Test API Endpoints

#### Test 4.1: Health Check
```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{"status": "healthy", "service": "propai-api"}
```

#### Test 4.2: Get All Cities
```bash
curl http://localhost:8000/api/cities
```

**Expected:**
```json
[
  {
    "id": 1,
    "name": "Bangalore",
    "state": "Karnataka",
    "region": "South India",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "tier": "Tier-1",
    "zone_count": 3
  },
  ...
]
```

#### Test 4.3: Get City Insights
```bash
curl http://localhost:8000/api/cities/Bangalore
```

**Expected:**
```json
{
  "id": 1,
  "name": "Bangalore",
  "state": "Karnataka",
  "tier": "Tier-1",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "zone_count": 3,
  "green_zones": 1,
  "yellow_zones": 2,
  "red_zones": 0,
  "average_score": 66.0
}
```

#### Test 4.4: Get All Zones
```bash
curl "http://localhost:8000/api/zones?city_id=1"
```

**Expected:**
```json
[
  {
    "id": 1,
    "city_id": 1,
    "name": "Whitefield",
    "description": "IT hub with metro connectivity",
    "growth_score": 78,
    "risk_level": "Green",
    "time_horizon": "3-5 years"
  },
  ...
]
```

#### Test 4.5: Get Events with Pagination
```bash
curl "http://localhost:8000/api/events?skip=0&limit=10"
```

**Expected:**
```json
{
  "total": 5,
  "skip": 0,
  "limit": 10,
  "events": [
    {
      "id": 1,
      "headline": "Delhi-Mumbai Expressway Phase 2 Approved for Expansion",
      "content": "Ministry of Road Transport announces approval for Phase 2 with focus on Sector 45 in Gurgaon...",
      "source_name": "Economic Times",
      "source_url": "https://economictimes.indiatimes.com/",
      "published_date": "2025-10-15T10:30:00"
    },
    ...
  ]
}
```

#### Test 4.6: API Documentation
Open in browser: **http://localhost:8000/docs**

This shows interactive Swagger UI with all endpoints.

---

## Frontend Testing

### Step 5: Prepare Frontend
```bash
# In a new terminal
cd frontend
npm install
```

**Expected:** `added XXX packages`

### Step 6: Start Frontend
```bash
npm run dev
```

**Expected Output:**
```
VITE v5.0.0  ready in 123 ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

### Step 7: Manual Frontend Testing

Open **http://localhost:5173** in browser and test:

#### Page 1: Home (`/`)
- [ ] Page loads without errors
- [ ] Hero section visible with title "Real Estate Intelligence for India"
- [ ] 3 CTA buttons visible (Explore Map, Latest Events)
- [ ] Stats cards show: 15+ zones, 3 cities, 100+ events
- [ ] Legal disclaimer visible at bottom
- [ ] Dark mode toggle works (top-right)

#### Page 2: Map (`/map`)
- [ ] City dropdown shows: Bangalore, Bhubaneswar, Hyderabad
- [ ] After selecting city, zones list appears on right
- [ ] Zones are color-coded: Green/Yellow/Red
- [ ] Clicking zone shows details panel with score, risk level, time horizon
- [ ] Zone count displayed (e.g., "3 zones tracked")

#### Page 3: Events (`/events`)
- [ ] List shows 5 sample events
- [ ] Each event shows: headline, snippet, source, date
- [ ] Pagination controls visible
- [ ] Events are sorted by date (newest first)
- [ ] Source links visible and working

#### Page 4: City Insights (`/insights`)
- [ ] City dropdown selects (defaults to Bangalore)
- [ ] Stats displayed:
  - 🟢 High Growth Zones (count)
  - 🟡 Medium Growth Zones (count)
  - 🔴 Low Growth Zones (count)
  - Total Zones (count)
  - Avg Growth Score (number)
- [ ] Bar chart shows zone distribution
- [ ] Top 10 zones table shows with scores and risk levels

#### Navigation
- [ ] Navbar links work (Home, Map, Events, Insights)
- [ ] Dark mode toggle affects all pages
- [ ] Footer visible on all pages with disclaimer
- [ ] No console errors (F12 → Console tab)

---

## Browser Console Verification

While frontend is running, open DevTools (F12) and check console:

✅ **Good:**
```
[no errors]
```

❌ **Bad (fix these):**
```
CORS error about localhost:8000
→ Check FRONTEND_URL in backend .env

GET /api/cities 404
→ Check VITE_API_URL in frontend .env

Failed to load map styles
→ Mapbox token issue (optional, not required for MVP)
```

---

## Network Tab Testing

In Browser DevTools → Network tab:

1. **Reload page**
2. **Click "Fetch/XHR"** to filter network requests
3. **Expected requests to `localhost:8000/api/`:**
   - `/api/cities` → 200 OK
   - `/api/zones?city_id=1` → 200 OK
   - `/api/events?skip=0&limit=20` → 200 OK

All should be **200 (green)**, not 404 or 500.

---

## End-to-End Testing Checklist

Use this after completing all individual tests:

```
BACKEND TESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ test_setup.py: 6/6 tests passed
✅ Health check: curl localhost:8000/health → 200
✅ API /cities endpoint → returns 3 cities
✅ API /zones endpoint → returns 15 zones
✅ API /events endpoint → returns 5 events
✅ API /map/data endpoint → returns GeoJSON

FRONTEND TESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Home page loads
✅ All 4 navigation links work
✅ Map page: city selector works
✅ Map page: zones list displays
✅ Events page: show 5 events with pagination
✅ Insights page: displays city statistics
✅ Dark mode toggle works
✅ No console errors
✅ API calls successful (Network tab)

DATABASE TESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 3 cities in database
✅ 5 events in database
✅ 15 zones with scores
✅ All scores between 0-100
✅ Risk levels: Red/Yellow/Green assigned
✅ PostGIS spatial tables created

OVERALL STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 PHASE 1 COMPLETE ✅
Ready to proceed to Phase 2 (Scrapers)
```

---

## Troubleshooting

### Backend won't start
```bash
# Check Python
python --version

# Check dependencies
pip list | grep -E "fastapi|sqlalchemy|psycopg2"

# Reinstall if needed
pip install -r requirements.txt --force-reinstall
```

### Database connection fails
```bash
# Verify connection string
echo $DATABASE_URL

# Test with psql (if installed)
psql $DATABASE_URL -c "SELECT 1"

# Check Neon dashboard: does database exist?
```

### Frontend shows blank page
```bash
# Check .env file
cat .env
# Should have: VITE_API_URL=http://localhost:8000/api

# Clear cache and rebuild
rm -rf node_modules dist
npm install
npm run dev
```

### CORS errors
- Backend: Update `FRONTEND_URL` in `.env`
- Frontend: Update `VITE_API_URL` in `.env`
- Both: Restart services after changing .env

---

## Performance Checks

Once everything works, verify performance:

### Backend Response Time
```bash
time curl http://localhost:8000/api/cities
# Expected: < 500ms
```

### Map Load Speed
- Open browser DevTools → Lighthouse
- Run Lighthouse audit
- Expected: Scores >80 for Performance

### Database Query Speed
```python
# In Python shell
from models.database import SessionLocal
from models.orm import Zone
import time

db = SessionLocal()
start = time.time()
zones = db.query(Zone).all()
print(f"Query time: {(time.time()-start)*1000:.1f}ms")
# Expected: < 100ms for 15 zones
```

---

**All tests passing? Time for Phase 2! 🚀**
