class Config:
    # Utilizar llave diference y alphanumeric
    SECRET_KEY = 'codigofacilito'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'test.mbrito@gmail.com'
    MAIL_PASSWORD = 'TestMildredBrito123'  # ALWAYS safer to create an environment variable


class TestConfig(Config):
    # New database for testing
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/project_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEST = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'test': TestConfig
}
