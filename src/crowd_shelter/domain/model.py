"""Core domain model for crowdShelter."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Final

EARTH_RADIUS_METERS: Final = 6_371_000.0


@dataclass(frozen=True, slots=True)
class GeoPoint:
    """A WGS84 geographic coordinate.

    Attributes:
        lat: Latitude in decimal degrees, in [-90, 90].
        lon: Longitude in decimal degrees, in [-180, 180].
    """

    lat: float
    lon: float

    def __post_init__(self) -> None:
        if not -90.0 <= self.lat <= 90.0:
            raise ValueError(f"Latitude out of range: {self.lat}")
        if not -180.0 <= self.lon <= 180.0:
            raise ValueError(f"Longitude out of range: {self.lon}")

    def distance_to(self, other: GeoPoint) -> float:
        """Great-circle distance to another point, in metres (Haversine)."""
        lat1, lon1 = math.radians(self.lat), math.radians(self.lon)
        lat2, lon2 = math.radians(other.lat), math.radians(other.lon)

        d_lat = lat2 - lat1
        d_lon = lon2 - lon1

        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        return 2 * EARTH_RADIUS_METERS * math.asin(math.sqrt(a))


class ShelterKind(Enum):
    """Type of protected space, as published by the municipal GIS layer."""

    PUBLIC_SHELTER = "public_shelter"
    SCHOOL_SHELTER = "school_shelter"
    UNDERGROUND_PARKING = "underground_parking"
    PROTECTED_SPACE = "protected_space"


class OpeningMode(Enum):
    """How the shelter becomes accessible during an alert."""

    ALWAYS_OPEN = "always_open"
    AUTOMATIC = "automatic"
    MANUAL = "manual"

    @property
    def is_reachable_during_alert(self) -> bool:
        """Manually-opened shelters cannot be relied on within the time budget."""
        return self is not OpeningMode.MANUAL


@dataclass(frozen=True, slots=True)
class Shelter:
    """A protected space that people can be assigned to.

    Attributes:
        shelter_id: Identifier from the source data.
        address: Street address, for display and debugging.
        location: WGS84 position of the entrance.
        kind: Type of protected space.
        capacity: Number of people the shelter can hold.
        capacity_is_estimated: True when capacity was derived from a
            per-kind default rather than a published floor area.
        opening_mode: How the shelter opens during an alert.
        is_accessible: Whether the entrance is step-free.
    """

    shelter_id: str
    address: str
    location: GeoPoint
    kind: ShelterKind
    capacity: int
    capacity_is_estimated: bool
    opening_mode: OpeningMode
    is_accessible: bool

    def __post_init__(self) -> None:
        if not self.shelter_id:
            raise ValueError("shelter_id must not be empty")
        if self.capacity <= 0:
            raise ValueError(f"capacity must be positive, got {self.capacity}")
