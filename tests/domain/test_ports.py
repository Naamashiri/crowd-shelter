from collections.abc import Sequence

from crowd_shelter.domain.allocation import AllocationResult
from crowd_shelter.domain.geo import GeoPoint
from crowd_shelter.domain.person import Person, WalkingProfile
from crowd_shelter.domain.ports import (
    UNREACHABLE,
    AllocationStrategy,
    PathFinder,
    ShelterRepository,
)
from crowd_shelter.domain.shelter import Shelter


class FakeShelterRepository:
    """A repository backed by an in-memory list."""

    def __init__(self, shelters: Sequence[Shelter]) -> None:
        self._shelters = tuple(shelters)

    def all_shelters(self) -> Sequence[Shelter]:
        return self._shelters


class StraightLinePathFinder:
    """A path finder that ignores the street network entirely."""

    def walking_time_seconds(
        self,
        origin: GeoPoint,
        destination: GeoPoint,
        profile: WalkingProfile,
    ) -> float:
        return origin.distance_to(destination) / 1.4


class RefusingStrategy:
    """A strategy that assigns nobody."""

    def allocate(
        self,
        people: Sequence[Person],
        shelters: Sequence[Shelter],
        path_finder: PathFinder,
    ) -> AllocationResult:
        return AllocationResult(
            assignments=(),
            unassigned_person_ids=tuple(p.person_id for p in people),
        )


def test_fakes_satisfy_the_protocols() -> None:
    repository: ShelterRepository = FakeShelterRepository([])
    finder: PathFinder = StraightLinePathFinder()
    strategy: AllocationStrategy = RefusingStrategy()

    assert repository.all_shelters() == ()
    assert finder is not None
    assert strategy is not None


def test_unreachable_is_greater_than_any_budget() -> None:
    assert UNREACHABLE > 10_000.0
