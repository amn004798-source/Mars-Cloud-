import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
from config.settings import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "mars_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    app.run()
