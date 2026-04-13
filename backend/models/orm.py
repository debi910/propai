"""
SQLAlchemy ORM models for PropAI platform
"""
from datetime import datetime
from typing import Optional
from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    DateTime,
    ForeignKey,
    TIMESTAMP,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class City(Base):
    """City metadata and location"""

    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    tier = Column(String(50))  # Tier-1, Tier-2
    region = Column(String(50))
    latitude = Column(Numeric(10, 6))
    longitude = Column(Numeric(10, 6))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    zones = relationship("Zone", back_populates="city", cascade="all, delete-orphan")


class EventClassification(Base):
    """Event type classifications"""

    __tablename__ = "event_classifications"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="classification")


class Event(Base):
    """Raw news events from scrapers"""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    location = Column(String(255))
    event_date = Column(TIMESTAMP)
    source_url = Column(String(500))
    source_name = Column(String(100))
    classification_id = Column(Integer, ForeignKey("event_classifications.id"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    classification = relationship("EventClassification", back_populates="events")
    zone_events = relationship("ZoneEvent", back_populates="event", cascade="all, delete-orphan")


class Zone(Base):
    """Geographic zones with growth potential"""

    __tablename__ = "zones"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    zone_type = Column(String(100))
    description = Column(Text)
    geometry = Column(Geometry("Polygon", srid=4326))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    city = relationship("City", back_populates="zones")
    scores = relationship("Score", back_populates="zone", cascade="all, delete-orphan")
    zone_events = relationship("ZoneEvent", back_populates="zone", cascade="all, delete-orphan")


class Score(Base):
    """Scoring breakdown per zone"""

    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)
    zone_id = Column(Integer, ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    score_value = Column(Integer)
    risk_level = Column(String(20))
    highway_proximity = Column(Integer)
    metro_proximity = Column(Integer)
    airport_proximity = Column(Integer)
    factory_proximity = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    zone = relationship("Zone", back_populates="scores")


class ZoneEvent(Base):
    """Pivot table: zones linked to triggering events"""

    __tablename__ = "zone_events"

    id = Column(Integer, primary_key=True)
    zone_id = Column(Integer, ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    zone = relationship("Zone", back_populates="zone_events")
    event = relationship("Event", back_populates="zone_events")


class User(Base):
    """User accounts (for future authentication)"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
