from functools import wraps
from pyrogram import filters
from config.settings import ADMIN_ID
import time

def admin_only(func):
    @wraps(func)
    async def wrapper(client, message):
        if message.from_user.id == ADMIN_ID:
            return await func(client, message)
        else:
            await message.reply("⛔ You are not authorised.")
    return wrapper

# simple cooldown (prevent spam)
cooldown_dict = {}
def cooldown(seconds=10):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message):
            user_id = message.from_user.id
            now = time.time()
            if user_id in cooldown_dict and now - cooldown_dict[user_id] < seconds:
                await message.reply("⏳ Please wait before uploading again.")
                return
            cooldown_dict[user_id] = now
            return await func(client, message)
        return wrapper
    return decorator
