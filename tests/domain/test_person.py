import pytest

from crowd_shelter.domain.geo import GeoPoint
from crowd_shelter.domain.person import Person, WalkingProfile


@pytest.mark.parametrize(
    "profile",
    [WalkingProfile.MOBILITY_IMPAIRED, WalkingProfile.PARENT_WITH_STROLLER],
)
def test_wheeled_profiles_cannot_use_steps(profile: WalkingProfile) -> None:
    assert not profile.can_use_steps


@pytest.mark.parametrize("profile", [WalkingProfile.ADULT, WalkingProfile.ELDERLY])
def test_walking_profiles_can_use_steps(profile: WalkingProfile) -> None:
    assert profile.can_use_steps


def test_rejects_empty_person_id() -> None:
    with pytest.raises(ValueError, match="person_id"):
        Person(
            person_id="",
            location=GeoPoint(lat=32.0, lon=34.0),
            profile=WalkingProfile.ADULT,
        )
