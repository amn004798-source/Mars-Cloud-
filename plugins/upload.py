from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import save_file, add_user
from helpers.utils import generate_token, format_size
from config.settings import STORAGE_CHANNEL

@Client.on_message(filters.document | filters.video | filters.photo | filters.audio | filters.voice | filters.sticker | filters.animation)
async def upload_file(client, message):
    user = message.from_user
    add_user(user.id, user.username)
    
    # Determine file info
    file_obj = None
    file_name = "Unknown"
    file_size = 0
    file_id = None
    
    if message.document:
        file_obj = message.document
        file_name = file_obj.file_name or "document"
        file_size = file_obj.file_size
        file_id = file_obj.file_id
    elif message.video:
        file_obj = message.video
        file_name = file_obj.file_name or "video.mp4"
        file_size = file_obj.file_size
        file_id = file_obj.file_id
    elif message.photo:
        file_obj = message.photo[-1]
        file_name = "photo.jpg"
        file_size = file_obj.file_size
        file_id = file_obj.file_id
    elif message.audio:
        file_obj = message.audio
        file_name = file_obj.file_name or "audio.mp3"
        file_size = file_obj.file_size
        file_id = file_obj.file_id
    elif message.voice:
        file_obj = message.voice
        file_name = "voice.ogg"
        file_size = file_obj.file_size
        file_id = file_obj.file_id
    elif message.sticker:
        file_obj = message.sticker
        file_name = "sticker.webp"
        file_size = file_obj.file_size
        file_id = file_obj.file_id
    elif message.animation:
        file_obj = message.animation
        file_name = file_obj.file_name or "animation.gif"
        file_size = file_obj.file_size
        file_id = file_obj.file_id
    else:
        await message.reply("Unsupported file type.")
        return

    # Forward/copy to storage channel
    try:
        sent = await message.copy(STORAGE_CHANNEL)
        msg_id = sent.id
    except Exception as e:
        await message.reply(f"Storage error: {e}")
        return

    # Generate token
    token = generate_token()
    
    # Save to DB
    save_file(user.id, user.username, token, file_id, msg_id, file_name, file_size)

    # Build share link
    link = f"https://t.me/{client.me.username}?start={token}"
    size_str = format_size(file_size)
    
    reply_text = f"""✅ **File Uploaded Successfully**

📄 **File Name:** `{file_name}`
📦 **Size:** {size_str}
🔗 **Share Link:** {link}"""

    # Inline button to copy link
    await message.reply(reply_text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Copy Link", callback_data=f"copy_{token}")]
    ]))

@Client.on_callback_query(filters.regex(r"^copy_"))
async def copy_link(client, callback):
    token = callback.data.split("_")[1]
    link = f"https://t.me/{client.me.username}?start={token}"
    await callback.answer(f"Link copied: {link}", show_alert=True)
