from google_hangouts_chat_bot.commands import Command
from google_hangouts_chat_bot.responses import (
    create_card,
    create_card_key_value,
    create_cards_response,
)

from tech_gallery_bot.version import __version__


class About(Command):
    command = "about"
    command_aliases = ["info"]
    description = "About this bot"
    hidden = True

    def handle(self, arguments, **kwargs):
        card = create_card(
            [
                create_card_key_value("Version", __version__),
                create_card_key_value(
                    "Source", "https://github.com/ciandt/tech-gallery-chat-bot"
                ),
                create_card_key_value("Created by", "jpimentel@ciandt.com"),
            ]
        )

        return create_cards_response([card])
