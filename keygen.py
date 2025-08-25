from pyrogram import filters
from pyrogram.types import CallbackQuery
from config import settings
from db import create_key, get_keys_for_user, ensure_user
from helpers import plan_badge

def register(app):
    @app.on_callback_query(filters.regex('^get_key$'))
    async def gen_key(c, q: CallbackQuery):
        user_id = q.from_user.id
        ensure_user(user_id)
        # always generate fresh key
        doc = create_key(user_id, 'free')
        from pyrogram import types
        kb = types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton('📋 Copy Key', url=f"https://t.me/share/url?url={doc['_id']}")],
            [types.InlineKeyboardButton('🌐 Validate', url=f"{settings.BASE_PUBLIC_URL}/api/validate?key={doc['_id']}")],
            [types.InlineKeyboardButton('📊 Dashboard', url=f"{settings.BASE_PUBLIC_URL}/dashboard?user_id={user_id}")],
        ])
        await q.message.edit_text(f"✅ New API Key generated\n\n🔑 <code>{doc['_id']}</code>\nPlan: {plan_badge(doc['plan'])}\nExpires: <code>{doc['expires_at'].isoformat()}</code>", reply_markup=kb, parse_mode='html')
