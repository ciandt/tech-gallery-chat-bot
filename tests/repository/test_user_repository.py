from unittest import mock

import pytest

from tech_gallery_bot.domain.user import User
from tech_gallery_bot.repositories import UserRepository
from tests.repository.helpers import DotDict

VALID_USER_DICT = DotDict(
    {
        "id": "123456789123456789",
        "email": "jane@ciandt.com",
        "followedTechnologyIds": ["python", "ruby", "kotlin", "rust"],
        "name": "Jane Doe",
        "photo": "https://server.com/image.png",
        "postGooglePlusPreference": False,
        "project": None,
        "timezoneOffset": -180,
    }
)

VALID_USER_DOMAIN = User(
    id_="123456789123456789",
    name="Jane Doe",
    email="jane@ciandt.com",
    photo="https://server.com/image.png",
)


@pytest.mark.parametrize("client", [None, ""])
def test_user_repository_invalid_init(client):
    with pytest.raises(TypeError):
        UserRepository(client)


def test_user_repository_find_by_email():
    with mock.patch("google.cloud.datastore.Client", autospec=True) as client:
        with mock.patch("google.cloud.datastore.query.Query", autospec=True) as query:
            client.query.return_value = query
            query.fetch.return_value = [VALID_USER_DICT]

            user = UserRepository(client).find_by_email("jane@ciandt.com")

            client.query.assert_called_once_with(kind="TechGalleryUser")
            query.add_filter.assert_called_once_with("email", "=", "jane@ciandt.com")
            query.fetch.assert_called_once_with(limit=1)

            assert user == VALID_USER_DOMAIN


def test_user_repository_find_by_email_without_results():
    with mock.patch("google.cloud.datastore.Client", autospec=True) as client:
        with mock.patch("google.cloud.datastore.query.Query", autospec=True) as query:
            client.query.return_value = query
            query.fetch.return_value = []

            user = UserRepository(client).find_by_email("jane@ciandt.com")
            assert user is None
