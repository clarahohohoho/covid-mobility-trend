from dotenv import load_dotenv
import os

load_dotenv()

# # MySQL Database credentials loaded from the .env file
DATABASE = os.getenv("DATABASE")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")

SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://"
    + DATABASE_USERNAME
    + ":"
    + DATABASE_PASSWORD
    + "@"
    + DATABASE_HOST
    + ":3306/"
    + DATABASE
)
# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
