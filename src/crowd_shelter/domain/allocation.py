"""The outcome of assigning people to shelters."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Assignment:
    """One person routed to one shelter.

    Attributes:
        person_id: Who is being routed.
        shelter_id: Where they were sent.
        eta_seconds: Expected walking time to reach the shelter.
    """

    person_id: str
    shelter_id: str
    eta_seconds: float

    def __post_init__(self) -> None:
        if self.eta_seconds < 0:
            raise ValueError(f"eta_seconds must not be negative, got {self.eta_seconds}")


@dataclass(frozen=True, slots=True)
class AllocationResult:
    """The full outcome of one allocation run.

    Attributes:
        assignments: People who were given a shelter.
        unassigned_person_ids: People with no reachable shelter within
            the time budget. These are not failures of the algorithm —
            they are people who should shelter in place instead.
    """

    assignments: tuple[Assignment, ...]
    unassigned_person_ids: tuple[str, ...]

    @property
    def assigned_count(self) -> int:
        """How many people were given a shelter."""
        return len(self.assignments)

    @property
    def total_people(self) -> int:
        """How many people were considered in this run."""
        return self.assigned_count + len(self.unassigned_person_ids)

    def occupancy(self) -> dict[str, int]:
        """Return the number of people assigned to each shelter."""
        counts: dict[str, int] = {}
        for assignment in self.assignments:
            counts[assignment.shelter_id] = counts.get(assignment.shelter_id, 0) + 1
        return counts
