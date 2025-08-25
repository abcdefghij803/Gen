import logging
from pyrogram import Client
from config import settings
logging.basicConfig(level=logging.INFO)
app = Client('KeyBot', api_id=settings.API_ID, api_hash=settings.API_HASH, bot_token=settings.BOT_TOKEN, workers=16)
# register handlers via import side-effects
from handlers import start as h_start, keygen as h_keygen, usage as h_usage, plans as h_plans, admin as h_admin
h_start.register(app)
h_keygen.register(app)
h_usage.register(app)
h_plans.register(app)
h_admin.register(app)
if __name__ == '__main__':
    print('🤖 Starting KeyBot...')
    app.run()
