from google_hangouts_chat_bot.commands import Command
from google_hangouts_chat_bot.responses import (
    create_card,
    create_cards_response,
    create_card_paragraph,
)


class Skills(Command):
    command = "skills"
    command_aliases = ["skill"]
    description = "List skill levels description"

    levels = [
        (
            "★☆☆☆☆",
            "Newbie",
            "Might have some theoretical knowledge, but no real practice. Requires training for this subject.",
        ),
        (
            "★★☆☆☆",
            "Capable",
            "Knows something about the subject, but needs some help on complex issues.",
        ),
        (
            "★★★☆☆",
            "Proficient",
            "Knows the subject and can solve complex problems without help. Is able to help co-workers.",
        ),
        (
            "★★★★☆",
            "Master",
            "Is a reference on the subject and can plan the architecture in different contexts. Has worked with it a lot times and knows almost all of its features. Have had the opportunity to make complex mechanisms using this technology.",
        ),
        (
            "★★★★★",
            "Advisor",
            "Is recognized by many colleges from many projects in different contexts. CI&T recognizes the incredible performance.",
        ),
    ]

    def handle(self, arguments, **kwargs):
        rows = [create_card_paragraph("Skill levels<br><br>")]

        for stars, name, description in self.levels:
            rows.append(
                create_card_paragraph(
                    f"{stars} - <b>{name}</b><br>{description}<br><br>"
                )
            )

        return create_cards_response([create_card(rows)])
