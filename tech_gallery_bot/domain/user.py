class User:
    def __init__(self, id_, name, email, photo):
        self.id = id_
        self.name = name
        self.email = email
        self.photo = photo

    @classmethod
    def from_dict(cls, dict_):
        return User(
            id_=dict_["id"],
            name=dict_["name"],
            email=dict_["email"],
            photo=dict_["photo"],
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "photo": self.photo,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return "{}(id_={!r}, name={!r}, email={!r}, photo={!r})".format(
            self.__class__.__name__, self.id, self.name, self.email, self.photo
        )
