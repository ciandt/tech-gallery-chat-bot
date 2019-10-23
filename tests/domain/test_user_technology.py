import pytest

from tech_gallery_bot.domain.user_technology import UserTechnology


@pytest.mark.parametrize(
    "args", [("java", 4, 3), ("python", 5, 0), ("ruby", 0, 0), ("nodejs", 30, 5000)]
)
def test_user_technology_init(args):
    (name, skills, endorsements) = args

    user_technology = UserTechnology(name, skills, endorsements)

    assert user_technology.name == name
    assert user_technology.skill == skills
    assert user_technology.endorsements == endorsements


def test_user_technology_from_dict():
    user_technology = UserTechnology.from_dict(
        {"name": "javascript", "skill": 2, "endorsements": 1000,}
    )

    assert user_technology.name == "javascript"
    assert user_technology.skill == 2
    assert user_technology.endorsements == 1000


def test_user_technology_to_dict():
    user_technology_dict = {
        "name": "javascript",
        "skill": 2,
        "endorsements": 1000,
    }

    user_technology = UserTechnology.from_dict(user_technology_dict)

    assert user_technology.to_dict() == user_technology_dict


def test_user_technology_comparison():
    user_technology_dict = {
        "name": "javascript",
        "skill": 2,
        "endorsements": 1000,
    }

    user_technology1 = UserTechnology.from_dict(user_technology_dict)
    user_technology2 = UserTechnology.from_dict(user_technology_dict)

    assert user_technology1 == user_technology2


def test_user_technology_repr():
    user_technology = UserTechnology(name="python", skill=4, endorsements=40)

    assert (
        repr(user_technology)
        == "UserTechnology(name='python', skill=4, endorsements=40)"
    )
