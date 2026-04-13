# 📰 Phase 2: Event Scrapers (Ready)

## What's New in Phase 2

✅ **Enhanced RSS Fetcher** - Now fetches real infrastructure news  
✅ **Better Feed Sources** - Economic Times, Moneycontrol, TOI cities  
✅ **Keyword Filtering** - Smart filtering for infrastructure news  
✅ **Duplicate Detection** - Prevents duplicate events in database  
✅ **Location Extraction** - Auto-detects city names from headlines  
✅ **HTML Cleanup** - Removes HTML tags from descriptions  
✅ **Orchestrator Activated** - Step 1 of pipeline is now live  

---

## How It Works

### 1️⃣ RSS Fetcher Enhanced (`data-pipeline/scrapers/rss_fetcher.py`)

**New Features:**
- Fetches from 6 major Indian news sources
- Filters for infrastructure keywords (metro, highway, airport, tech park, etc.)
- Excludes noise keywords (celebrity, movie, sports, etc.)
- Extracts city names from titles
- Cleans HTML from descriptions
- Rate limiting (1 second between feeds)
- Timeout handling (10 seconds per feed)

**Feeds Being Used:**
1. Economic Times - Real Estate
2. Economic Times - Infrastructure
3. Moneycontrol - Infrastructure
4. TOI - Delhi
5. TOI - Mumbai
6. TOI - Bangalore

---

### 2️⃣ Orchestrator Updated (`data-pipeline/orchestrator.py`)

**Now Activated:**
- `step_scrape_events()` - Actually runs the scraper ✅
- Connects to your Neon database
- Avoids duplicates by checking source_url
- Logs statistics

**Still Deferred (Phase 3-4):**
- NLP processing
- Geocoding
- Zone generation
- Scoring

---

## Run the Scraper

### From Python (If Installed)

```bash
# From backend folder
python run_phase2.py
```

**Expected Output:**
```
🚀 PHASE 2: Event Scraper Pipeline
📡 Fetching from Economic Times - Real Estate...
✅ Found 3 relevant events from Economic Times - Real Estate
...
📊 PIPELINE STATISTICS
Total events in database: X
Total cities: 3
✅ Sample events:
  1. Metro extension planned...
     Source: Economic Times
     Location: Bangalore
```

### Via API

Once backend is running:
```bash
# See all events
curl http://localhost:8000/api/events

# See events with pagination
curl "http://localhost:8000/api/events?page=1&limit=20"

# See events in database
curl http://localhost:8000/docs
```

---

## What Gets Stored

Each fetched event includes:
- `title` - News headline
- `description` - Article summary (cleaned HTML)
- `location` - Extracted city name
- `event_date` - Publication date
- `source_url` - Link to original article
- `source_name` - News source (ET, Moneycontrol, TOI, etc.)

---

## How to Verify

### In Neon Console (Web)

```sql
-- Check fetched events
SELECT COUNT(*) FROM events;

-- See latest events
SELECT title, source_name, event_date FROM events 
ORDER BY event_date DESC LIMIT 10;

-- Events by city
SELECT location, COUNT(*) FROM events 
WHERE location IS NOT NULL
GROUP BY location;
```

### Via API

```bash
curl http://localhost:8000/api/events | jq '.items[0]'
```

---

## Next: Phase 3 (NLP Pipeline)

Phase 3 will:
1. Extract entities and locations with spaCy
2. Geocode locations to coordinates
3. Link events to zones
4. Classify event types

Ready to proceed when you say! 🚀

---

## File Changes Summary

| File | Change |
|------|--------|
| `rss_fetcher.py` | ✅ Enhanced with real feeds, better filtering |
| `orchestrator.py` | ✅ Activated scraping step |
| `run_phase2.py` | ✨ New test runner script |

All changes are backward compatible. Can run multiple times without issues.
