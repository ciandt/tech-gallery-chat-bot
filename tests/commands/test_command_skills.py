from unittest import mock
from unittest.mock import DEFAULT, call, ANY

from tech_gallery_bot.commands import Skills


@mock.patch.multiple(
    "tech_gallery_bot.commands.skills",
    create_card_paragraph=DEFAULT,
    create_cards_response=DEFAULT,
)
def test_command_skills(**mocks):
    Skills().handle(None)

    mocks["create_card_paragraph"].assert_has_calls(
        [call(ANY)] * 6  # 1 title + 5 levels
    )

    mocks["create_cards_response"].assert_called_once()
