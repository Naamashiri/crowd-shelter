from __future__ import annotations

import math
from dataclasses import dataclass
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
