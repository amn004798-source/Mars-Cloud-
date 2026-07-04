from pyrogram import Client, filters
from helpers.decorators import admin_only
from database.db import get_total_users, get_total_files, get_today_uploads, files_col, users_col
from helpers.utils import format_size

@Client.on_message(filters.command("admin") & admin_only)
async def admin_panel(client, message):
    text = f"""📊 **Admin Panel**

Total Users: {get_total_users()}
Total Files: {get_total_files()}
Today's Uploads: {get_today_uploads()}
"""
    await message.reply(text)

@Client.on_message(filters.command("stats") & admin_only)
async def stats(client, message):
    total_size = 0
    for f in files_col.find():
        total_size += f['file_size']
    text = f"""📈 **Statistics**
Total Files: {get_total_files()}
Total Users: {get_total_users()}
Today Uploads: {get_today_uploads()}
Total Storage Used: {format_size(total_size)}
"""
    await message.reply(text)

@Client.on_message(filters.command("broadcast") & admin_only)
async def broadcast(client, message):
    if not message.reply_to_message:
        await message.reply("Reply to a message to broadcast.")
        return
    users = users_col.find()
    count = 0
    for user in users:
        try:
            await message.reply_to_message.copy(user['user_id'])
            count += 1
        except:
            pass
    await message.reply(f"Broadcast sent to {count} users.")

# Additional admin commands like ban, delete file can be added similarly.
