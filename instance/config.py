# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "\xd2x\xbb\x85q/"


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
