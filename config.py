import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://tim:3V9LYlUlhpgajimtht7EE1wmjkZfc5sw@dpg-cjbik3vdb61s738csm7g-a.singapore-postgres.render.com/aigo"

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")