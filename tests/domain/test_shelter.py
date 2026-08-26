from dataclasses import FrozenInstanceError

import pytest

from crowd_shelter.domain.shelter import OpeningMode
from tests.domain.test_geo import _shelter


def test_manual_shelters_are_not_reachable_during_alert() -> None:
    assert not OpeningMode.MANUAL.is_reachable_during_alert


@pytest.mark.parametrize("mode", [OpeningMode.ALWAYS_OPEN, OpeningMode.AUTOMATIC])
def test_self_opening_shelters_are_reachable(mode: OpeningMode) -> None:
    assert mode.is_reachable_during_alert


def test_rejects_non_positive_capacity() -> None:
    with pytest.raises(ValueError, match="capacity"):
        _shelter(capacity=0)


def test_rejects_empty_shelter_id() -> None:
    with pytest.raises(ValueError, match="shelter_id"):
        _shelter(shelter_id="")


def test_shelter_is_immutable() -> None:
    shelter = _shelter()

    with pytest.raises(FrozenInstanceError):
        shelter.capacity = 999  # type: ignore[misc]
