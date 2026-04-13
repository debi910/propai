"""
RSS Feed scraper for Indian news sources about real estate & infrastructure
"""
import feedparser
import logging
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
from base_scraper import BaseScraper

logger = logging.getLogger(__name__)

# Target RSS feeds (free, legal, real estate & infrastructure focused)
RSS_FEEDS = {
    "Economic Times - Real Estate": "https://economictimes.indiatimes.com/rss/realty.cms",
    "Moneycontrol - Infrastructure": "https://www.moneycontrol.com/rss/moneycontrol_infra.xml",
    "TOI - Delhi": "https://timesofindia.indiatimes.com/delhi/rss.cms",
    "TOI - Mumbai": "https://timesofindia.indiatimes.com/rssfeedsindex.cms?feedtype=citynews&feed=mumbai",
    "TOI - Bangalore": "https://timesofindia.indiatimes.com/rssfeedsindex.cms?feedtype=citynews&feed=bangalore",
}

# Infrastructure keywords to filter events
INFRASTRUCTURE_KEYWORDS = [
    "metro", "highway", "airport", "railway", "infrastructure",
    "road", "bridge", "expansion", "development", "project",
    "construction", "approved", "announced", "government",
    "transit", "corridor", "expressway", "industrial zone", "tech park",
    "real estate", "property", "commercial", "residential", "investment",
]

# Exclude keywords (reduces noise)
EXCLUDE_KEYWORDS = [
    "movie", "film", "entertainment", "celebrity", "sports",
    "fashion", "health", "medical", "lawsuit", "court",
]


class RSSFetcher(BaseScraper):
    """Fetch events from RSS feeds"""

    def __init__(self):
        super().__init__("rss_fetcher")
        self.feeds = RSS_FEEDS

    def fetch(self, max_per_feed: int = 15) -> List[Dict[str, str]]:
        """Fetch all events from configured RSS feeds with retry logic"""
        events = []
        
        for source_name, feed_url in self.feeds.items():
            try:
                self.logger.info(f"📡 Fetching from {source_name}...")
                
                # Add timeout for better error handling
                feed = feedparser.parse(feed_url, timeout=10)
                
                if feed.bozo:
                    self.logger.warning(f"⚠️ Feed issue for {source_name}")
                
                entries = feed.entries[:max_per_feed]
                matched = 0
                
                for entry in entries:
                    # Extract and filter by keywords
                    title = entry.get("title", "").lower()
                    summary = entry.get("summary", "").lower()
                    text_combined = f"{title} {summary}"
                    
                    # Skip excluded keywords first
                    if any(kw in text_combined for kw in EXCLUDE_KEYWORDS):
                        continue
                    
                    # Check for infrastructure keywords
                    if not any(kw in text_combined for kw in INFRASTRUCTURE_KEYWORDS):
                        continue
                    
                    try:
                        # Parse publication date
                        pub_datetime = self._parse_date(entry.get("published", ""))
                        
                        event = {
                            "title": entry.get("title", ""),
                            "description": self._clean_html(entry.get("summary", "")),
                            "location": self._extract_location(entry.get("title", "")),
                            "event_date": pub_datetime.date() if pub_datetime else None,
                            "source_url": entry.get("link", ""),
                            "source_name": source_name,
                        }
                        
                        if self.validate_event(event):
                            events.append(event)
                            matched += 1
                    
                    except Exception as e:
                        self.logger.debug(f"Error parsing entry: {e}")
                        continue
                
                self.logger.info(f"✅ Found {matched} relevant events from {source_name}")
                time.sleep(1)  # Rate limiting
            
            except Exception as e:
                self.logger.error(f"❌ Error fetching {source_name}: {e}")
                continue
        
        self.logger.info(f"\n🎯 Total events fetched: {len(events)}")
        return events
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse publication date from various formats"""
        if not date_str:
            return datetime.utcnow()
        
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except:
            return datetime.utcnow()
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()[:500]
    
    def _extract_location(self, title: str) -> Optional[str]:
        """Extract location mention from title"""
        # Simple location extraction - can be enhanced with NLP
        cities = ["Bangalore", "Bengaluru", "Hyderabad", "Mumbai", "Delhi",
                  "Chennai", "Pune", "Kolkata", "Jaipur", "Bhubaneswar",
                  "Ahmedabad", "Lucknow", "Indore", "Coimbatore"]
        
        for city in cities:
            if city.lower() in title.lower():
                return city
        
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetcher = RSSFetcher()
    events = fetcher.fetch()
    print(f"Fetched {len(events)} events")
    for event in events[:3]:
        print(f"- {event['headline']}")
