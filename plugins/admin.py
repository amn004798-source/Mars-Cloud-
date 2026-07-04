from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.decorators import admin_only
from database.db import (
    get_total_users, get_total_files, get_today_uploads, get_total_storage,
    get_banned_users, ban_user, unban_user, is_banned,
    delete_file_by_token, search_files, get_all_users,
    get_user_files
)
from helpers.utils import format_size
import datetime

# ---------- Admin Panel ----------
@Client.on_message(filters.command("admin") & admin_only)
async def admin_panel(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Stats", callback_data="admin_stats")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban")],
        [InlineKeyboardButton("✅ Unban User", callback_data="admin_unban")],
        [InlineKeyboardButton("🗑️ Delete File", callback_data="admin_delete")],
        [InlineKeyboardButton("🔍 Search File", callback_data="admin_search")],
        [InlineKeyboardButton("👥 Users List", callback_data="admin_users")],
        [InlineKeyboardButton("❌ Close", callback_data="admin_close")]
    ])
    await message.reply("👑 **Admin Panel**\nChoose an action:", reply_markup=buttons)

# ---------- Stats ----------
@Client.on_callback_query(filters.regex(r"^admin_stats$") & admin_only)
async def admin_stats_callback(client, callback):
    total_users = get_total_users()
    total_files = get_total_files()
    today_uploads = get_today_uploads()
    banned_count = len(get_banned_users())
    total_size = get_total_storage()

    text = f"""📊 **Statistics**

👥 Total Users: {total_users}
📁 Total Files: {total_files}
📤 Today's Uploads: {today_uploads}
🚫 Banned Users: {banned_count}
💾 Total Storage Used: {format_size(total_size)}
"""
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_back")]]))

# ---------- Broadcast ----------
@Client.on_message(filters.command("broadcast") & admin_only)
async def broadcast_cmd(client, message):
    if not message.reply_to_message:
        await message.reply("Reply to a message to broadcast it to all users.")
        return
    from database.db import get_db
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    users = cur.fetchall()
    conn.close()
    count = 0
    for user in users:
        try:
            await message.reply_to_message.copy(user['user_id'])
            count += 1
        except Exception:
            pass
    await message.reply(f"✅ Broadcast sent to {count} users.")

# ---------- Ban / Unban ----------
@Client.on_message(filters.command("ban") & admin_only)
async def ban_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /ban <user_id>")
        return
    try:
        user_id = int(message.command[1])
    except:
        await message.reply("Invalid user ID.")
        return
    ban_user(user_id)
    await message.reply(f"✅ User {user_id} banned.")

@Client.on_message(filters.command("unban") & admin_only)
async def unban_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /unban <user_id>")
        return
    try:
        user_id = int(message.command[1])
    except:
        await message.reply("Invalid user ID.")
        return
    unban_user(user_id)
    await message.reply(f"✅ User {user_id} unbanned.")

# ---------- Delete File ----------
@Client.on_message(filters.command("delete") & admin_only)
async def delete_file_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /delete <token>")
        return
    token = message.command[1]
    if delete_file_by_token(token):
        await message.reply(f"✅ File with token `{token}` deleted.")
    else:
        await message.reply(f"❌ File with token `{token}` not found.")

# ---------- Search File ----------
@Client.on_message(filters.command("search") & admin_only)
async def search_file_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /search <filename>")
        return
    query = ' '.join(message.command[1:])
    results = search_files(query)
    if not results:
        await message.reply("No files found.")
        return
    text = "🔍 **Search Results:**\n\n"
    for f in results[:10]:
        text += f"📄 `{f['file_name']}` – Token: `{f['token']}` – by `{f['user_id']}`\n"
    if len(results) > 10:
        text += f"\n... and {len(results)-10} more."
    await message.reply(text)

# ---------- Users List ----------
@Client.on_message(filters.command("userslist") & admin_only)
async def userslist_cmd(client, message):
    users = get_all_users(limit=50, offset=0)
    if not users:
        await message.reply("No users yet.")
        return
    text = "👥 **Recent Users (last 50):**\n\n"
    for u in users:
        text += f"👤 `{u['user_id']}` – @{u['username'] or 'N/A'} – joined {u['joined'][:10]}\n"
    await message.reply(text)

# ---------- Callbacks ----------
@Client.on_callback_query(filters.regex(r"^admin_"))
async def admin_callback(client, callback):
    data = callback.data
    if data == "admin_back":
        await admin_panel(client, callback.message)
        await callback.answer()
        return
    elif data == "admin_close":
        await callback.message.delete()
        await callback.answer("Closed.")
        return
    elif data == "admin_broadcast":
        await callback.message.edit_text("📢 Reply to a message with /broadcast to broadcast it.")
    elif data == "admin_ban":
        await callback.message.edit_text("🚫 Use /ban <user_id>")
    elif data == "admin_unban":
        await callback.message.edit_text("✅ Use /unban <user_id>")
    elif data == "admin_delete":
        await callback.message.edit_text("🗑️ Use /delete <token>")
    elif data == "admin_search":
        await callback.message.edit_text("🔍 Use /search <filename>")
    elif data == "admin_users":
        await callback.message.edit_text("👥 Use /userslist")
    await callback.answer()

# Also allow direct commands
@Client.on_message(filters.command("stats") & admin_only)
async def stats_cmd(client, message):
    # Simulate callback
    await admin_stats_callback(client, message)
