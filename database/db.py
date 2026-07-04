from pymongo import MongoClient
from config.settings import MONGODB_URI, STORAGE_CHANNEL
import datetime

client = MongoClient(MONGODB_URI)
db = client["mars_cloud"]

files_col = db["files"]
users_col = db["users"]

def add_user(user_id, username):
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({
            "user_id": user_id,
            "username": username,
            "joined": datetime.datetime.now()
        })

def save_file(user_id, username, token, file_id, message_id, file_name, file_size):
    files_col.insert_one({
        "user_id": user_id,
        "username": username,
        "token": token,
        "file_id": file_id,
        "message_id": message_id,
        "channel_id": STORAGE_CHANNEL,
        "file_name": file_name,
        "file_size": file_size,
        "upload_time": datetime.datetime.now(),
        "download_count": 0
    })

def get_file_by_token(token):
    return files_col.find_one({"token": token})

def get_user_files(user_id):
    return files_col.find({"user_id": user_id}).sort("upload_time", -1)

def increment_download(token):
    files_col.update_one({"token": token}, {"$inc": {"download_count": 1}})

def get_total_users():
    return users_col.count_documents({})

def get_total_files():
    return files_col.count_documents({})

def get_today_uploads():
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return files_col.count_documents({"upload_time": {"$gte": today}})

def get_today_downloads():
    # We don't store download timestamps in this version; can be added if needed
    return 0
