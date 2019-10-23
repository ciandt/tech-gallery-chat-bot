from google.cloud.datastore import Client

from tech_gallery_bot.domain import User, UserTechnology, UserProfile


class UserProfileRepository:
    def __init__(self, client):
        if not isinstance(client, Client):
            raise TypeError(f"client should be a Datastore Client")

        self._client = client

    def find_by_user(self, user):
        if not isinstance(user, User):
            raise TypeError(f"user should be a User")

        key = self._client.key("UserProfile", f"profile{user.id}")
        result = self._client.get(key)

        if result is None:
            return None

        profile_dict = dict(result)

        technologies = []

        for collection in ["positiveRecItems", "negativeRecItems", "otherItems"]:
            if collection in profile_dict and profile_dict[collection] is not None:
                for key, value in profile_dict[collection].items():
                    technologies.append(
                        UserTechnology(
                            name=value["technologyName"],
                            skill=int(value["skillLevel"]),
                            endorsements=int(value["endorsementQuantity"]),
                        )
                    )

        return UserProfile(user=user, technologies=technologies)
