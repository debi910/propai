#!/usr/bin/env python
"""
Phase 2 Runner: Event Scraper Test
Fetches real news events and stores them in the database
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
    """Run Phase 2: Event scraper pipeline"""
    logger.info("=" * 60)
    logger.info("🚀 PHASE 2: Event Scraper Pipeline")
    logger.info("=" * 60)
    
    try:
        orchestrator = DataPipelineOrchestrator()
        orchestrator.run()
        
        # Get statistics
        db = orchestrator.db
        from models.orm import Event, City
        
        total_events = db.query(Event).count()
        cities = db.query(City).count()
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 PIPELINE STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total events in database: {total_events}")
        logger.info(f"Total cities: {cities}")
        
        if total_events > 0:
            logger.info("\n✅ Sample events:")
            sample_events = db.query(Event).limit(3).all()
            for i, event in enumerate(sample_events, 1):
                logger.info(f"  {i}. {event.title[:60]}...")
                logger.info(f"     Source: {event.source_name}")
                logger.info(f"     Location: {event.location or 'Not extracted'}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Phase 2 Complete!")
        logger.info("=" * 60)
        
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
