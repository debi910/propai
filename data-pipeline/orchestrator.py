"""
Main orchestrator for the data pipeline
Coordinates scraping, NLP processing, and storage
"""
import logging
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, '.')

from models.database import SessionLocal
from models.orm import Event, EventClassification

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class DataPipelineOrchestrator:
    """Orchestrates the full data pipeline"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.logger = logging.getLogger("orchestrator")
    
    def run(self):
        """Execute full pipeline: scrape -> NLP -> classify -> geocode -> store"""
        self.logger.info("🚀 Starting data pipeline orchestration...")
        
        try:
            # Step 1: Scrape events
            self.logger.info("📰 Step 1: Fetching events from sources...")
            self.step_scrape_events()
            
            # Step 2: NLP processing
            self.logger.info("🧠 Step 2: Processing with NLP...")
            self.step_nlp_processing()
            
            # Step 3: Geocoding
            self.logger.info("📍 Step 3: Geocoding locations...")
            self.step_geocoding()
            
            # Step 4: Zone generation
            self.logger.info("🗺️ Step 4: Generating growth zones...")
            self.step_zone_generation()
            
            # Step 5: Scoring
            self.logger.info("📊 Step 5: Computing growth scores...")
            self.step_scoring()
            
            self.logger.info("\n✅ Phase 4 Complete: Full pipeline executed!")
            
        except Exception as e:
            self.logger.error(f"❌ Pipeline error: {e}")
            raise
        finally:
            self.db.close()
    
    def step_scrape_events(self):
        """Fetch events from news sources"""
        from scrapers.rss_fetcher import RSSFetcher
        
        fetcher = RSSFetcher()
        events = fetcher.fetch(max_per_feed=15)
        
        # Store in database (avoid duplicates by source_url)
        added_count = 0
        for event_data in events:
            # Check if event already exists
            existing = self.db.query(Event).filter(
                Event.source_url == event_data.get("source_url")
            ).first()
            
            if not existing and event_data.get("source_url"):
                event = Event(**event_data)
                self.db.add(event)
                added_count += 1
        
        self.db.commit()
        self.logger.info(f"✅ Stored {added_count} new events from {len(events)} fetched")
    
    def step_nlp_processing(self):
        """Process events with NLP to extract entities and classify types"""
        from nlp.entity_extractor import EntityExtractor
        from models.orm import EventClassification
        
        extractor = EntityExtractor()
        
        # Find events without classifications
        events_without_classification = self.db.query(Event).filter(
            Event.classification_id == None
        ).all()
        
        if not events_without_classification:
            self.logger.info("✅ All events already classified")
            return
        
        for event in events_without_classification:
            try:
                # Combine title and description for extraction
                text = f"{event.title} {event.description or ''}"
                
                # Extract entities
                locations = extractor.extract_locations(text)
                organizations = extractor.extract_organizations(text)
                
                # Extract event type and status
                event_type = extractor.extract_event_type(text)
                
                # Check if classification exists, otherwise create it
                classification = self.db.query(EventClassification).filter(
                    EventClassification.name == event_type
                ).first()
                
                if not classification:
                    extracted_location = locations[0].text if locations else event.location
                    classification = EventClassification(
                        name=event_type,
                        description=f"Extracted location: {extracted_location}"
                    )
                    self.db.add(classification)
                    self.db.flush()  # Flush to get the ID
                
                # Update event with extracted location and classification
                event.location = locations[0].text if locations else event.location
                event.classification_id = classification.id
                
            except Exception as e:
                self.logger.warning(f"Error processing event {event.id}: {e}")
                continue
        
        self.db.commit()
        self.logger.info(f"✅ Classified {len(events_without_classification)} events with NLP")
    
    def step_geocoding(self):
        """Geocode extracted locations to coordinates"""
        from nlp.geocoder import Geocoder
        
        geocoder = Geocoder()
        
        # Find events with locations but without coordinates
        events = self.db.query(Event).filter(
            Event.location != None
        ).all()
        
        if not events:
            self.logger.info("⏂ No events to geocode")
            return
        
        geocoded_count = 0
        for event in events:
            try:
                if event.location:
                    coords = geocoder.geocode(event.location)
                    if coords:
                        # Coordinates will be used in Phase 4 for zone mapping
                        # Store in a simple tuple format for now
                        self.logger.debug(f"✓ Geocoded {event.location}: {coords}")
                        geocoded_count += 1
            
            except Exception as e:
                self.logger.debug(f"Geocoding error for {event.location}: {e}")
                continue
        
        self.db.commit()
        self.logger.info(f"✅ Geocoded {geocoded_count}/{len(events)} events")
    
    def step_zone_generation(self):
        """Generate growth zones from geocoded events"""
        from geospatial.zone_generator import ZoneGenerator
        from models.orm import Zone as ZoneModel, City, Event
        from geoalchemy2 import WKTElement
        
        generator = ZoneGenerator()
        
        # Get all events with locations and coordinates
        events_with_locations = self.db.query(Event).filter(
            Event.location != None
        ).all()
        
        if not events_with_locations:
            self.logger.info("⏂ No events with locations for zone generation")
            return
        
        zone_count = 0
        
        # Group events by location/city
        locations_map = {}
        for event in events_with_locations:
            if event.location:
                if event.location not in locations_map:
                    locations_map[event.location] = []
                locations_map[event.location].append(event)
        
        # Create zones for each location
        for location, location_events in locations_map.items():
            try:
                # Get first event's city
                city = None
                for city_obj in self.db.query(City).all():
                    if city_obj.name.lower() in location.lower() or location.lower() in city_obj.name.lower():
                        city = city_obj
                        break
                
                if not city:
                    # Skip if city not found
                    continue
                
                # Generate zone geometry
                # Use coordinates of first event or city center
                center_lat = city.latitude
                center_lon = city.longitude
                
                # Create polygon for the zone
                polygon_geojson = generator.create_zone_polygon(
                    location,
                    location_events[0].location or "Unknown",
                    center_lat,
                    center_lon
                )
                
                # Convert to WKT for PostGIS
                ring = polygon_geojson['coordinates'][0]
                wkt_coords = ','.join([f"{lon} {lat}" for lon, lat in ring])
                wkt = f"POLYGON(({wkt_coords}))"
                geometry = WKTElement(wkt, srid=4326)
                
                # Check if zone already exists
                existing_zone = self.db.query(ZoneModel).filter(
                    ZoneModel.city_id == city.id,
                    ZoneModel.name == location
                ).first()
                
                if not existing_zone:
                    zone = ZoneModel(
                        city_id=city.id,
                        name=location,
                        zone_type="Growth_Zone",
                        description=f"Infrastructure zone: {location}",
                        geometry=geometry
                    )
                    self.db.add(zone)
                    zone_count += 1
            
            except Exception as e:
                self.logger.warning(f"Error creating zone for {location}: {e}")
                continue
        
        self.db.commit()
        self.logger.info(f"✅ Generated {zone_count} zones")
    
    def step_scoring(self):
        """Compute growth scores for zones based on events"""
        from scoring.scorer import ScoringEngine
        from models.orm import Zone as ZoneModel, Score, Event
        
        scorer = ScoringEngine()
        
        # Get all zones
        zones = self.db.query(ZoneModel).all()
        
        if not zones:
            self.logger.info("⏂ No zones to score")
            return
        
        scored_count = 0
        
        for zone in zones:
            try:
                # Find events in this zone's location
                events = self.db.query(Event).filter(
                    Event.location == zone.name
                ).all()
                
                if not events:
                    continue
                
                # Convert events to scoring format
                event_dicts = [
                    {
                        "event_type": "Unknown",  # Would extract from classification
                        "status": "Proposed"  # Would extract from classification
                    }
                    for _ in events
                ]
                
                # Calculate score
                city_tier = zone.city.tier if zone.city else "Tier-2"
                score_result = scorer.calculate_score(event_dicts, city_tier)
                
                # Check if score already exists
                existing_score = self.db.query(Score).filter(
                    Score.zone_id == zone.id
                ).first()
                
                if not existing_score:
                    score = Score(
                        zone_id=zone.id,
                        score_value=score_result['growth_score'],
                        risk_level=score_result['risk_level'],
                        highway_proximity=0,
                        metro_proximity=0,
                        airport_proximity=0,
                        factory_proximity=0
                    )
                    self.db.add(score)
                    scored_count += 1
            
            except Exception as e:
                self.logger.debug(f"Error scoring zone {zone.name}: {e}")
                continue
        
        self.db.commit()
        self.logger.info(f"✅ Computed scores for {scored_count} zones")


if __name__ == "__main__":
    orchestrator = DataPipelineOrchestrator()
    orchestrator.run()
