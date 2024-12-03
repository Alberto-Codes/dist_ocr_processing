import os

from  dotenv import load_dotenv
from keyring import get_credential
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/ocr.db")
ONLINE_DATABASE_URL = os.getenv("ONLINE_DATABASE_URL")
ONLINE_TARGET_DB = os.getenv("ONLINE_TARGET_DB")

_engines={}
_SessionLocals = {}

def get_online_database_url():
    user = get_credential("ABCDB", None).username
    password = get_credential("ABCDB", None).password
    return ONLINE_DATABASE_URL.format(user=user, password=password, database=ONLINE_TARGET_DB)

