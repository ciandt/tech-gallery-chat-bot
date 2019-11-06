from unittest import mock
from unittest.mock import DEFAULT, call, ANY

from tech_gallery_bot.commands import About


@mock.patch.multiple(
    "tech_gallery_bot.commands.about",
    create_card_key_value=DEFAULT,
    create_cards_response=DEFAULT,
)
def test_command_about(**mocks):
    About().handle(None)

    mocks["create_card_key_value"].assert_has_calls(
        [call("Version", ANY), call("Source", ANY, on_click=ANY)]
    )

    mocks["create_cards_response"].assert_called_once()
