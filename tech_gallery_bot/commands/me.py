from google_hangouts_chat_bot.commands import Command
from google_hangouts_chat_bot.responses import (
    create_card,
    create_cards_response,
    create_card_key_value,
    create_card_image,
)


class Me(Command):
    command = "me"
    command_aliases = ["/me"]
    description = "Displays who is talking"
    hidden = True

    def handle(self, arguments, **kwargs):
        if "sender" not in kwargs:
            raise ValueError("'sender' not supplied in kwargs")

        try:
            card = create_card(
                [
                    create_card_key_value("Name", kwargs["sender"]["displayName"]),
                    create_card_key_value("Email", kwargs["sender"]["email"]),
                    create_card_image(kwargs["sender"]["avatarUrl"]),
                ]
            )

            return create_cards_response([card])

        except KeyError as error:
            raise ValueError(f"Invalid sender: '{error.args[0]}' not supplied.")
