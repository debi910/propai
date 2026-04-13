"""
Base scraper class for news event extraction
"""
import logging
import sys
import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scraper implementations"""

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"scraper.{name}")

    @abstractmethod
    def fetch(self) -> List[Dict[str, str]]:
        """
        Fetch events from source
        Returns list of dicts with:
        - headline: str
        - content: str
        - source_url: str (optional)
        - published_date: str (ISO format)
        """
        pass

    def validate_event(self, event: Dict[str, str]) -> bool:
        """Validate event structure"""
        required_fields = ['headline', 'content', 'source_name', 'published_date']
        return all(field in event for field in required_fields)

    def log_event(self, event: Dict[str, str]):
        """Log event fetch"""
        self.logger.info(f"Found: {event['headline'][:60]}...")
