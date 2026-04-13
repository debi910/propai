"""
NLP-based entity extraction using spaCy
Extracts locations, event types, and status from news text
"""
import spacy
import logging
import sys
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

logger = logging.getLogger(__name__)


@dataclass
class ExtractedEntity:
    """Represents an extracted entity"""
    text: str
    type: str
    confidence: float = 1.0


class EntityExtractor:
    """Extract locations and entities from news text"""

    # Hardcoded Indian locations for initial version
    INDIAN_CITIES = {
        # Tier 1
        "bangalore": {"region": "South", "tier": "Tier-1"},
        "bengaluru": {"region": "South", "tier": "Tier-1"},
        "hyderabad": {"region": "South", "tier": "Tier-1"},
        "delhi": {"region": "North", "tier": "Tier-1"},
        "mumbai": {"region": "West", "tier": "Tier-1"},
        "pune": {"region": "West", "tier": "Tier-1"},
        "pune": {"region": "West", "tier": "Tier-1"},
        "gurgaon": {"region": "North", "tier": "Tier-2"},
        "noida": {"region": "North", "tier": "Tier-2"},
        "bhubaneswar": {"region": "East", "tier": "Tier-2"},
        # Neighborhoods
        "whitefield": {"parent_city": "bangalore"},
        "koramangala": {"parent_city": "bangalore"},
        "indiranagar": {"parent_city": "bangalore"},
        "sector 45": {"parent_city": "gurgaon"},
        "hitec city": {"parent_city": "hyderabad"},
        "gachibowli": {"parent_city": "hyderabad"},
        "nayapalli": {"parent_city": "bhubaneswar"},
        "chandrasekharpur": {"parent_city": "bhubaneswar"},
    }

    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.error("spacy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None

    def extract_locations(self, text: str) -> List[ExtractedEntity]:
        """Extract location mentions from text"""
        if not self.nlp:
            return []

        locations = []
        doc = self.nlp(text)

        # Use spaCy NER
        for ent in doc.ents:
            if ent.label_ == "GPE":  # Geopolitical entity
                normalized = ent.text.lower()
                if normalized in self.INDIAN_CITIES:
                    locations.append(
                        ExtractedEntity(text=ent.text, type="LOCATION", confidence=0.9)
                    )

        # Also check for hardcoded locations
        text_lower = text.lower()
        for location, info in self.INDIAN_CITIES.items():
            if location in text_lower and location not in [l.text.lower() for l in locations]:
                locations.append(
                    ExtractedEntity(text=location.title(), type="LOCATION", confidence=0.8)
                )

        return locations

    def extract_organizations(self, text: str) -> List[ExtractedEntity]:
        """Extract organization mentions"""
        if not self.nlp:
            return []

        orgs = []
        doc = self.nlp(text)

        for ent in doc.ents:
            if ent.label_ == "ORG":
                orgs.append(ExtractedEntity(text=ent.text, type="ORGANIZATION", confidence=0.9))

        return orgs

    @staticmethod
    def extract_event_type(text: str) -> str:
        """Classify event type based on keywords"""
        text_lower = text.lower()

        event_keywords = {
            "Highway": ["highway", "expressway", "road", "corridor"],
            "Metro": ["metro", "subway", "rail", "transit"],
            "Airport": ["airport", "aviation", "terminal"],
            "Factory": ["factory", "plant", "industrial", "manufacturing", "office"],
            "Government_Regulation": ["government", "regulation", "policy", "approval", "ministry"],
        }

        for event_type, keywords in event_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return event_type

        return "Unknown"

    @staticmethod
    def extract_status(text: str) -> str:
        """Extract project status from text"""
        text_lower = text.lower()

        status_keywords = {
            "Approved": ["approved", "sanctioned", "cleared", "green light"],
            "Proposed": ["proposed", "planned", "proposed", "announced"],
            "Under_Construction": ["construction", "ongoing", "under way", "being built"],
            "Completed": ["completed", "finished", "operational", "launched"],
        }

        for status, keywords in status_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return status

        return "Proposed"  # Default


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extractor = EntityExtractor()

    test_text = """
    Delhi-Mumbai Expressway Phase 2 approved for expansion in Sector 45, Gurgaon.
    Construction expected to begin Q2 2025. Ministry announces new government policy.
    """

    locations = extractor.extract_locations(test_text)
    print(f"Locations: {[str(loc.text) for loc in locations]}")

    event_type = extractor.extract_event_type(test_text)
    print(f"Event Type: {event_type}")

    status = extractor.extract_status(test_text)
    print(f"Status: {status}")
