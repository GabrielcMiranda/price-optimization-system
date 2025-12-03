from os import getenv
from dotenv import load_dotenv

class Settings:

    load_dotenv()
    PG_URL = getenv('PG_URL')
    SECRET_KEY = getenv('SECRET_KEY')
    ALGORITHM = getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 600))   