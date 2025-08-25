import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv('BOT_TOKEN','')
    API_ID = int(os.getenv('API_ID','0') or 0)
    API_HASH = os.getenv('API_HASH','')
    MONGO_URI = os.getenv('MONGO_URI','mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME','keybot_db')
    BASE_PUBLIC_URL = os.getenv('BASE_PUBLIC_URL','http://localhost:8080')
    SUPPORT_URL = os.getenv('SUPPORT_URL','https://t.me/your_support')
    UPGRADE_URL = os.getenv('UPGRADE_URL','https://t.me/your_admin')
    ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS','').split(',') if x.strip().isdigit()]
    ADMIN_API_TOKEN = os.getenv('ADMIN_API_TOKEN','supersecrettoken')
    PLANS = {
        'free': {'daily':700,'per_min':60,'videos':15,'days':7},
        'premium': {'daily':3000,'per_min':180,'videos':50,'days':30},
        'pro': {'daily':7500,'per_min':400,'videos':150,'days':90},
    }

settings = Settings()
