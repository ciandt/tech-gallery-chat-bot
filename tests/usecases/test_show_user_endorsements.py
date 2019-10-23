from unittest import mock

from tech_gallery_bot.domain import User, UserProfile, UserTechnology
from tech_gallery_bot.usecases import ShowUserEndorsements

user = User(
    id_=102, name="John", email="john@ciandt.com", photo="http://server.com/image.png",
)


def test_show_user_endorsements():
    with mock.patch(
        "tech_gallery_bot.repositories.UserRepository"
    ) as user_repository, mock.patch(
        "tech_gallery_bot.repositories.UserProfileRepository"
    ) as user_profile_repository:
        user_repository.find_by_email.return_value = user

        user_profile_repository.find_by_user.return_value = UserProfile(
            user=user,
            technologies=[
                UserTechnology(name="Flash", skill=3, endorsements=5),
                UserTechnology(name="Python", skill=4, endorsements=18),
                UserTechnology(name="Git", skill=4, endorsements=17),
                UserTechnology(name="Kotlin", skill=4, endorsements=8),
                UserTechnology(name="Rust", skill=1, endorsements=0),
                UserTechnology(name="C#", skill=0, endorsements=2),
                UserTechnology(name="Docker", skill=2, endorsements=2),
            ],
        )

        uc = ShowUserEndorsements(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
        )

        result = uc.execute("john@ciandt.com", 5)

        user_repository.find_by_email.assert_called_once_with("john@ciandt.com")
        user_profile_repository.find_by_user.assert_called_once_with(user)

        assert result.user == user

        assert result.technologies == [
            UserTechnology(name="Python", skill=4, endorsements=18),
            UserTechnology(name="Git", skill=4, endorsements=17),
            UserTechnology(name="Kotlin", skill=4, endorsements=8),
            UserTechnology(name="Flash", skill=3, endorsements=5),
            UserTechnology(name="Docker", skill=2, endorsements=2),
        ]


def test_show_user_endorsements_no_zero():
    with mock.patch(
        "tech_gallery_bot.repositories.UserRepository"
    ) as user_repository, mock.patch(
        "tech_gallery_bot.repositories.UserProfileRepository"
    ) as user_profile_repository:
        user_repository.find_by_email.return_value = user

        user_profile_repository.find_by_user.return_value = UserProfile(
            user=user,
            technologies=[
                UserTechnology(name="Flash", skill=3, endorsements=5),
                UserTechnology(name="C#", skill=0, endorsements=0),
                UserTechnology(name="Python", skill=4, endorsements=18),
                UserTechnology(name="Rust", skill=0, endorsements=0),
                UserTechnology(name="Git", skill=4, endorsements=17),
                UserTechnology(name="Kotlin", skill=4, endorsements=8),
                UserTechnology(name="Docker", skill=3, endorsements=2),
                UserTechnology(name="PHP", skill=2, endorsements=0),
            ],
        )

        uc = ShowUserEndorsements(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
        )

        result = uc.execute("john@ciandt.com", 10)

        user_repository.find_by_email.assert_called_once_with("john@ciandt.com")
        user_profile_repository.find_by_user.assert_called_once_with(user)

        assert result.user == user

        assert result.technologies == [
            UserTechnology(name="Python", skill=4, endorsements=18),
            UserTechnology(name="Git", skill=4, endorsements=17),
            UserTechnology(name="Kotlin", skill=4, endorsements=8),
            UserTechnology(name="Flash", skill=3, endorsements=5),
            UserTechnology(name="Docker", skill=3, endorsements=2),
        ]


def test_show_user_endorsements_user_not_found():
    with mock.patch(
        "tech_gallery_bot.repositories.UserRepository"
    ) as user_repository, mock.patch(
        "tech_gallery_bot.repositories.UserProfileRepository"
    ) as user_profile_repository:
        user_repository.find_by_email.return_value = None

        uc = ShowUserEndorsements(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
        )

        result = uc.execute("john@ciandt.com", 10)

        user_repository.find_by_email.assert_called_once_with("john@ciandt.com")
        user_profile_repository.find_by_user.assert_not_called()

        assert result is None


def test_show_user_endorsements_user_profile_not_found():
    with mock.patch(
        "tech_gallery_bot.repositories.UserRepository"
    ) as user_repository, mock.patch(
        "tech_gallery_bot.repositories.UserProfileRepository"
    ) as user_profile_repository:
        user_repository.find_by_email.return_value = user
        user_profile_repository.find_by_user.return_value = None

        uc = ShowUserEndorsements(
            user_repository=user_repository,
            user_profile_repository=user_profile_repository,
        )

        result = uc.execute("john@ciandt.com", 10)

        user_repository.find_by_email.assert_called_once_with("john@ciandt.com")
        user_profile_repository.find_by_user.assert_called_once_with(user)

        assert result is None
