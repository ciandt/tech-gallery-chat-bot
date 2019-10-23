from google_hangouts_chat_bot.commands import Command
from google_hangouts_chat_bot.responses import (
    create_card_paragraph,
    create_card,
    create_card_header,
    create_cards_response,
    create_text_response,
)

from tech_gallery_bot.usecases.show_user_endorsements import ShowUserEndorsements
from tech_gallery_bot.usecases.show_user_skills import ShowUserSkills


class User(Command):
    command = "user"
    arguments = "<login> [--skills | --endorsements] [--limit=<n>]"
    description = (
        "To show an user\n"
        "\t_--skills_ to order by skill level _(default)_\n"
        "\t_--endorsements_ to order by amount of endorsements\n"
        "\t_--limit_ to limit the number of results; default to _50_ if not specified"
    )

    def handle(self, arguments, **kwargs):
        if not isinstance(arguments, list):
            raise TypeError("arguments should be a list")

        if len(arguments) == 0:
            return create_text_response(
                "Error: <login> is a required parameter; type *help* for more information."
            )

        login = arguments.pop(0).lower()
        if login == "me" or login == "/me":
            if "sender" not in kwargs:
                raise ValueError("'sender' not supplied in kwargs")

            if "email" not in kwargs["sender"]:
                raise ValueError("Invalid sender: 'email' not supplied.")

            login = kwargs["sender"]["email"].split("@")[0]

        """ LIMIT """
        limit = 50
        for arg in arguments:
            if "--limit" in arg:
                arguments.remove(arg)
                try:
                    arg_name, value = arg.split("=")
                    limit = int(value)

                    if limit < 1:
                        return create_text_response(
                            "Error: Invalid _limit_ parameter; type *help* for more information."
                        )

                except ValueError:
                    return create_text_response(
                        "Error: Invalid _limit_ parameter; type *help* for more information."
                    )

        """ ORDER """
        order = "skills"  # default
        if len(arguments) > 0:
            if "--endorsement" in arguments[0]:
                order = "endorsements"

        if order == "skills":
            result = self._show_skills(login, limit, **kwargs)
        else:
            result = self._show_endorsements(login, limit, **kwargs)

        if result is None:
            return create_text_response(f"User '{login}' not found.")

        return result

    def _show_skills(self, login, limit, **kwargs):
        email = self._login_to_email(login)
        user_repository, user_profile_repository = self._get_repos(kwargs)

        result = ShowUserSkills(user_repository, user_profile_repository).execute(
            email, limit
        )
        if result is None:
            return None

        lines = []

        for tech in result.technologies:
            stars = ("★" * tech.skill) + ("☆" * (5 - tech.skill))
            lines.append(f"{stars} <b>{tech.name}</b>")

        card = create_card(
            [create_card_paragraph("<br>".join(lines))],
            header=self._get_card_header(result.user),
        )

        return create_cards_response([card])

    def _show_endorsements(self, login, limit, **kwargs):
        email = self._login_to_email(login)
        user_repository, user_profile_repository = self._get_repos(kwargs)

        result = ShowUserEndorsements(user_repository, user_profile_repository).execute(
            email, limit
        )
        if result is None:
            return None

        rows = []

        for tech in result.technologies:
            rows.append(
                create_card_paragraph(
                    f'<b>{tech.name}</b>: <br>{tech.endorsements} endorsement{"s" if tech.endorsements > 1 else ""}'
                )
            )

        card = create_card(rows, header=self._get_card_header(result.user))

        return create_cards_response([card])

    @staticmethod
    def _get_repos(kwargs):
        if "user_repository" not in kwargs:
            raise ValueError("'user_repository' not supplied in kwargs")

        if "user_profile_repository" not in kwargs:
            raise ValueError("'user_profile_repository' not supplied in kwargs")

        return kwargs["user_repository"], kwargs["user_profile_repository"]

    @staticmethod
    def _get_card_header(user):
        return create_card_header(user.name, user.email, user.photo, "AVATAR")

    @staticmethod
    def _login_to_email(login):
        if "@ciandt.com" in login:
            email = login
        else:
            email = f"{login}@ciandt.com"
        return email
