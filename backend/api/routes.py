"""
API routes for PropAI
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.functions import ST_AsGeoJSON
import logging

from models.database import get_db
from models.orm import City, Zone, Event, Score, EventClassification, ZoneEvent

router = APIRouter()
logger = logging.getLogger(__name__)


# ============================================================================
# CITY ENDPOINTS
# ============================================================================


@router.get("/cities", tags=["cities"])
async def get_cities(db: Session = Depends(get_db)):
    """Get all cities with zone statistics"""
    try:
        cities = db.query(City).all()
        result = []
        for city in cities:
            zone_count = db.query(func.count(Zone.id)).filter(
                Zone.city_id == city.id
            ).scalar()
            result.append({
                "id": city.id,
                "name": city.name,
                "region": city.region,
                "latitude": float(city.latitude) if city.latitude else None,
                "longitude": float(city.longitude) if city.longitude else None,
                "tier": city.tier,
                "zone_count": zone_count or 0,
            })
        return result
    except Exception as e:
        logger.error(f"Error fetching cities: {e}")
        raise HTTPException(status_code=500, detail="Error fetching cities")


@router.get("/cities/{city_name}", tags=["cities"])
async def get_city_insights(city_name: str, db: Session = Depends(get_db)):
    """Get city insights with zone statistics"""
    try:
        city = db.query(City).filter(City.name.ilike(city_name)).first()
        if not city:
            raise HTTPException(status_code=404, detail="City not found")

        zones = db.query(Zone).filter(Zone.city_id == city.id).all()
        
        # Calculate statistics
        green_zones = db.query(func.count(Zone.id)).join(Score).filter(
            Zone.city_id == city.id,
            Score.risk_level == "GREEN"
        ).scalar()
        yellow_zones = db.query(func.count(Zone.id)).join(Score).filter(
            Zone.city_id == city.id,
            Score.risk_level == "YELLOW"
        ).scalar()
        red_zones = db.query(func.count(Zone.id)).join(Score).filter(
            Zone.city_id == city.id,
            Score.risk_level == "RED"
        ).scalar()

        avg_score = db.query(func.avg(Score.score_value)).join(Zone).filter(
            Zone.city_id == city.id
        ).scalar() or 0

        return {
            "id": city.id,
            "name": city.name,
            "tier": city.tier,
            "region": city.region,
            "latitude": float(city.latitude) if city.latitude else None,
            "longitude": float(city.longitude) if city.longitude else None,
            "zone_count": len(zones),
            "green_zones": green_zones or 0,
            "yellow_zones": yellow_zones or 0,
            "red_zones": red_zones or 0,
            "average_score": round(float(avg_score), 2),
            "zones": [
                {
                    "id": z.id,
                    "name": z.name,
                    "zone_type": z.zone_type,
                    "description": z.description,
                }
                for z in zones
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching city insights: {e}")
        raise HTTPException(status_code=500, detail="Error fetching city insights")


# ============================================================================
# ZONE ENDPOINTS
# ============================================================================


@router.get("/zones", tags=["zones"])
async def get_zones(
    city_id: int = Query(None),
    risk_level: str = Query(None),
    score_min: int = Query(0),
    score_max: int = Query(100),
    db: Session = Depends(get_db),
):
    """Get all zones with optional filters"""
    try:
        query = db.query(Zone).outerjoin(Score)

        if city_id:
            query = query.filter(Zone.city_id == city_id)
        if risk_level:
            query = query.filter(Score.risk_level == risk_level.upper())
        
        query = query.filter(
            (Score.score_value >= score_min) | (Score.score_value == None),
            (Score.score_value <= score_max) | (Score.score_value == None)
        )

        zones = query.all()

        result = []
        for zone in zones:
            # Get first score if exists
            score = zone.scores[0] if zone.scores else None
            result.append({
                "id": zone.id,
                "city_id": zone.city_id,
                "name": zone.name,
                "zone_type": zone.zone_type,
                "description": zone.description,
                "score_value": score.score_value if score else 0,
                "risk_level": score.risk_level if score else "UNKNOWN",
            })

        return result
    except Exception as e:
        logger.error(f"Error fetching zones: {e}")
        raise HTTPException(status_code=500, detail="Error fetching zones")


@router.get("/zones/{zone_id}", tags=["zones"])
async def get_zone_details(zone_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific zone"""
    try:
        zone = db.query(Zone).filter(Zone.id == zone_id).first()
        if not zone:
            raise HTTPException(status_code=404, detail="Zone not found")

        score = zone.scores[0] if zone.scores else None
        city = zone.city

        return {
            "id": zone.id,
            "name": zone.name,
            "zone_type": zone.zone_type,
            "description": zone.description,
            "city_name": city.name,
            "city_id": city.id,
            "score_value": score.score_value if score else 0,
            "risk_level": score.risk_level if score else "UNKNOWN",
            "highway_proximity": score.highway_proximity if score else 0,
            "metro_proximity": score.metro_proximity if score else 0,
            "airport_proximity": score.airport_proximity if score else 0,
            "factory_proximity": score.factory_proximity if score else 0,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching zone details: {e}")
        raise HTTPException(status_code=500, detail="Error fetching zone details")


# ============================================================================
# EVENT ENDPOINTS
# ============================================================================


@router.get("/events", tags=["events"])
async def get_events(
    city_id: int = Query(None),
    event_type: str = Query(None),
    skip: int = Query(0),
    limit: int = Query(20),
    db: Session = Depends(get_db),
):
    """Get events with optional filters and pagination"""
    try:
        query = db.query(Event)

        if city_id:
            # Filter by city through zone_events
            query = query.join(ZoneEvent).join(Zone).filter(
                Zone.city_id == city_id
            ).distinct()

        if event_type:
            query = query.join(EventClassification).filter(
                EventClassification.name == event_type
            ).distinct()

        query = query.order_by(Event.event_date.desc())
        total = query.count()
        events = query.offset(skip).limit(limit).all()

        result = []
        for event in events:
            desc_preview = event.description[:200] + "..." if len(event.description) > 200 else event.description
            result.append({
                "id": event.id,
                "title": event.title,
                "description": desc_preview,
                "location": event.location,
                "source_name": event.source_name,
                "source_url": event.source_url,
                "event_date": event.event_date.isoformat() if event.event_date else None,
                "classification": event.classification.name if event.classification else None,
            })

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "events": result,
        }
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        raise HTTPException(status_code=500, detail="Error fetching events")


