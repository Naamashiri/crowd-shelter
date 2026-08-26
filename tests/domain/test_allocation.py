import pytest

from crowd_shelter.domain.allocation import AllocationResult, Assignment


def _result(*shelter_ids: str, unassigned: int = 0) -> AllocationResult:
    assignments = tuple(
        Assignment(person_id=f"P{i}", shelter_id=sid, eta_seconds=42.0)
        for i, sid in enumerate(shelter_ids)
    )
    unassigned_ids = tuple(f"U{i}" for i in range(unassigned))
    return AllocationResult(assignments=assignments, unassigned_person_ids=unassigned_ids)


def test_rejects_negative_eta() -> None:
    with pytest.raises(ValueError, match="eta_seconds"):
        Assignment(person_id="P1", shelter_id="S1", eta_seconds=-1.0)


def test_counts_assigned_and_total() -> None:
    result = _result("S1", "S1", "S2", unassigned=2)

    assert result.assigned_count == 3
    assert result.total_people == 5


def test_occupancy_groups_by_shelter() -> None:
    result = _result("S1", "S1", "S2")

    assert result.occupancy() == {"S1": 2, "S2": 1}


def test_empty_result_has_no_occupancy() -> None:
    result = _result()

    assert result.occupancy() == {}
    assert result.total_people == 0
