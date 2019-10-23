from tech_gallery_bot.domain.user import User

from tech_gallery_bot.domain.user_technology import UserTechnology


class UserProfile:
    def __init__(self, user, technologies):
        self.user = user
        self.technologies = technologies

    @classmethod
    def from_dict(cls, dict_):
        return UserProfile(
            user=User.from_dict(dict_["user"]),
            technologies=[UserTechnology.from_dict(t) for t in dict_["technologies"]],
        )

    def to_dict(self):
        return {
            "user": self.user.to_dict(),
            "technologies": [t.to_dict() for t in self.technologies],
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return "{}({!r}, {!r})".format(
            self.__class__.__name__, self.user, self.technologies
        )
