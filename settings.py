import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_ID = os.environ.get('api_id')
API_HASH = os.environ.get("api_hash")
PHONE = os.environ.get("phone")