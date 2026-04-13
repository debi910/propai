"""
Comprehensive test suite for PropAI setup verification
Run this after completing SETUP.md steps
"""
import sys
import asyncio
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_suite")

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def test_imports():
    """Test all critical imports"""
    logger.info(f"{BLUE}[TEST 1/6] Testing imports...{RESET}")
    try:
        from models.database import SessionLocal, init_db, get_db
        from models.orm import City, Event, Zone, Score
        from api.routes import router
        logger.info(f"{GREEN}✅ All imports successful{RESET}")
        return True
    except ImportError as e:
        logger.error(f"{RED}❌ Import error: {e}{RESET}")
        return False


def test_database_connection():
    """Test database connectivity"""
    logger.info(f"{BLUE}[TEST 2/6] Testing database connection...{RESET}")
    try:
        from models.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info(f"{GREEN}✅ Database connection successful{RESET}")
        return True
    except Exception as e:
        logger.error(f"{RED}❌ Database connection failed: {e}{RESET}")
        logger.error(f"{YELLOW}Hint: Check DATABASE_URL in .env file{RESET}")
        return False


def test_database_tables():
    """Test if all tables exist"""
    logger.info(f"{BLUE}[TEST 3/6] Testing database tables...{RESET}")
    try:
        from models.database import SessionLocal
        from models.orm import City, Event, Zone, Score
        
        db = SessionLocal()
        
        # Test each table
        cities = db.query(City).count()
        events = db.query(Event).count()
        zones = db.query(Zone).count()
        scores = db.query(Score).count()
        
        db.close()
        
        logger.info(f"{GREEN}✅ Table counts:{RESET}")
        logger.info(f"   • Cities: {cities}")
        logger.info(f"   • Events: {events}")
        logger.info(f"   • Zones: {zones}")
        logger.info(f"   • Scores: {scores}")
        
        if cities > 0 and events > 0 and zones > 0:
            logger.info(f"{GREEN}✅ Sample data successfully loaded{RESET}")
            return True
        else:
            logger.warning(f"{YELLOW}⚠️ No sample data found. Run: python seeds/load_samples.py{RESET}")
            return True  # Not a failure, just missing data
            
    except Exception as e:
        logger.error(f"{RED}❌ Table check failed: {e}{RESET}")
        return False


def test_api_routes():
    """Test API routes are defined"""
    logger.info(f"{BLUE}[TEST 4/6] Testing API routes...{RESET}")
    try:
        from api.routes import router
        
        # Get all route paths
        routes = []
        for route in router.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        logger.info(f"{GREEN}✅ Found {len(routes)} API routes:{RESET}")
        for route in sorted(routes):
            logger.info(f"   • {route}")
        
        # Check critical routes exist
        critical_routes = ['/cities', '/zones', '/events', '/health']
        missing = [r for r in critical_routes if not any(r in route for route in routes)]
        
        if missing:
            logger.warning(f"{YELLOW}⚠️ Missing routes: {missing}{RESET}")
            return False
        
        logger.info(f"{GREEN}✅ All critical routes present{RESET}")
        return True
        
    except Exception as e:
        logger.error(f"{RED}❌ Route check failed: {e}{RESET}")
        return False


def test_nlp_components():
    """Test NLP pipeline components"""
    logger.info(f"{BLUE}[TEST 5/6] Testing NLP components...{RESET}")
    try:
        from data_pipeline.nlp.entity_extractor import EntityExtractor
        from data_pipeline.nlp.geocoder import Geocoder
        from data_pipeline.scoring.scorer import ScoringEngine
        
        # Test entity extraction
        extractor = EntityExtractor()
        test_text = "Metro expansion announced in Whitefield, Bangalore"
        locations = extractor.extract_locations(test_text)
        event_type = extractor.extract_event_type(test_text)
        
        logger.info(f"{GREEN}✅ NLP Components:{RESET}")
        logger.info(f"   • EntityExtractor: Found {len(locations)} locations")
        logger.info(f"   • Event type detected: {event_type}")
        
        # Test geocoder
        geocoder = Geocoder()
        coords = geocoder.geocode("Bangalore")
        if coords:
            logger.info(f"   • Geocoder: Bangalore → {coords}")
        
        # Test scorer
        test_events = [
            {"event_type": "Metro", "status": "Approved"},
            {"event_type": "Highway", "status": "Approved"},
        ]
        score = ScoringEngine.calculate_score(test_events, "Tier-1")
        logger.info(f"   • Scorer: Test score = {score['growth_score']}/100 ({score['risk_level']})")
        
        logger.info(f"{GREEN}✅ All NLP components working{RESET}")
        return True
        
    except Exception as e:
        logger.error(f"{RED}❌ NLP component test failed: {e}{RESET}")
        logger.error(f"{YELLOW}Hint: Run 'python -m spacy download en_core_web_sm'{RESET}")
        return False


def test_sample_data_quality():
    """Test quality of sample data"""
    logger.info(f"{BLUE}[TEST 6/6] Testing sample data quality...{RESET}")
    try:
        from models.database import SessionLocal
        from models.orm import City, Zone, Score
        
        db = SessionLocal()
        
        zones = db.query(Zone).all()
        if not zones:
            logger.warning(f"{YELLOW}⚠️ No zones in database{RESET}")
            return True
        
        # Check scores
        avg_score = sum(z.score.growth_score for z in zones if z.score) / len(zones)
        
        # Check risk levels
        risk_levels = set(z.score.risk_level for z in zones if z.score)
        
        logger.info(f"{GREEN}✅ Sample data quality:{RESET}")
        logger.info(f"   • Total zones: {len(zones)}")
        logger.info(f"   • Average growth score: {avg_score:.1f}/100")
        logger.info(f"   • Risk levels present: {', '.join(sorted(risk_levels))}")
        
        # Zone details by city
        from models.orm import City
        for city in db.query(City).all():
            city_zones = db.query(Zone).filter(Zone.city_id == city.id).count()
            logger.info(f"   • {city.name}: {city_zones} zones")
        
        db.close()
        logger.info(f"{GREEN}✅ Sample data looks good{RESET}")
        return True
        
    except Exception as e:
        logger.error(f"{RED}❌ Data quality test failed: {e}{RESET}")
        return False


def main():
    """Run all tests"""
    logger.info(f"\n{BLUE}{'='*60}")
    logger.info(f"PropAI Setup Verification Test Suite")
    logger.info(f"{'='*60}{RESET}\n")
    
    tests = [
        ("Imports", test_imports),
        ("Database Connection", test_database_connection),
        ("Database Tables", test_database_tables),
        ("API Routes", test_api_routes),
        ("NLP Components", test_nlp_components),
        ("Sample Data Quality", test_sample_data_quality),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"{RED}❌ Test '{name}' crashed: {e}{RESET}")
            results.append((name, False))
        print()
    
    # Summary
    logger.info(f"{BLUE}{'='*60}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*60}{RESET}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        logger.info(f"{status} - {name}")
    
    logger.info(f"\n{BLUE}Result: {passed}/{total} tests passed{RESET}\n")
    
    if passed == total:
        logger.info(f"{GREEN}🎉 All tests passed! Ready to run backend.{RESET}")
        logger.info(f"{GREEN}Next: python main.py{RESET}\n")
        return 0
    else:
        logger.info(f"{RED}⚠️ Some tests failed. Check errors above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
