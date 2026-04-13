# 🗄️ Neon Database Setup Guide

## Option 1: Direct SQL in Neon Console (Recommended - No Python needed!)

### Step 1: Access Neon Console
1. Go to **https://console.neon.tech**
2. Sign in with your account
3. Click your project name (should show your database)
4. Click "SQL Editor" in the left sidebar

### Step 2: Run the Setup Script
1. Open [database.sql](../database.sql) 
2. Copy the entire contents
3. Paste into the Neon SQL Editor
4. Click "Run" or press **Ctrl+Enter**

✅ Tables are created!  
✅ Sample data is loaded!  
✅ Indexes are created!

### What Gets Created
- ✅ 7 tables (cities, events, zones, scores, etc.)
- ✅ 3 sample cities (Bangalore, Hyderabad, Bhubaneswar)
- ✅ 5 sample events
- ✅ 10+ zones with scores
- ✅ PostGIS enabled for spatial queries

### Verify Setup
Run this in the SQL Editor:
```sql
-- Check row counts
SELECT 
    'cities' as table_name, COUNT(*) as row_count FROM cities
UNION ALL
SELECT 'events', COUNT(*) FROM events
UNION ALL
SELECT 'zones', COUNT(*) FROM zones
UNION ALL
SELECT 'scores', COUNT(*) FROM scores;
```

Expected output:
```
table_name    row_count
cities        3
events        5
zones         7
scores        7
```

---

## Option 2: Using Python (If Python 3.9+ Installed)

If you have Python installed:

```bash
cd backend
pip install -r requirements.txt
python -c "from models.database import init_db; init_db()"
python seeds/load_samples.py
```

---

## Option 3: Using psql Command Line

If you have PostgreSQL client installed:

1. Download [database.sql](../database.sql)
2. Run:
```bash
psql "postgresql://neondb_owner:npg_Bd9LNy2PutYe@ep-cool-lab-anobxnbc.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require" < database.sql
```

---

## Viewing Your Data

### In Neon Console
Left sidebar → Tables → Click any table to view data

### Via API
Once backend is running:
```bash
curl http://localhost:8000/api/cities
curl http://localhost:8000/api/zones
curl http://localhost:8000/api/events
```

---

## Adding More Sample Data

### Cities
```sql
INSERT INTO cities (name, tier, region, latitude, longitude) VALUES
    ('Mumbai', 'Tier-1', 'West', 19.0760, 72.8777),
    ('Delhi', 'Tier-1', 'North', 28.7041, 77.1025)
ON CONFLICT (name) DO NOTHING;
```

### Events
```sql
INSERT INTO events (title, description, location, event_date, source_url, source_name, classification_id) VALUES
    ('New Metro Line', 'Extended metro to suburbs', 'Mumbai', '2026-12-01', 'https://example.com', 'News', 
     (SELECT id FROM event_classifications WHERE name = 'Metro/Transit')
    )
ON CONFLICT DO NOTHING;
```

### Zones
```sql
INSERT INTO zones (city_id, name, zone_type, description, geometry) VALUES
    (
        (SELECT id FROM cities WHERE name = 'Mumbai'),
        'Navi Mumbai',
        'Business Zone',
        'New development area',
        ST_GeomFromText('POLYGON((72.95 19.05, 73.00 19.05, 73.00 19.10, 72.95 19.10, 72.95 19.05))', 4326)
    )
ON CONFLICT (city_id, name) DO NOTHING;
```

---

## Connecting to Database Locally

If you want to connect from a local tool (like DBeaver, pgAdmin):

**Connection Details:**
- Host: `ep-cool-lab-anobxnbc.c-6.us-east-1.aws.neon.tech`
- Port: `5432`
- Database: `neondb`
- User: `neondb_owner`
- Password: `npg_Bd9LNy2PutYe`
- SSL Mode: `require`

---

## Troubleshooting

### Tables Already Exist
The SQL script uses `ON CONFLICT DO NOTHING` so it's safe to run multiple times.

### Permission Denied
Ensure you're using the correct role (neondb_owner).

### PostGIS Not Available
Neon includes PostGIS by default - it's already enabled.

### Geometry Errors
The sample zones use dummy polygon geometries. Update them with real coordinates using PostGIS tools.

---

## Next Steps

1. ✅ Set up database tables (you're here!)
2. Start backend: `python backend/main.py`
3. Start frontend: `npm -C frontend run dev`
4. Test API endpoints
5. Deploy to Railway/Vercel

See [QUICKSTART.md](../QUICKSTART.md) for complete 10-minute setup.