@router.get("/events/{event_id}", tags=["events"])
async def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific event"""
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # Get zones related to this event
        zones = db.query(Zone).join(ZoneEvent).filter(
            ZoneEvent.event_id == event_id
        ).all()

        return {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "location": event.location,
            "source_name": event.source_name,
            "source_url": event.source_url,
            "event_date": event.event_date.isoformat() if event.event_date else None,
            "classification": event.classification.name if event.classification else None,
            "zones": [
                {
                    "id": z.id,
                    "name": z.name,
                    "zone_type": z.zone_type,
                }
                for z in zones
            ],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching event details: {e}")
        raise HTTPException(status_code=500, detail="Error fetching event details")


# ============================================================================
# MAP DATA ENDPOINT
# ============================================================================


@router.get("/map/data", tags=["map"])
async def get_map_data(city_id: int = Query(None), db: Session = Depends(get_db)):
    """Get GeoJSON data optimized for map rendering"""
    try:
        query = db.query(Zone).outerjoin(Score)

        if city_id:
            query = query.filter(Zone.city_id == city_id)

        zones = query.all()

        features = []
        for zone in zones:
            score = zone.scores[0] if zone.scores else None
            risk_color_map = {
                "GREEN": "#10b981",
                "YELLOW": "#f59e0b",
                "RED": "#ef4444",
            }

            features.append({
                "type": "Feature",
                "id": zone.id,
                "geometry": zone.geometry if zone.geometry else {"type": "Polygon", "coordinates": []},
                "properties": {
                    "id": zone.id,
                    "name": zone.name,
                    "zone_type": zone.zone_type,
                    "description": zone.description,
                    "city_id": zone.city_id,
                    "score_value": score.score_value if score else 0,
                    "risk_level": score.risk_level if score else "UNKNOWN",
                    "highway_proximity": score.highway_proximity if score else 0,
                    "metro_proximity": score.metro_proximity if score else 0,
                    "airport_proximity": score.airport_proximity if score else 0,
                    "factory_proximity": score.factory_proximity if score else 0,
                    "color": risk_color_map.get(score.risk_level if score else "RED", "#ef4444"),
                },
            })

        return {
            "type": "FeatureCollection",
            "features": features,
        }
    except Exception as e:
        logger.error(f"Error fetching map data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching map data")
