import os


class Config(object):
    DEBUG = False
    TESTING = False
    ALLOWED_DOMAINS = ["ciandt.com"]

    @property
    def GOOGLE_APPLICATION_ID(self):
        return os.environ.get("GOOGLE_APPLICATION_ID")

    @property
    def TECH_GALLERY_SERVICE_ACCOUNT(self):
        return os.environ.get("TECH_GALLERY_SERVICE_ACCOUNT")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


def load_configs(app):
    environments = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
        "testing": TestingConfig,
    }

    if "ENV" not in app.config is None:
        raise ValueError("No ENV set for application")

    if app.config.get("ENV") not in environments:
        raise ValueError("Invalid ENV set for application")

    app.config.from_object(environments.get(app.config.get("ENV"))())
    return app
