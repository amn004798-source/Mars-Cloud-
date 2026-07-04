from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import add_user
from helpers.decorators import not_banned

@Client.on_message(filters.command("start") & not_banned)
async def start_command(client, message):
    user = message.from_user
    add_user(user.id, user.username or "Unknown")
    
    text = """🚀 **Welcome to Mars Cloud Storage**

Store and share your files instantly.

**Supported Files:**  
• Videos • Photos • Documents • PDF • ZIP • APK • Audio • Any Telegram-supported file

✨ **Features**  
- Unlimited file uploads  
- Permanent storage  
- Instant unique share links  
- Private storage channel  
- Fast delivery  
- Secure system  
- Easy sharing  

Simply send me any file to get started."""
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Upload File", callback_data="upload")],
        [InlineKeyboardButton("📁 My Files", callback_data="myfiles")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ])
    await message.reply(text, reply_markup=buttons)

@Client.on_callback_query()
async def callback_handler(client, callback):
    data = callback.data
    if data == "upload":
        await callback.answer("Send me any file.")
    elif data == "myfiles":
        await client.send_message(callback.message.chat.id, "/myfiles")
    elif data == "help":
        await callback.message.reply("Send any file to upload. Use /myfiles to see your uploads.")
    elif data == "about":
        await callback.message.reply("Mars Cloud Storage v1.0 – Built with Pyrogram.")
    await callback.answer()
