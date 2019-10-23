class UserTechnology:
    def __init__(self, name, skill, endorsements):
        self.name = name
        self.skill = skill
        self.endorsements = endorsements

    @classmethod
    def from_dict(cls, dict_):
        return UserTechnology(
            name=dict_["name"],
            skill=dict_["skill"],
            endorsements=dict_["endorsements"],
        )

    def to_dict(self):
        return {
            "name": self.name,
            "skill": self.skill,
            "endorsements": self.endorsements,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return "{}(name={!r}, skill={!r}, endorsements={!r})".format(
            self.__class__.__name__, self.name, self.skill, self.endorsements
        )
