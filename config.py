import os

class Config:

    SECRET_KEY = "PhotoForensics2026"

    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False