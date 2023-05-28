import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

WEB_SERVICE_PATH = os.getenv('WEB_SERVICE_PATH')
WEBHOOK_URL = f"{WEB_SERVICE_PATH}/{BOT_TOKEN}"
