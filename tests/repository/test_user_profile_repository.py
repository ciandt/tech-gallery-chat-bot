from unittest import mock

import pytest

from tech_gallery_bot.domain.user import User
from tech_gallery_bot.domain.user_profile import UserProfile
from tech_gallery_bot.domain.user_technology import UserTechnology
from tech_gallery_bot.repositories import UserProfileRepository

VALID_USER = User(
    id_="123456789123456789",
    name="Jane Doe",
    email="jane@ciandt.com",
    photo="https://server.com/image.png",
)

VALID_PROFILE_DICT = {
    "positiveRecItems": {
        "9GmibrFM": {
            "companyRecommendation": "Recomendada",
            "endorsementQuantity": 18,
            "skillLevel": 4,
            "technologyName": "Python",
            "technologyPhotoUrl": "https://server.com/python.png",
        }
    },
    "negativeRecItems": {
        "lzcZ4Doo": {
            "companyRecommendation": None,
            "endorsementQuantity": 5,
            "skillLevel": 3,
            "technologyName": "Flash",
            "technologyPhotoUrl": "https://server.com/flash.png",
        },
    },
    "otherItems": {
        "p5CVvvZ3": {
            "companyRecommendation": "Recomendada",
            "endorsementQuantity": 17,
            "skillLevel": 4,
            "technologyName": "Git",
            "technologyPhotoUrl": "https://server.com/git.png",
        },
        "gmqohfqT": {
            "companyRecommendation": None,
            "endorsementQuantity": 8,
            "skillLevel": 4,
            "technologyName": "Kotlin",
            "technologyPhotoUrl": "https://server.com/kotlin.png",
        },
    },
}

VALID_PROFILE = UserProfile(
    user=VALID_USER,
    technologies=[
        UserTechnology(name="Python", skill=4, endorsements=18),
        UserTechnology(name="Flash", skill=3, endorsements=5),
        UserTechnology(name="Git", skill=4, endorsements=17),
        UserTechnology(name="Kotlin", skill=4, endorsements=8),
    ],
)


@pytest.mark.parametrize("client", [None, ""])
def test_user_profile_repository_invalid_init(client):
    with pytest.raises(TypeError):
        UserProfileRepository(client)


@pytest.mark.parametrize("user", [None, ""])
def test_user_profile_repository_find_by_user_invalid(user):
    with mock.patch("google.cloud.datastore.Client", autospec=True) as client:
        with pytest.raises(TypeError):
            UserProfileRepository(client).find_by_user(user)


def test_user_profile_repository_find_by_user():
    with mock.patch("google.cloud.datastore.Client", autospec=True) as client:
        client.key.return_value = "user-profile-key-123456789123456789"
        client.get.return_value = VALID_PROFILE_DICT

        user = User(
            id_="123456789123456789",
            name="Jane Doe",
            email="jane@ciandt.com",
            photo="https://server.com/image.png",
        )

        profile = UserProfileRepository(client).find_by_user(user)

        client.key.assert_called_once_with("UserProfile", "profile123456789123456789")
        client.get.assert_called_once_with("user-profile-key-123456789123456789")

        assert profile == VALID_PROFILE


def test_user_profile_find_by_user_without_results():
    with mock.patch("google.cloud.datastore.Client", autospec=True) as client:
        client.key.return_value = "user-profile-key-123456789123456789"
        client.get.return_value = None

        user = User(
            id_="123456789123456789",
            name="Jane Doe",
            email="jane@ciandt.com",
            photo="https://server.com/image.png",
        )

        profile = UserProfileRepository(client).find_by_user(user)
        assert profile is None
