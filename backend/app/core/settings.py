from os import getenv
from dotenv import load_dotenv

class Settings:

    load_dotenv()
    PG_URL = getenv('PG_URL')
