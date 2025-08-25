import logging
from pyrogram import Client
from config import settings

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Initialize Pyrogram Client
app = Client(
    "KeyBot",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN,
    workers=16
)

# Import handlers and register them
from handlers import start, keygen, usage, plans, admin

start.register(app)
keygen.register(app)
usage.register(app)
plans.register(app)
admin.register(app)


if __name__ == "__main__":
    logging.info("🤖 Starting KeyBot...")
    app.run()
