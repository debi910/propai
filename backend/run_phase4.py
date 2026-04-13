#!/usr/bin/env python
"""
Phase 4 Runner: Geospatial & Scoring Pipeline
Generates growth zones and computes risk scores
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
    """Run Phase 4: Geospatial & Scoring Pipeline"""
    logger.info("=" * 60)
    logger.info("🚀 PHASE 4: Geospatial & Scoring Pipeline")
    logger.info("=" * 60)
    
    try:
        orchestrator = DataPipelineOrchestrator()
        orchestrator.run()
        
        # Get statistics
        db = orchestrator.db
        from models.orm import Zone, Score
        
        total_zones = db.query(Zone).count()
        scored_zones = db.query(Score).count()
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 PIPELINE STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total zones: {total_zones}")
        logger.info(f"Zones with scores: {scored_zones}")
        
        if scored_zones > 0:
            logger.info("\n✅ Growth score summary:")
            
            # Get summary stats
            from sqlalchemy import func
            score_dist = db.query(
                Score.risk_level,
                func.count(Score.id).label('count')
            ).group_by(Score.risk_level).all()
            
            for risk_level, count in score_dist:
                logger.info(f"  - {risk_level}: {count} zones")
            
            # Show top zones
            logger.info("\n📈 Top growth zones:")
            top_zones = db.query(Zone, Score).join(
                Score, Zone.id == Score.zone_id
            ).order_by(Score.score_value.desc()).limit(5).all()
            
            for i, (zone, score) in enumerate(top_zones, 1):
                logger.info(f"  {i}. {zone.name} - Score: {score.score_value} ({score.risk_level})")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Phase 4 Complete!")
        logger.info("=" * 60)
        logger.info("\nFull pipeline ready for deployment!")
        
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
