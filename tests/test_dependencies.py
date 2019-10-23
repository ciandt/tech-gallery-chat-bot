from unittest import mock
from unittest.mock import ANY

import pytest

from tech_gallery_bot.dependencies import get_dependencies
from tech_gallery_bot.repositories import UserRepository, UserProfileRepository


@pytest.mark.parametrize("config", [None, "", ("a", "b"), True, False])
def test_get_dependencies_with_invalid_argument(config):
    with pytest.raises(TypeError):
        get_dependencies(config=config)


def test_get_dependencies_with_incomplete_argument():
    with pytest.raises(ValueError):
        get_dependencies(config={})


def test_get_dependencies_with_correct_argument():
    with mock.patch("tech_gallery_bot.dependencies.Client", autospec=True) as client:
        client.from_service_account_json.return_value = client

        dependencies = get_dependencies(
            config={"TECH_GALLERY_SERVICE_ACCOUNT": "path/to/file.json"}
        )

        client.from_service_account_json.assert_called_once_with(
            "path/to/file.json", namespace=ANY
        )

        assert isinstance(dependencies["user_repository"], UserRepository)

        assert isinstance(
            dependencies["user_profile_repository"], UserProfileRepository
        )
