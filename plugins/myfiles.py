from pyrogram import Client, filters
from database.db import get_user_files
from helpers.utils import format_size
from helpers.decorators import not_banned

@Client.on_message(filters.command("myfiles") & not_banned)
async def my_files(client, message):
    user_id = message.from_user.id
    files = list(get_user_files(user_id))
    if not files:
        await message.reply("📭 You have no uploaded files.")
        return
    
    text = "📁 **Your Files**\n\n"
    for idx, f in enumerate(files[:10], 1):
        link = f"https://t.me/{client.me.username}?start={f['token']}"
        size = format_size(f['file_size'])
        text += f"{idx}. `{f['file_name']}` – {size} – [Link]({link})\n"
    
    if len(files) > 10:
        text += f"\n... and {len(files)-10} more."
    
    await message.reply(text, disable_web_page_preview=True)
