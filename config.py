import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_DELTA = timedelta(seconds=60 * 60 * 24)
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class HerokuConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://bfffgjpkqclazl:60664ad9d2cf64ba92bc6bd36417b4c368e0b6ec19d6a1a9e69609c4c13fec10@ec2-54-83-55-125.compute-1.amazonaws.com:5432/dcct34fdpcvmlj'


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig
}
