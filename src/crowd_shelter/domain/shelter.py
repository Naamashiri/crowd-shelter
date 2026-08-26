from dataclasses import dataclass
from enum import Enum

from crowd_shelter.domain.geo import GeoPoint


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
