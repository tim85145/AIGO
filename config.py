import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://tim:jcWp8TX0fAbBDNNJ5yqPRWValFJumLJc@dpg-cjg2p641ja0c739rgr30-a.singapore-postgres.render.com/aigo_owcd"

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")