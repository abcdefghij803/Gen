from pyrogram import filters
from pyrogram.types import Message
from config import settings
from database.db import get_key, set_key, create_key

def _is_admin(uid: int) -> bool:
    return uid in settings.ADMIN_IDS

def register(app):
    @app.on_message(filters.command('ban') & filters.private)
    async def ban(c, m: Message):
        if not _is_admin(m.from_user.id): return
        parts = m.text.split(maxsplit=1)
        if len(parts) < 2: return await m.reply_text('Usage: /ban <KEY>')
        k = parts[1].strip()
        if not get_key(k): return await m.reply_text('Key not found')
        set_key(k, {'banned': True})
        await m.reply_text('✅ Key banned.')

    @app.on_message(filters.command('unban') & filters.private)
    async def unban(c, m: Message):
        if not _is_admin(m.from_user.id): return
        parts = m.text.split(maxsplit=1)
        if len(parts) < 2: return await m.reply_text('Usage: /unban <KEY>')
        k = parts[1].strip()
        if not get_key(k): return await m.reply_text('Key not found')
        set_key(k, {'banned': False})
        await m.reply_text('✅ Key unbanned.')

    @app.on_message(filters.command('gen') & filters.private)
    async def gen(c, m: Message):
        if not _is_admin(m.from_user.id): return
        parts = m.text.split()
        if len(parts) < 2: return await m.reply_text('Usage: /gen <user_id> [plan] [days]')
        user_id = int(parts[1])
        plan = parts[2] if len(parts) >= 3 else 'free'
        days = int(parts[3]) if len(parts) >= 4 else settings.PLANS.get(plan, {}).get('days', 7)
        doc = create_key(user_id, plan, days)
        await m.reply_text(f"✅ Key created for {user_id}: `{doc['_id']}` (plan {plan})")
