from dataclasses import FrozenInstanceError

import pytest

from crowd_shelter.domain.geo import GeoPoint
from crowd_shelter.domain.shelter import OpeningMode, Shelter, ShelterKind


def _shelter(**overrides: object) -> Shelter:
    """Build a valid Shelter, overriding only the fields under test."""
    defaults: dict[str, object] = {
        "shelter_id": "TLV-001",
        "address": "Nahalat Binyamin 12",
        "location": GeoPoint(lat=32.0668, lon=34.7745),
        "kind": ShelterKind.PUBLIC_SHELTER,
        "capacity": 60,
        "capacity_is_estimated": False,
        "opening_mode": OpeningMode.AUTOMATIC,
        "is_accessible": True,
    }
    return Shelter(**{**defaults, **overrides})  # type: ignore[arg-type]


def test_distance_to_self_is_zero() -> None:
    point = GeoPoint(lat=32.0668, lon=34.7745)
    assert point.distance_to(point) == pytest.approx(0.0)


def test_known_distance_tel_aviv_landmarks() -> None:
    dizengoff_square = GeoPoint(lat=32.0781, lon=34.7743)
    rabin_square = GeoPoint(lat=32.0806, lon=34.7806)

    distance = dizengoff_square.distance_to(rabin_square)

    assert distance == pytest.approx(650, abs=100)


def test_distance_is_symmetric() -> None:
    a = GeoPoint(lat=32.06, lon=34.77)
    b = GeoPoint(lat=32.08, lon=34.79)

    assert a.distance_to(b) == pytest.approx(b.distance_to(a))


def test_geopoint_is_immutable() -> None:
    point = GeoPoint(lat=32.0, lon=34.0)

    with pytest.raises(FrozenInstanceError):
        point.lat = 33.0  # type: ignore[misc]


@pytest.mark.parametrize("bad_lat", [91.0, -91.0, 180.0])
def test_rejects_out_of_range_latitude(bad_lat: float) -> None:
    with pytest.raises(ValueError, match="Latitude"):
        GeoPoint(lat=bad_lat, lon=34.0)


@pytest.mark.parametrize("bad_lon", [181.0, -181.0, 360.0])
def test_rejects_out_of_range_longitude(bad_lon: float) -> None:
    with pytest.raises(ValueError, match="Longitude"):
        GeoPoint(lat=32.0, lon=bad_lon)
