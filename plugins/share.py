from pyrogram import Client, filters
from database.db import get_file_by_token, increment_download
from config.settings import STORAGE_CHANNEL

@Client.on_message(filters.command("start") & filters.regex(r"start\s+(\w+)"))
async def share_file(client, message):
    token = message.matches[0].group(1)
    file_data = get_file_by_token(token)
    if not file_data:
        await message.reply("❌ Invalid or expired link.")
        return
    
    # Increment download count
    increment_download(token)
    
    # Retrieve file from storage channel
    chat_id = file_data["channel_id"]
    msg_id = file_data["message_id"]
    
    try:
        await client.copy_message(message.chat.id, chat_id, msg_id)
        await message.reply("📥 File delivered.")
    except Exception as e:
        await message.reply(f"Error retrieving file: {e}")
