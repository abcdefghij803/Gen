from pymongo import MongoClient
from datetime import datetime, timedelta, timezone, date
import secrets, string
from config import settings

_client = MongoClient(settings.MONGO_URI)
_db = _client[settings.DB_NAME]

keys_col = _db['keys']
users_col = _db['users']

def _new_key():
    alphabet = string.ascii_letters + string.digits
    return 'K_' + ''.join(secrets.choice(alphabet) for _ in range(44))

def ensure_user(user_id: int):
    users_col.update_one({'_id': user_id}, {'$setOnInsert': {'_id': user_id, 'created_at': datetime.now(timezone.utc)}}, upsert=True)

def create_key(user_id: int, plan: str = 'free', days: int = None):
    ensure_user(user_id)
    if plan not in settings.PLANS: plan = 'free'
    days = days if days is not None else settings.PLANS[plan]['days']
    now = datetime.now(timezone.utc).replace(microsecond=0)
    key = _new_key()
    doc = {'_id': key, 'user_id': user_id, 'plan': plan, 'banned': False, 'expires_at': now + timedelta(days=days), 'daily_count':0, 'minute_count':0, 'video_count':0, 'minute_window_start': now, 'day': date.today(), 'created_at': now, 'updated_at': now}
    keys_col.insert_one(doc)
    return doc

def get_key(key: str):
    return keys_col.find_one({'_id': key})

def get_keys_for_user(user_id: int):
    return list(keys_col.find({'user_id': user_id}).sort('expires_at', -1))

def set_key(key: str, data: dict):
    data['updated_at'] = datetime.now(timezone.utc)
    keys_col.update_one({'_id': key}, {'$set': data})
    return keys_col.find_one({'_id': key})

def reset_counters_if_needed(doc: dict):
    changed = False
    now = datetime.now(timezone.utc)
    if (now - doc.get('minute_window_start', now)) >= timedelta(seconds=60):
        doc['minute_window_start'] = now
        doc['minute_count'] = 0
        changed = True
    if doc.get('day') != date.today():
        doc['day'] = date.today()
        doc['daily_count'] = 0
        doc['video_count'] = 0
        changed = True
    if changed:
        set_key(doc['_id'], {'minute_window_start': doc['minute_window_start'], 'minute_count': doc['minute_count'], 'day': doc['day'], 'daily_count': doc['daily_count'], 'video_count': doc['video_count']})
    return doc

def charge_usage(doc: dict, video: bool = False):
    upd = {'minute_count': doc['minute_count'] + 1, 'daily_count': doc['daily_count'] + 1}
    if video:
        upd['video_count'] = doc.get('video_count', 0) + 1
    set_key(doc['_id'], upd)
