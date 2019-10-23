from unittest import mock
from unittest.mock import call, ANY, DEFAULT

import pytest
from google_hangouts_chat_bot.responses import create_text_response

from tech_gallery_bot.commands import User
from tech_gallery_bot.domain import User as UserDomain, UserTechnology
from tech_gallery_bot.usecases import ShowUserEndorsementsResult, ShowUserSkillsResult

DEFAULT_LIMIT = 50

SHOW_USER_SKILLS_RESULT = ShowUserSkillsResult(
    user=UserDomain(
        id_="123",
        name="Jane Doe",
        email="jane@ciandt.com",
        photo="http://server.com/jane.png",
    ),
    technologies=[
        UserTechnology(name="Python", skill=4, endorsements=18),
        UserTechnology(name="Git", skill=4, endorsements=17),
        UserTechnology(name="Kotlin", skill=4, endorsements=8),
        UserTechnology(name="Flash", skill=3, endorsements=5),
        UserTechnology(name="Rust", skill=1, endorsements=0),
    ],
)

SHOW_USER_ENDORSEMENTS_RESULT = ShowUserEndorsementsResult(
    user=UserDomain(
        id_="123",
        name="Jane Doe",
        email="jane@ciandt.com",
        photo="http://server.com/jane.png",
    ),
    technologies=[
        UserTechnology(name="Java", skill=4, endorsements=11),
        UserTechnology(name="Ruby", skill=2, endorsements=6),
        UserTechnology(name="Python", skill=4, endorsements=6),
        UserTechnology(name="HTML", skill=3, endorsements=1),
    ],
)


@pytest.fixture(autouse=True)
def user_repository():
    with mock.patch("tech_gallery_bot.repositories.UserRepository") as _user_repository:
        yield _user_repository


@pytest.fixture(autouse=True)
def user_profile_repository():
    with mock.patch(
        "tech_gallery_bot.repositories.UserProfileRepository"
    ) as _user_profile_repository:
        yield _user_profile_repository


@pytest.fixture(autouse=True)
def kwargs():
    return {
        "user_repository": user_repository,
        "user_profile_repository": user_profile_repository,
    }


@pytest.mark.parametrize("args", [None, "", ("a", "b"), {}])
def test_command_user_with_invalid_arguments(args):
    with pytest.raises(TypeError):
        User().handle(args)


def test_command_user_without_arguments():
    result = User().handle([])
    assert result == create_text_response(
        "Error: <login> is a required parameter; type *help* for more information."
    )


@pytest.mark.parametrize("login", ["me", "/me"])
def test_command_user_me_as_login_without_sender(login):
    with pytest.raises(ValueError):
        User().handle([login])


@pytest.mark.parametrize("login", ["me", "/me"])
def test_command_user_me_as_login_with_invalid_sender(login):
    with pytest.raises(ValueError):
        User().handle([login], sender={})


def test_command_user_without_dependencies():
    with pytest.raises(ValueError):
        User().handle(["jane"])


def test_command_user_without_user_repository_dependency(user_repository):
    kwargs = {
        "user_repository": user_repository,
    }

    with pytest.raises(ValueError):
        User().handle(["jane"], **kwargs)


def test_command_user_with_user_profile_repository_dependency(user_profile_repository):
    kwargs = {
        "user_profile_repository": user_profile_repository,
    }

    with pytest.raises(ValueError):
        User().handle(["jane"], **kwargs)


def test_command_user_with_invalid_user(kwargs):
    with mock.patch("tech_gallery_bot.commands.user.ShowUserSkills") as uc:
        uc.return_value.execute.return_value = None

        result = User().handle(["invalid"], **kwargs)

        assert uc.return_value.execute.call_args == call("invalid@ciandt.com", ANY)

        assert result == create_text_response("User 'invalid' not found.")


