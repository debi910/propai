"""
Geocoding: Convert location names to lat/long using geopy + Nominatim
"""
import logging
import sys
import os
from typing import Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderQueryError

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

logger = logging.getLogger(__name__)


class Geocoder:
    """Convert location names to coordinates"""

    # Hardcoded major Indian city coordinates
    CITY_COORDINATES = {
        "bangalore": (12.9716, 77.5946),
        "bengaluru": (12.9716, 77.5946),
        "hyderabad": (17.3850, 78.4867),
        "delhi": (28.7041, 77.1025),
        "mumbai": (19.0760, 72.8777),
        "pune": (18.5204, 73.8567),
        "gurgaon": (28.4595, 77.0266),
        "noida": (28.5355, 77.3910),
        "bhubaneswar": (20.2961, 85.8245),
        # Neighborhoods
        "whitefield": (12.9698, 77.7499),
        "koramangala": (12.9352, 77.6245),
        "electronics city": (12.8387, 77.6784),
        "indiranagar": (12.9716, 77.6412),
        "sector 45": (28.4745, 77.1239),
        "hitec city": (17.3604, 78.3489),
        "gachibowli": (17.4500, 78.3472),
        "nayapalli": (20.2961, 85.8245),
        "chandrasekharpur": (20.2857, 85.8332),
    }

    def __init__(self):
        try:
            self.nominatim = Nominatim(user_agent="propai_geocoder")
            self.logger = logging.getLogger("geocoder")
        except Exception as e:
            self.logger.warning(f"Nominatim initialization warning: {e}")
            self.nominatim = None

    def geocode(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Convert location name to (latitude, longitude)
        Returns None if location not found
        """
        # Try hardcoded locations first (faster, no API call)
        location_lower = location.lower().strip()
        if location_lower in self.CITY_COORDINATES:
            return self.CITY_COORDINATES[location_lower]

        # Try partial match for neighborhoods
        for city, coords in self.CITY_COORDINATES.items():
            if city in location_lower:
                return coords

        # Fallback to Nominatim API (rate limited: 1 req/sec)
        if not self.nominatim:
            return None

        try:
            # Add "India" to ensure Indian locations
            search_query = f"{location}, India"
            result = self.nominatim.geocode(search_query, timeout=10)

            if result:
                return (result.latitude, result.longitude)
        except GeocoderTimedOut:
            self.logger.warning(f"Geocoder timed out for {location}")
        except GeocoderQueryError as e:
            self.logger.debug(f"Geocoder query error for {location}: {e}")
        except Exception as e:
            self.logger.warning(f"Geocoding error for {location}: {e}")

        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    geocoder = Geocoder()

    test_locations = ["Whitefield, Bangalore", "Hitec City", "Sector 45"]

    for loc in test_locations:
        coords = geocoder.geocode(loc)
        print(f"{loc}: {coords}")
