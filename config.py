import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    print(SECRET_KEY)
#    SQLALCHEMY_DATABASE_URI = "sqlite:///F:\\DB.Browser.for.SQLite-v3.13.1-win64\\riget_data.db"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    print(SQLALCHEMY_DATABASE_URI)
    FLASK_ADMIN_SWATCH = "slate"
    UPLOAD_FOLDER = "app/static"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False