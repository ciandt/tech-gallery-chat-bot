from google.cloud.datastore import Client

from tech_gallery_bot.domain import User


class UserRepository:
    def __init__(self, client):
        if not isinstance(client, Client):
            raise TypeError(f"client should be a Datastore Client")

        self._client = client

    def find_by_email(self, email):
        query = self._client.query(kind="TechGalleryUser")
        query.add_filter("email", "=", email)

        results = list(query.fetch(limit=1))

        if len(results) == 0:
            return None

        user_dict = dict(results[0])
        user_dict["id"] = results[0].id

        return User.from_dict(user_dict)
