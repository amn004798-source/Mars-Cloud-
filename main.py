from pyrogram import Client
from config.settings import API_ID, API_HASH, BOT_TOKEN
import plugins  # this imports all plugins (start, upload, share, myfiles, admin)

app = Client("mars_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

if __name__ == "__main__":
    app.run()
