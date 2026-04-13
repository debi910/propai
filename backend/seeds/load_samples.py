"""
Load sample data into database for demo
"""
import json
import sys
import logging
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, '.')

from models.database import SessionLocal, init_db
from models.orm import City, Event, EventClassification, Zone, Score
from geospatial.zone_generator import ZoneGenerator
from scoring.scorer import ScoringEngine

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_cities():
    """Load sample cities"""
    db = SessionLocal()
    
    cities_data = [
        {
            "name": "Bangalore",
            "region": "South India",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "tier": "Tier-1"
        },
        {
            "name": "Bhubaneswar",
            "region": "East India",
            "latitude": 20.2961,
            "longitude": 85.8245,
            "tier": "Tier-2"
        },
        {
            "name": "Hyderabad",
            "region": "South India",
            "latitude": 17.3850,
            "longitude": 78.4867,
            "tier": "Tier-1"
        }
    ]
    
    cities = []
    for city_data in cities_data:
        city = db.query(City).filter(City.name == city_data['name']).first()
        if not city:
            city = City(**city_data)
            db.add(city)
    
    db.commit()
    cities = db.query(City).all()
    logger.info(f"✅ Loaded {len(cities)} cities")
    return cities


def load_events():
    """Load sample events"""
    db = SessionLocal()
    
    events_data = [
        {
            "title": "Delhi-Mumbai Expressway Phase 2 Approved for Expansion",
            "description": "Ministry of Road Transport announces approval for Phase 2 with focus on Sector 45 in Gurgaon. Construction expected to begin Q2 2025.",
            "location": "Gurgaon",
            "source_name": "Economic Times",
            "source_url": "https://economictimes.indiatimes.com/event1",
            "event_date": "2025-10-15T10:30:00Z",
        },
        {
            "title": "Bangalore Metro Extension to Whitefield Approved",
            "description": "BMRCL approves 15 km metro extension to Whitefield IT corridor. Project funding secured. Expected operational by 2027.",
            "location": "Whitefield",
            "source_name": "Moneycontrol",
            "source_url": "https://www.moneycontrol.com/event2",
            "event_date": "2025-10-12T14:45:00Z",
        },
        {
            "title": "Major IT Park Coming to Hyderabad Hitec City",
            "description": "Tech Giant announces 500,000 sq ft office complex in Hyderabad Hitec City. Expected to create 5000+ jobs.",
            "location": "Hitec City",
            "source_name": "TOI",
            "source_url": "https://www.timesofindia.com/event3",
            "event_date": "2025-10-10T09:15:00Z",
        },
        {
            "title": "Bhubaneswar Airport Expansion Proposed",
            "description": "State government proposes expansion of Biju Patnaik International Airport to handle 5 million passengers annually.",
            "location": "Bhubaneswar",
            "source_name": "PIB",
            "source_url": "https://pib.gov.in/event4",
            "event_date": "2025-10-08T11:20:00Z",
        },
        {
            "title": "Koramangala Tech Hub Gets Government Support",
            "description": "Bangalore development authority allocates Rs 200 crore for infrastructure upgrade in Koramangala startup ecosystem.",
            "location": "Koramangala",
            "source_name": "Economic Times",
            "source_url": "https://economictimes.indiatimes.com/event5",
            "event_date": "2025-10-05T16:30:00Z",
        }
    ]
    
    events = []
    for event_data in events_data:
        event = db.query(Event).filter(Event.title == event_data['title']).first()
        if not event:
            event = Event(**event_data)
            db.add(event)
            events.append(event)
    
    db.commit()
    all_events = db.query(Event).all()
    logger.info(f"✅ Loaded {len(all_events)} events")
    return db.query(Event).all()


def load_zones_and_scores():
    """Load sample zones with GeoJSON and computed scores"""
    from geoalchemy2 import WKTElement
    db = SessionLocal()
    
    geojson_path = '../sample-data/zones.geojson'
    
    try:
        with open(geojson_path, 'r') as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        logger.warning(f"Sample zones file not found: {geojson_path}")
        return
    
    cities = {c.name: c for c in db.query(City).all()}
    
    for feature in geojson_data.get('features', []):
        props = feature['properties']
        city_name = props.get('city_name')
        geometry = feature.get('geometry')
        
        if not city_name or city_name not in cities:
            continue
        
        city = cities[city_name]
        zone_name = props.get('name')
        
        # Check if zone exists
        zone = db.query(Zone).filter(
            Zone.name == zone_name,
            Zone.city_id == city.id
        ).first()
        
        if not zone:
            # Convert GeoJSON geometry to WKT
            geom_wkt = None
            if geometry and geometry.get('type') == 'Polygon':
                coords = geometry['coordinates'][0]
                wkt_coords = ','.join([f"{lon} {lat}" for lon, lat in coords])
                geom_wkt = WKTElement(f"POLYGON(({wkt_coords}))", srid=4326)
            
            zone = Zone(
                city_id=city.id,
                name=zone_name,
                zone_type="Growth_Zone",
                description=props.get('description', ''),
                geometry=geom_wkt,
            )
            db.add(zone)
            db.flush()
        
        # Create or update score
        score = db.query(Score).filter(Score.zone_id == zone.id).first()
        if not score:
            score = Score(zone_id=zone.id)
            db.add(score)
        
        score.score_value = props.get('score_value', props.get('growth_score', 0))
        score.risk_level = props.get('risk_level', 'RED').upper()
        score.highway_proximity = props.get('highway_proximity', 0)
        score.metro_proximity = props.get('metro_proximity', 0)
        score.airport_proximity = props.get('airport_proximity', 0)
        score.factory_proximity = props.get('factory_proximity', 0)
    
    db.commit()
    all_zones = db.query(Zone).all()
    logger.info(f"✅ Loaded {len(all_zones)} zones with scores")


def main():
    """Main seed function"""
    logger.info("🌱 Starting database seed...")
    
    # Initialize database
    init_db()
    logger.info("✅ Database tables initialized")
    
    # Load data
    load_cities()
    load_events()
    load_zones_and_scores()
    
    logger.info("🎉 Database seeding complete!")
    
    # Verify
    db = SessionLocal()
    city_count = db.query(City).count()
    event_count = db.query(Event).count()
    zone_count = db.query(Zone).count()
    
    logger.info(f"📊 Final counts: {city_count} cities, {event_count} events, {zone_count} zones")


if __name__ == "__main__":
    main()
