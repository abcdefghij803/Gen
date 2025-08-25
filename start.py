from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import settings

def register(app):
    @app.on_message(filters.command('start') & filters.private)
    async def start_cmd(c, m: Message):
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton('🎟 Get API Key', callback_data='get_key')],
            [InlineKeyboardButton('📊 My Usage', callback_data='usage'), InlineKeyboardButton('💎 Plans', callback_data='plans')],
            [InlineKeyboardButton('🌐 Dashboard', url=f"{settings.BASE_PUBLIC_URL}/generate")],
            [InlineKeyboardButton('🛟 Support', url=settings.SUPPORT_URL), InlineKeyboardButton('🚀 Upgrade', url=settings.UPGRADE_URL)],
        ])
        await m.reply_text(f"👋 Hello {m.from_user.first_name}!\n\nWelcome to *KeyBot Pro* — API key generator + YouTube streaming API.", reply_markup=kb)
