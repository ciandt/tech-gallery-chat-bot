from unittest import mock
from unittest.mock import call, DEFAULT

import pytest

from tech_gallery_bot.commands import Me


def test_command_me_without_sender():
    with pytest.raises(ValueError):
        Me().handle(None)


def test_command_me_with_invalid_sender():
    with pytest.raises(ValueError):
        Me().handle(None, sender={})


@mock.patch.multiple(
    "tech_gallery_bot.commands.me",
    create_card_key_value=DEFAULT,
    create_card_image=DEFAULT,
    create_cards_response=DEFAULT,
)
def test_command_me(**mocks):
    sender = {
        "displayName": "Jane Doe",
        "email": "jane@doe.com",
        "avatarUrl": "http://server.com/avatar.png",
    }

    Me().handle(None, sender=sender)

    assert mocks["create_card_key_value"].call_args_list == [
        call("Name", "Jane Doe"),
        call("Email", "jane@doe.com"),
    ]

    assert mocks["create_card_image"].call_args_list == [
        call("http://server.com/avatar.png")
    ]

    mocks["create_cards_response"].assert_called_once()