@mock.patch.multiple(
    "tech_gallery_bot.commands.user",
    create_card_paragraph=DEFAULT,
    create_card_header=DEFAULT,
    create_card=DEFAULT,
    create_cards_response=DEFAULT,
)
@pytest.mark.parametrize("login", ["jane", "me"])
def test_command_user_with_default_options(kwargs, login, **mocks):
    with mock.patch("tech_gallery_bot.commands.user.ShowUserSkills") as uc:
        uc.return_value.execute.return_value = SHOW_USER_SKILLS_RESULT

        mocks["create_cards_response"].return_value = "cards-response"

        sender = {
            "email": "jane@ciandt.com",
        }

        result = User().handle([login], sender=sender, **kwargs)

        assert uc.return_value.execute.call_args == call(
            "jane@ciandt.com", DEFAULT_LIMIT
        )

        assert mocks["create_card_paragraph"].call_args == call(
            "★★★★☆ <b>Python</b><br>★★★★☆ <b>Git</b><br>★★★★☆ <b>Kotlin</b><br>★★★☆☆ <b>Flash</b><br>★☆☆☆☆ <b>Rust</b>"
        )

        assert mocks["create_card_header"].call_args == call(
            "Jane Doe", "jane@ciandt.com", "http://server.com/jane.png", "AVATAR"
        )

        mocks["create_card"].assert_called_once()
        mocks["create_cards_response"].assert_called_once()

        assert result == "cards-response"


def test_command_user_with_email(kwargs):
    with mock.patch("tech_gallery_bot.commands.user.ShowUserSkills") as uc:
        uc.return_value.execute.return_value = None

        User().handle(["jane@ciandt.com"], **kwargs)

        assert uc.return_value.execute.call_args == call(
            "jane@ciandt.com", DEFAULT_LIMIT
        )


@pytest.mark.parametrize("param", ["--endorsement", "--endorsements"])
def test_command_user_order_by_endorsement(kwargs, param):
    with mock.patch("tech_gallery_bot.commands.user.ShowUserEndorsements") as uc:
        uc.return_value.execute.return_value = None

        User().handle(["jane", param], **kwargs)

        assert uc.return_value.execute.call_args == call(
            "jane@ciandt.com", DEFAULT_LIMIT
        )


@pytest.mark.parametrize(
    "limit",
    [
        "--limit",
        "--limit=",
        "--limit==",
        "--limit=A",
        "--limit=-10",
        "--limit=0",
        "--limit=2.3",
    ],
)
def test_command_user_with_invalid_limit(kwargs, limit):
    result = User().handle(["jane", limit], **kwargs)
    assert result == create_text_response(
        "Error: Invalid _limit_ parameter; type *help* for more information."
    )


def test_command_user_with_limit(kwargs):
    with mock.patch("tech_gallery_bot.commands.user.ShowUserSkills") as uc:
        uc.return_value.execute.return_value = None

        User().handle(["jane", "--limit=20"], **kwargs)

        assert uc.return_value.execute.call_args == call("jane@ciandt.com", 20)


@mock.patch.multiple(
    "tech_gallery_bot.commands.user",
    create_card_paragraph=DEFAULT,
    create_card_header=DEFAULT,
    create_card=DEFAULT,
    create_cards_response=DEFAULT,
)
@pytest.mark.parametrize("login", ["jane", "me"])
def test_command_user_order_by_endorsement_with_limit(kwargs, login, **mocks):
    with mock.patch("tech_gallery_bot.commands.user.ShowUserEndorsements") as uc:
        uc.return_value.execute.return_value = SHOW_USER_ENDORSEMENTS_RESULT

        mocks["create_cards_response"].return_value = "cards-response"

        sender = {
            "email": "jane@ciandt.com",
        }

        result = User().handle(
            [login, "--endorsements", "--limit=5"], sender=sender, **kwargs
        )

        assert uc.return_value.execute.call_args == call("jane@ciandt.com", 5)

        assert mocks["create_card_paragraph"].call_args_list == [
            call("<b>Java</b>: <br>11 endorsements"),
            call("<b>Ruby</b>: <br>6 endorsements"),
            call("<b>Python</b>: <br>6 endorsements"),
            call("<b>HTML</b>: <br>1 endorsement"),
        ]

        assert mocks["create_card_header"].call_args == call(
            "Jane Doe", "jane@ciandt.com", "http://server.com/jane.png", "AVATAR"
        )

        mocks["create_card"].assert_called_once()
        mocks["create_cards_response"].assert_called_once()

        assert result == "cards-response"
