from tech_gallery_bot.domain.user import User
from tech_gallery_bot.domain.user_profile import UserProfile
from tech_gallery_bot.domain.user_technology import UserTechnology

user = User(
    id_="123",
    name="Jane Doe",
    email="jane@ciandt.com",
    photo="http://server.com/jane.png",
)

technologies = [
    UserTechnology(name="javascript", skill=2, endorsements=5),
    UserTechnology(name="python", skill=5, endorsements=0),
    UserTechnology(name="ruby", skill=1, endorsements=0),
    UserTechnology(name="nodejs", skill=3000, endorsements=5000),
]


def test_user_profile_init():
    user_profile = UserProfile(user=user, technologies=technologies)

    assert user_profile.user == user
    assert user_profile.technologies == technologies


def test_user_profile_from_dict():
    user_profile = UserProfile.from_dict(
        {
            "user": {
                "id": "123",
                "name": "Jane Doe",
                "email": "jane@ciandt.com",
                "photo": "http://server.com/jane.png",
            },
            "technologies": [
                {"name": "javascript", "skill": 2, "endorsements": 5},
                {"name": "python", "skill": 5, "endorsements": 0},
                {"name": "ruby", "skill": 1, "endorsements": 0},
                {"name": "nodejs", "skill": 3000, "endorsements": 5000},
            ],
        }
    )

    assert user_profile.user == user
    assert user_profile.technologies == technologies


def test_user_profile_to_dict():
    user_profile_dict = {
        "user": {
            "id": "123",
            "name": "Jane Doe",
            "email": "jane@ciandt.com",
            "photo": "http://server.com/jane.png",
        },
        "technologies": [
            {"name": "javascript", "skill": 2, "endorsements": 5},
            {"name": "python", "skill": 5, "endorsements": 0},
            {"name": "ruby", "skill": 1, "endorsements": 0},
            {"name": "nodejs", "skill": 3000, "endorsements": 5000},
        ],
    }

    user_profile = UserProfile(user=user, technologies=technologies)

    assert user_profile.to_dict() == user_profile_dict


def test_user_profile_comparison():
    user_profile_dict = {
        "user": {
            "id": "123",
            "name": "Jane Doe",
            "email": "jane@ciandt.com",
            "photo": "http://server.com/jane.png",
        },
        "technologies": [
            {"name": "javascript", "skill": 2, "endorsements": 5},
            {"name": "python", "skill": 5, "endorsements": 0},
        ],
    }

    user_profile1 = UserProfile.from_dict(user_profile_dict)
    user_profile2 = UserProfile.from_dict(user_profile_dict)

    assert user_profile1 == user_profile2


def test_user_profile_repr():
    user_profile = UserProfile(user=user, technologies=technologies)

    assert (
        repr(user_profile)
        == "UserProfile(User(id_='123', name='Jane Doe', email='jane@ciandt.com', photo='http://server.com/jane.png'), [UserTechnology(name='javascript', skill=2, endorsements=5), UserTechnology(name='python', skill=5, endorsements=0), UserTechnology(name='ruby', skill=1, endorsements=0), UserTechnology(name='nodejs', skill=3000, endorsements=5000)])"
    )
