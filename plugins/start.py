from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import add_user

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    user = message.from_user
    add_user(user.id, user.username or "Unknown")
    
    # If token is passed in start parameter (for sharing)
    if len(message.command) > 1:
        token = message.command[1]
        # Handle token sharing – we'll redirect to share.py
        await client.send_message(message.chat.id, f"📥 Retrieving your file...")
        # Actually we'll handle it via separate handler; for now we pass to share plugin via filters.
        # We'll implement share logic in share.py and use a separate handler.
        # To avoid duplication, we'll just send a message and let share.py handle via command filter.
        # We can also call the share function directly, but we'll let the filter catch it.
        # For simplicity, we just forward to the share handler by sending the same message again?
        # Actually we can manually trigger the share function by calling it.
        # But better: we define a separate handler for start with token in share.py.
        # For now, we'll just show welcome and ignore token; token handling will be in share.py with a filter.
        pass
    
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
