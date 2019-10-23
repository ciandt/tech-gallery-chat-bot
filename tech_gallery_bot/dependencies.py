from google.cloud.datastore import Client

from tech_gallery_bot.repositories import UserRepository, UserProfileRepository


def _get_datastore_client(*, config):
    if not isinstance(config, dict):
        raise TypeError("config should be a dict")

    if "TECH_GALLERY_SERVICE_ACCOUNT" not in config:
        raise ValueError("TECH_GALLERY_SERVICE_ACCOUNT entry not found in config")

    return Client.from_service_account_json(
        config["TECH_GALLERY_SERVICE_ACCOUNT"], namespace="prod"
    )


def get_dependencies(*, config):
    client = _get_datastore_client(config=config)

    return {
        "user_repository": UserRepository(client),
        "user_profile_repository": UserProfileRepository(client),
    }
