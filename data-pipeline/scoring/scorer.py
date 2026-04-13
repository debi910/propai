"""
Rule-based scoring engine
Calculates growth scores for zones based on infrastructure events
"""
import logging
import sys
import os
from typing import Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

logger = logging.getLogger(__name__)


class ScoringEngine:
    """Calculate zone growth scores and risk levels"""

    # Scoring weights for different infrastructure types
    EVENT_WEIGHTS = {
        "Highway": 30,
        "Metro": 40,
        "Airport": 15,
        "Factory": 25,
        "Government_Regulation": 10,
    }

    # Status bonuses
    STATUS_WEIGHTS = {
        "Approved": 20,
        "Under_Construction": 15,
        "Proposed": 5,
        "Completed": 25,
    }

    # Tier bonuses
    TIER_BONUS = {
        "Tier-1": 10,
        "Tier-2": 5,
        "Tier-3": 0,
    }

    @classmethod
    def calculate_score(
        cls,
        events: List[Dict],
        city_tier: str = "Tier-2",
    ) -> Dict:
        """
        Calculate growth score (0-100) from events
        
        Args:
            events: List of classified events affecting the zone
            city_tier: Tier of the city
        
        Returns:
            Dict with:
            - growth_score: 0-100
            - risk_level: Green/Yellow/Red
            - time_horizon: 3-5yrs/5-8yrs/8-12yrs
            - breakdown: dict of individual scores
        """
        score = 0
        breakdown = {
            "event_scores": {},
            "status_bonus": 0,
            "tier_bonus": 0,
            "total": 0,
        }

        # Sum event type weights
        for event in events:
            event_type = event.get("event_type", "Unknown")
            status = event.get("status", "Proposed")

            event_score = cls.EVENT_WEIGHTS.get(event_type, 0)
            status_bonus = cls.STATUS_WEIGHTS.get(status, 0)

            score += event_score + status_bonus
            breakdown["event_scores"][event_type] = breakdown["event_scores"].get(event_type, 0) + event_score

        # Add tier bonus
        tier_bonus = cls.TIER_BONUS.get(city_tier, 0)
        score += tier_bonus
        breakdown["tier_bonus"] = tier_bonus

        # Cap at 100
        score = min(score, 100)
        breakdown["total"] = score

        # Determine risk level
        if score >= 70:
            risk_level = "Green"
            time_horizon = "3-5 years"
        elif score >= 50:
            risk_level = "Yellow"
            time_horizon = "5-8 years"
        else:
            risk_level = "Red"
            time_horizon = "8-12 years"

        return {
            "growth_score": score,
            "risk_level": risk_level,
            "time_horizon": time_horizon,
            "breakdown": breakdown,
        }

    @staticmethod
    def determine_risk_level(score: int) -> str:
        """Determine risk level from score"""
        if score >= 70:
            return "Green"
        elif score >= 50:
            return "Yellow"
        else:
            return "Red"

    @staticmethod
    def determine_time_horizon(score: int) -> str:
        """Determine investment time horizon from score"""
        if score >= 70:
            return "3-5 years"
        elif score >= 50:
            return "5-8 years"
        else:
            return "8-12 years"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test scoring
    test_events = [
        {"event_type": "Metro", "status": "Approved"},
        {"event_type": "Highway", "status": "Approved"},
        {"event_type": "Factory", "status": "Under_Construction"},
    ]

    result = ScoringEngine.calculate_score(test_events, "Tier-1")
    print(f"Growth Score: {result['growth_score']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Time Horizon: {result['time_horizon']}")
    print(f"Breakdown: {result['breakdown']}")
