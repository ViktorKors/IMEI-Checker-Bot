import os
from dotenv import load_dotenv

load_dotenv()

IMEI_API_URL = "https://api.imeicheck.net/v1/checks"
API_URL = "http://localhost:8000/api/check-imei"
API_SANDBOX_TOKEN = os.getenv("API_SANDBOX_TOKEN")
API_AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

AUTHORIZED_USERS = set(map(int, os.getenv("AUTHORIZED_USERS", "").split(",")))
