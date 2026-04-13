"""
Geospatial zone generation using PostGIS
Creates zone polygons based on infrastructure event locations
"""
import logging
import sys
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

logger = logging.getLogger(__name__)


@dataclass
class Zone:
    """Represents a growth zone"""
    name: str
    event_type: str
    center_lat: float
    center_lon: float
    buffer_km: float


class ZoneGenerator:
    """Generate zones from infrastructure events"""

    # Buffer distances (in km) for different infrastructure types
    BUFFER_DISTANCES = {
        "Highway": 2.0,  # 2km corridor
        "Metro": 1.5,    # 1.5km around metro stations
        "Airport": 3.0,  # 3km around airport
        "Factory": 1.0,  # 1km industrial area
        "Government_Regulation": 2.0,
    }

    @staticmethod
    def km_to_degrees(km: float, latitude: float = 20.0) -> float:
        """
        Approximate conversion: km to degrees
        At equator: 1 degree ≈ 111 km
        At higher latitudes: adjusted by cos(latitude)
        India is between 8-35°N
        """
        import math
        lat_rad = math.radians(latitude)
        return km / (111.0 * math.cos(lat_rad))

    @classmethod
    def create_zone_polygon(
        cls,
        location_name: str,
        event_type: str,
        center_lat: float,
        center_lon: float,
    ) -> Dict:
        """
        Create a zone polygon (GeoJSON) from center point and event type
        Returns GeoJSON polygon geometry
        """
        buffer_km = cls.BUFFER_DISTANCES.get(event_type, 1.0)
        buffer_deg = cls.km_to_degrees(buffer_km, center_lat)

        # Create simple bounding box polygon (square)
        # Real implementation would use ST_Buffer in PostGIS
        coords = [
            [center_lon - buffer_deg, center_lat - buffer_deg],
            [center_lon + buffer_deg, center_lat - buffer_deg],
            [center_lon + buffer_deg, center_lat + buffer_deg],
            [center_lon - buffer_deg, center_lat + buffer_deg],
            [center_lon - buffer_deg, center_lat - buffer_deg],  # Close polygon
        ]

        return {
            "type": "Polygon",
            "coordinates": [coords],
        }

    @staticmethod
    def merge_overlapping_zones(zones: List[Dict]) -> List[Dict]:
        """
        Merge zones that overlap significantly
        For MVP, simple implementation - clusters zones within 1km
        """
        # This would use PostGIS ST_Union in production
        # For now, return as-is
        return zones


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    generator = ZoneGenerator()

    # Test zone creation
    zone_geom = generator.create_zone_polygon(
        "Whitefield",
        "Metro",
        12.9698,
        77.7499,
    )

    print(f"Zone geometry: {zone_geom}")
