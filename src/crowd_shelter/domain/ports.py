"""Interfaces the domain requires from the outside world.

Implementations live in the infrastructure and application layers;
the domain depends only on these contracts.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from crowd_shelter.domain.allocation import AllocationResult
from crowd_shelter.domain.geo import GeoPoint
from crowd_shelter.domain.person import Person, WalkingProfile
from crowd_shelter.domain.shelter import Shelter

#: Walking time returned when no route exists between two points.
UNREACHABLE = float("inf")


class ShelterRepository(Protocol):
    """A source of shelter records."""

    def all_shelters(self) -> Sequence[Shelter]:
        """Return every known shelter."""
        ...


class PathFinder(Protocol):
    """Computes walking time between points on the pedestrian network."""

    def walking_time_seconds(
        self,
        origin: GeoPoint,
        destination: GeoPoint,
        profile: WalkingProfile,
    ) -> float:
        """Return walking time in seconds, or UNREACHABLE if no route exists.

        The profile affects both speed and which segments are passable:
        wheeled profiles cannot use paths with steps.
        """
        ...


class AllocationStrategy(Protocol):
    """Assigns people to shelters."""

    def allocate(
        self,
        people: Sequence[Person],
        shelters: Sequence[Shelter],
        path_finder: PathFinder,
    ) -> AllocationResult:
        """Assign each person to a shelter, or leave them unassigned."""
        ...
