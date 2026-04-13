-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create cities table
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    state VARCHAR(100),
    region VARCHAR(100),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    tier VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    headline VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    source_url VARCHAR(500),
    source_name VARCHAR(100),
    published_date TIMESTAMP NOT NULL,
    fetched_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create event classifications table
CREATE TABLE event_classifications (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    event_type VARCHAR(50),  -- Highway, Metro, Airport, Factory, Government_Regulation
    status VARCHAR(50),      -- Proposed, Approved, Under_Construction, Completed
    extracted_location VARCHAR(200),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    confidence DECIMAL(3, 2),  -- 0.0 to 1.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create zones table (geospatial)
CREATE TABLE zones (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    shape GEOMETRY(Polygon, 4326) NOT NULL,
    center_point GEOMETRY(Point, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create scores table (scoring breakdown)
CREATE TABLE scores (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    growth_score INTEGER,  -- 0-100
    risk_level VARCHAR(20),  -- Green, Yellow, Red
    time_horizon VARCHAR(20),  -- 3-5yrs, 5-8yrs, 8-12yrs
    highway_score INTEGER DEFAULT 0,
    metro_score INTEGER DEFAULT 0,
    airport_score INTEGER DEFAULT 0,
    factory_score INTEGER DEFAULT 0,
    approved_bonus INTEGER DEFAULT 0,
    tier_bonus INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger events for zone score updates
CREATE TABLE zone_events (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    event_classification_id INTEGER NOT NULL REFERENCES event_classifications(id) ON DELETE CASCADE,
    relevance_score DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial indexes for performance
CREATE INDEX idx_zones_shape ON zones USING GIST(shape);
CREATE INDEX idx_zones_center ON zones USING GIST(center_point);
CREATE INDEX idx_event_classifications_geom ON event_classifications USING GIST(
    ST_Point(longitude, latitude)
);
CREATE INDEX idx_zones_city ON zones(city_id);
CREATE INDEX idx_scores_zone ON scores(zone_id);
CREATE INDEX idx_events_date ON events(published_date);
