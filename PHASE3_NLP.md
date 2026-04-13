# 🧠 Phase 3: NLP Extraction & Geocoding (Ready)

## What's New in Phase 3

✅ **Entity Extraction** - Detects locations & organizations with spaCy  
✅ **Event Classification** - Auto-classifies events (Highway, Metro, Airport, Tech Park)  
✅ **Status Detection** - Identifies project status (Approved, Proposed, Constructed)  
✅ **Geocoding** - Converts locations to lat/long coordinates  
✅ **NLP Processing Activated** - Steps 2 & 3 of pipeline now live  

---

## How It Works

### 1️⃣ Entity Extraction (`data-pipeline/nlp/entity_extractor.py`)

**Features:**
- Uses spaCy NER to identify Geopolitical Entities (GPE)
- Hardcoded database of 100+ Indian cities & neighborhoods
- Extracts organizations mentioned in news
- Classifies event types:
  - **Highway** - Expressways, roads, corridors
  - **Metro** - Subway, rail transit systems
  - **Airport** - Aviation terminals
  - **Factory** - Industrial zones, plants
  - **Tech_Park** - IT parks, business hubs
  
- Identifies project status:
  - **Approved** - Sanctioned, cleared, green light
  - **Proposed** - Planned, announced
  - **Under_Construction** - Ongoing, being built
  - **Completed** - Operational, launched

**Example:**
```
Input: "Delhi-Mumbai Expressway Phase 2 approved for Sector 45, Gurgaon"
Output:
  - Locations: [Gurgaon, Delhi, Mumbai]
  - Event Type: Highway
  - Status: Approved
```

### 2️⃣ Geocoder (`data-pipeline/nlp/geocoder.py`)

**Features:**
- Converts location names to GPS coordinates
- Uses hardcoded coordinates for major Indian cities (instant, no API calls)
- Falls back to Nominatim/OpenStreetMap API for unknown locations
- Covers:
  - 10 major Indian cities (Bangalore, Mumbai, Delhi, Hyderabad, etc.)
  - 20+ neighborhoods (Whitefield, Koramangala, Hitec City, etc.)

**Speed:**
- Hardcoded lookups: Instant
- Nominatim API: ~1 second per location (rate limited)

**Example:**
```
Input: Whitefield, Bangalore
Output: (12.9698, 77.7499)
```

---

## Run the NLP Pipeline

### From Python (If Installed)

```bash
# Full pipeline with NLP & Geocoding
python backend/run_phase3.py
```

**Expected Output:**
```
🚀 PHASE 3: NLP Extraction & Geocoding Pipeline
📰 Step 1: Fetching events from sources...
✅ Stored X new events
🧠 Step 2: Processing with NLP...
✅ Classified Y events with NLP
📍 Step 3: Geocoding locations...
✅ Geocoded Z events

✅ Phase 3 Complete!
```

---

## Verify Results

### In Neon Console

```sql
-- See all events with locations
SELECT title, location, source_name 
FROM events 
WHERE location IS NOT NULL
LIMIT 10;

-- Count by location
SELECT location, COUNT(*) 
FROM events 
WHERE location IS NOT NULL
GROUP BY location;

-- See event classifications
SELECT 
    e.title,
    e.location,
    ec.name as event_type,
    ec.description
FROM events e
LEFT JOIN event_classifications ec ON e.id = ec.id;
```

### Via API

```bash
# See events with locations
curl "http://localhost:8000/api/events" | jq '.items[] | {title, location, source_name}'

# See city zones
curl "http://localhost:8000/api/cities/Bangalore" | jq '.zones'
```

---

## Data Flow: Phase 3

```
RSS Feeds
    ↓
[Phase 2] Scraper → Raw Events in DB
    ↓
[Phase 3] Entity Extraction → Locations, Types, Status
    ↓
[Phase 3] Geocoding → Coordinates (lat/lng)
    ↓
[Phase 4] Zone Generator → Create growth polygons
    ↓
[Phase 4] Scoring Engine → Risk levels (Green/Yellow/Red)
    ↓
API Endpoints → Frontend visualization
```

---

## Next: Phase 4 (Geospatial & Scoring)

Phase 4 will:
1. Create zone geometries (GeoJSON polygons)
2. Link events to nearest zones
3. Compute growth scores based on:
   - Highway proximity (+30 pts)
   - Metro proximity (+40 pts)
   - Airport proximity (+15 pts)
   - Factory proximity (-25 pts)
4. Assign risk levels:
   - **GREEN** (76-100): High growth potential
   - **YELLOW** (51-75): Moderate growth
   - **RED** (0-50): Lower potential or risk

---

## File Changes Summary

| File | Change |
|------|--------|
| `entity_extractor.py` | ✅ Already optimized for events |
| `geocoder.py` | ✅ Already optimized for events |
| `orchestrator.py` | ✅ Activated steps 2 & 3, improved NLP |
| `run_phase3.py` | ✨ New test runner for Phase 3 |

All changes are backward compatible and can run multiple times.

---

## Dependencies

The following Python packages are required (already in requirements.txt):

- **spacy** - NLP entity extraction
- **geopy** - Geocoding
- **feedparser** - RSS parsing (from Phase 2)
- **sqlalchemy** - Database ORM

Auto-download spaCy model if needed:
```bash
python -m spacy download en_core_web_sm
```

---

## Performance Notes

- **NLP Processing**: ~50-100ms per event (depends on spaCy model)
- **Geocoding**: 
  - Hardcoded: <1ms per location
  - API lookup: ~1-2 seconds (rate limited)
- **Batch Processing**: All events in one run

For production, consider:
- Running in background job (Celery/RQ)
- Caching geocoding results
- Batch API calls with timeout handling

---

**Ready for Phase 4?** Let's build the geospatial engine! 🗺️
