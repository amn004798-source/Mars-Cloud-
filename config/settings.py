import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STORAGE_CHANNEL = int(os.getenv("STORAGE_CHANNEL_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))
MONGODB_URI = os.getenv("MONGODB_URI")
