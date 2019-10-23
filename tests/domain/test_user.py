import pytest

from tech_gallery_bot.domain.user import User
from tech_gallery_bot.domain.user_technology import UserTechnology

technologies = [
    UserTechnology("java", 2, 0),
    UserTechnology("python", 0, 2),
    UserTechnology("swift", 20, 31),
]


@pytest.mark.parametrize(
    "id_,name,email,photo",
    [
        (100, "Jane", "jane@ciandt.com", "http://server.com/image.png"),
        (101, "John", "john@ciandt.com", None),
        (102, "Richard", "richard@ciandt.com", "https://server.com/another-image.png"),
    ],
)
def test_user_init(id_, name, email, photo):
    user = User(id_=id_, name=name, email=email, photo=photo)

    assert user.id == id_
    assert user.name == name
    assert user.email == email
    assert user.photo == photo


def test_user_init_without_technologies():
    user = User(
        id_=101,
        name="Jane",
        email="jane@ciandt.com",
        photo="http://server.com/image.png",
    )

    assert user.id == 101
    assert user.name == "Jane"
    assert user.email == "jane@ciandt.com"
    assert user.photo == "http://server.com/image.png"


def test_user_from_dict():
    user = User.from_dict(
        {
            "id": 100,
            "name": "Jane",
            "email": "jane@ciandt.com",
            "photo": "http://server.com/image.png",
        }
    )

    assert user.id == 100
    assert user.name == "Jane"
    assert user.email == "jane@ciandt.com"
    assert user.photo == "http://server.com/image.png"


def test_user_to_dict():
    user_dict = {
        "id": 101,
        "name": "John",
        "email": "john@ciandt.com",
        "photo": "http://server.com/image.png",
    }

    user = User.from_dict(user_dict)

    assert user.to_dict() == user_dict


def test_user_comparison():
    user_dict = {
        "id": 102,
        "name": "Richard",
        "email": "richard@ciandt.com",
        "photo": "https://server.com/image.png",
    }

    user1 = User.from_dict(user_dict)
    user2 = User.from_dict(user_dict)

    assert user1 == user2


def test_user_repr():
    user = User(
        id_=101,
        name="Jane",
        email="jane@ciandt.com",
        photo="http://server.com/image.png",
    )

    assert (
        repr(user)
        == "User(id_=101, name='Jane', email='jane@ciandt.com', photo='http://server.com/image.png')"
    )
