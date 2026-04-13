#!/usr/bin/env python
"""
Phase 3 Runner: NLP Extraction & Geocoding Pipeline
Processes scraped events with NLP and geocodes locations
"""
import sys
import os
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data_pipeline.orchestrator import DataPipelineOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Run Phase 3: NLP Extraction & Geocoding"""
    logger.info("=" * 60)
    logger.info("🚀 PHASE 3: NLP Extraction & Geocoding Pipeline")
    logger.info("=" * 60)
    
    try:
        orchestrator = DataPipelineOrchestrator()
        orchestrator.run()
        
        # Get statistics
        db = orchestrator.db
        from models.orm import Event
        
        total_events = db.query(Event).count()
        events_with_location = db.query(Event).filter(Event.location != None).count()
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 PIPELINE STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total events: {total_events}")
        logger.info(f"Events with locations: {events_with_location}")
        logger.info(f"Location extraction rate: {events_with_location}/{total_events} ({100*events_with_location//total_events if total_events > 0 else 0}%)")
        
        if events_with_location > 0:
            logger.info("\n✅ Sample geocoded events:")
            geocoded = db.query(Event).filter(Event.location != None).limit(5).all()
            for i, event in enumerate(geocoded, 1):
                logger.info(f"  {i}. {event.title[:50]}...")
                logger.info(f"     Location: {event.location}")
                logger.info(f"     Source: {event.source_name}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Phase 3 Complete!")
        logger.info("=" * 60)
        logger.info("\nNext: Phase 4 - Geospatial & Scoring Pipeline")
        
        return 0
    
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}", exc_info=True)
        return 1
    
    finally:
        if 'orchestrator' in locals():
            orchestrator.db.close()


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
