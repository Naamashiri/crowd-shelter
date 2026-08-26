"""People who need to reach a protected space during an alert."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from crowd_shelter.domain.geo import GeoPoint


class WalkingProfile(Enum):
    """Mobility category, determining walking speed and step tolerance."""

    ADULT = "adult"
    ELDERLY = "elderly"
    MOBILITY_IMPAIRED = "mobility_impaired"
    PARENT_WITH_STROLLER = "parent_with_stroller"

    @property
    def can_use_steps(self) -> bool:
        """Whether this profile can traverse a path segment with steps."""
        return self not in (
            WalkingProfile.MOBILITY_IMPAIRED,
            WalkingProfile.PARENT_WITH_STROLLER,
        )


@dataclass(frozen=True, slots=True)
class Person:
    """Someone who needs to reach a protected space.

    Attributes:
        person_id: Identifier, unique within a simulation run.
        location: WGS84 position at the moment the alert sounds.
        profile: Mobility category, determining walking speed.
    """

    person_id: str
    location: GeoPoint
    profile: WalkingProfile

    def __post_init__(self) -> None:
        if not self.person_id:
            raise ValueError("person_id must not be empty")
