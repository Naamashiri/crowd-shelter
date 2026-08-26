"""Tunable assumptions. Every value here is a documented estimate."""

from typing import Final

from crowd_shelter.domain.model import ShelterKind

#: Seconds from siren to impact in central Israel.
ALERT_TIME_BUDGET_SECONDS: Final = 90.0

#: Seconds lost to hearing the alert, orienting and starting to move.
REACTION_TIME_SECONDS: Final = 18.0

#: Floor area assumed per person in a public shelter.
SQUARE_METRES_PER_PERSON: Final = 0.75

#: Fallback capacity when the source record has no floor area.
DEFAULT_CAPACITY_BY_KIND: Final[dict[ShelterKind, int]] = {
    ShelterKind.PUBLIC_SHELTER: 60,
    ShelterKind.SCHOOL_SHELTER: 120,
    ShelterKind.UNDERGROUND_PARKING: 400,
    ShelterKind.PROTECTED_SPACE: 40,
}


def estimate_capacity(kind: ShelterKind, area_sqm: float | None) -> tuple[int, bool]:
    """Return (capacity, is_estimated) for a shelter record.

    Uses the published floor area when available, otherwise falls back
    to a per-kind default.
    """
    if area_sqm is not None and area_sqm > 0:
        return max(1, int(area_sqm / SQUARE_METRES_PER_PERSON)), False
    return DEFAULT_CAPACITY_BY_KIND[kind], True
