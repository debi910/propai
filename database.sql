-- AI-Powered Real Estate Intelligence Platform
-- PostgreSQL + PostGIS Schema
-- Run this in Neon Console (SQL Editor)

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Cities Table
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    tier VARCHAR(50),
    region VARCHAR(50),
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Event Classifications Table
CREATE TABLE IF NOT EXISTS event_classifications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Events Table
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    event_date DATE,
    source_url VARCHAR(500),
    source_name VARCHAR(100),
    classification_id INTEGER REFERENCES event_classifications(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Zones Table
CREATE TABLE IF NOT EXISTS zones (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    zone_type VARCHAR(100),
    description TEXT,
    geometry GEOMETRY(Polygon, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(city_id, name)
);

-- 5. Scores Table
CREATE TABLE IF NOT EXISTS scores (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    score_value INTEGER CHECK (score_value >= 0 AND score_value <= 100),
    risk_level VARCHAR(20),
    highway_proximity INTEGER,
    metro_proximity INTEGER,
    airport_proximity INTEGER,
    factory_proximity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Zone Events Table (Many-to-Many)
CREATE TABLE IF NOT EXISTS zone_events (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(zone_id, event_id)
);

-- 7. Users Table (for future authentication)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_zones_city_id ON zones(city_id);
CREATE INDEX IF NOT EXISTS idx_zones_geometry ON zones USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_scores_zone_id ON scores(zone_id);
CREATE INDEX IF NOT EXISTS idx_zone_events_zone_id ON zone_events(zone_id);
CREATE INDEX IF NOT EXISTS idx_zone_events_event_id ON zone_events(event_id);
CREATE INDEX IF NOT EXISTS idx_events_classification_id ON events(classification_id);
CREATE INDEX IF NOT EXISTS idx_events_event_date ON events(event_date);

-- Insert Sample Data

-- 1. Insert Cities
INSERT INTO cities (name, tier, region, latitude, longitude) VALUES
    ('Bangalore', 'Tier-1', 'South', 12.9716, 77.5946),
    ('Hyderabad', 'Tier-1', 'South', 17.3850, 78.4867),
    ('Bhubaneswar', 'Tier-2', 'East', 20.2961, 85.8245)
ON CONFLICT (name) DO NOTHING;

-- 2. Insert Event Classifications
INSERT INTO event_classifications (name, description) VALUES
    ('Highway Development', 'New highway projects and expansions'),
    ('Metro/Transit', 'Metro rail and public transport projects'),
    ('Airport Expansion', 'Airport development projects'),
    ('Industrial Zone', 'Factory and industrial parks'),
    ('Tech Hub', 'IT parks and tech developments')
ON CONFLICT (name) DO NOTHING;

-- 3. Insert Events
INSERT INTO events (title, description, location, event_date, source_url, source_name, classification_id)
VALUES
    (
        'Delhi-Mumbai Expressway Phase 2',
        'High-speed corridor connecting Delhi to Mumbai',
        'Delhi-Mumbai Corridor',
        '2026-06-15',
        'https://example.com/delhi-mumbai',
        'Economic Times',
        (SELECT id FROM event_classifications WHERE name = 'Highway Development')
    ),
    (
        'Bangalore Metro Phase 3',
        'Extension to Whitefield and Electronics City',
        'Bangalore',
        '2026-08-20',
        'https://example.com/bangalore-metro',
        'Moneycontrol',
        (SELECT id FROM event_classifications WHERE name = 'Metro/Transit')
    ),
    (
        'Hyderabad IT Park Expansion',
        'New tech park in Hitec City with 500K sq ft',
        'Hyderabad',
        '2026-05-10',
        'https://example.com/hyderabad-it',
        'PIB',
        (SELECT id FROM event_classifications WHERE name = 'Tech Hub')
    ),
    (
        'Bhubaneswar Airport Expansion',
        'New terminal addition',
        'Bhubaneswar',
        '2026-07-01',
        'https://example.com/bhubaneswar-airport',
        'Economic Times',
        (SELECT id FROM event_classifications WHERE name = 'Airport Expansion')
    ),
    (
        'Koramangala Tech Hub Development',
        'New startup ecosystem and incubation center',
        'Bangalore',
        '2026-09-15',
        'https://example.com/koramangala-tech',
        'Moneycontrol',
        (SELECT id FROM event_classifications WHERE name = 'Tech Hub')
    )
ON CONFLICT DO NOTHING;

-- 4. Insert Zones (with dummy polygon geometries - can be updated later)
-- For Bangalore
INSERT INTO zones (city_id, name, zone_type, description, geometry) VALUES
    (
        (SELECT id FROM cities WHERE name = 'Bangalore'),
        'Whitefield',
        'IT Zone',
        'Tech corridor near Bangalore',
        ST_GeomFromText('POLYGON((77.65 12.97, 77.70 12.97, 77.70 13.02, 77.65 13.02, 77.65 12.97))', 4326)
    ),
    (
        (SELECT id FROM cities WHERE name = 'Bangalore'),
        'Koramangala',
        'Startup Hub',
        'Trendy business and startup district',
        ST_GeomFromText('POLYGON((77.58 12.93, 77.63 12.93, 77.63 12.98, 77.58 12.98, 77.58 12.93))', 4326)
    ),
    (
        (SELECT id FROM cities WHERE name = 'Bangalore'),
        'Electronics City',
        'IT Zone',
        'Electronics manufacturing and IT hub',
        ST_GeomFromText('POLYGON((77.65 12.85, 77.70 12.85, 77.70 12.90, 77.65 12.90, 77.65 12.85))', 4326)
    )
ON CONFLICT (city_id, name) DO NOTHING;

-- For Hyderabad
INSERT INTO zones (city_id, name, zone_type, description, geometry) VALUES
    (
        (SELECT id FROM cities WHERE name = 'Hyderabad'),
        'Hitec City',
        'IT Zone',
        'Major IT hub in Hyderabad',
        ST_GeomFromText('POLYGON((78.38 17.36, 78.43 17.36, 78.43 17.41, 78.38 17.41, 78.38 17.36))', 4326)
    ),
    (
        (SELECT id FROM cities WHERE name = 'Hyderabad'),
        'Gachibowli',
        'Business District',
        'Corporate and business offices',
        ST_GeomFromText('POLYGON((78.34 17.44, 78.39 17.44, 78.39 17.49, 78.34 17.49, 78.34 17.44))', 4326)
    )
ON CONFLICT (city_id, name) DO NOTHING;

-- For Bhubaneswar
INSERT INTO zones (city_id, name, zone_type, description, geometry) VALUES
    (
        (SELECT id FROM cities WHERE name = 'Bhubaneswar'),
        'Nayapalli',
        'Business Zone',
        'Commercial and residential area',
        ST_GeomFromText('POLYGON((85.82 20.29, 85.87 20.29, 85.87 20.34, 85.82 20.34, 85.82 20.29))', 4326)
    ),
    (
        (SELECT id FROM cities WHERE name = 'Bhubaneswar'),
        'Chandrasekharpur',
        'IT Zone',
        'Tech park area',
        ST_GeomFromText('POLYGON((85.84 20.31, 85.89 20.31, 85.89 20.36, 85.84 20.36, 85.84 20.31))', 4326)
    )
ON CONFLICT (city_id, name) DO NOTHING;

-- 5. Insert Scores for each zone
INSERT INTO scores (zone_id, score_value, risk_level, highway_proximity, metro_proximity, airport_proximity, factory_proximity)
SELECT z.id, 78, 'GREEN', 30, 40, 0, 0
FROM zones z
WHERE z.name = 'Whitefield'
ON CONFLICT DO NOTHING;

INSERT INTO scores (zone_id, score_value, risk_level, highway_proximity, metro_proximity, airport_proximity, factory_proximity)
SELECT z.id, 62, 'YELLOW', 15, 40, 0, 20
FROM zones z
WHERE z.name = 'Koramangala'
ON CONFLICT DO NOTHING;

INSERT INTO scores (zone_id, score_value, risk_level, highway_proximity, metro_proximity, airport_proximity, factory_proximity)
SELECT z.id, 58, 'YELLOW', 25, 0, 40, 30
FROM zones z
WHERE z.name = 'Electronics City'
ON CONFLICT DO NOTHING;

INSERT INTO scores (zone_id, score_value, risk_level, highway_proximity, metro_proximity, airport_proximity, factory_proximity)
SELECT z.id, 85, 'GREEN', 0, 40, 15, 0
FROM zones z
WHERE z.name = 'Hitec City'
ON CONFLICT DO NOTHING;

INSERT INTO scores (zone_id, score_value, risk_level, highway_proximity, metro_proximity, airport_proximity, factory_proximity)
SELECT z.id, 68, 'YELLOW', 20, 40, 0, 0
FROM zones z
WHERE z.name = 'Gachibowli'
ON CONFLICT DO NOTHING;

INSERT INTO scores (zone_id, score_value, risk_level, highway_proximity, metro_proximity, airport_proximity, factory_proximity)
SELECT z.id, 52, 'YELLOW', 10, 0, 15, 25
FROM zones z
WHERE z.name = 'Nayapalli'
ON CONFLICT DO NOTHING;

INSERT INTO scores (zone_id, score_value, risk_level, highway_proximity, metro_proximity, airport_proximity, factory_proximity)
SELECT z.id, 38, 'RED', 5, 0, 30, 20
FROM zones z
WHERE z.name = 'Chandrasekharpur'
ON CONFLICT DO NOTHING;

-- 6. Link some events to zones
INSERT INTO zone_events (zone_id, event_id)
SELECT z.id, e.id
FROM zones z, events e
WHERE z.name = 'Whitefield' AND e.title LIKE '%Metro%'
ON CONFLICT DO NOTHING;

INSERT INTO zone_events (zone_id, event_id)
SELECT z.id, e.id
FROM zones z, events e
WHERE z.name = 'Koramangala' AND e.title LIKE '%Tech Hub%'
ON CONFLICT DO NOTHING;

INSERT INTO zone_events (zone_id, event_id)
SELECT z.id, e.id
FROM zones z, events e
WHERE z.name = 'Hitec City' AND e.title LIKE '%IT Park%'
ON CONFLICT DO NOTHING;

-- Verify tables were created
SELECT 'Tables created successfully!' as status;
SELECT 
    (SELECT COUNT(*) FROM cities) as city_count,
    (SELECT COUNT(*) FROM events) as event_count,
    (SELECT COUNT(*) FROM zones) as zone_count,
    (SELECT COUNT(*) FROM scores) as score_count;
