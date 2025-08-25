from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import settings

def register(app):
    @app.on_callback_query(filters.regex('^plans$'))
    async def plans(c, q: CallbackQuery):
        p = settings.PLANS
        txt = ("💎 <b>Plans</b>\n\n"
            f"🆓 Free — {p['free']['days']} days | {p['free']['daily']} req/day | {p['free']['per_min']} req/min | {p['free']['videos']} videos\n\n"
            f"💠 Premium — {p['premium']['days']} days | {p['premium']['daily']} req/day | {p['premium']['per_min']} req/min | {p['premium']['videos']} videos\n\n"
            f"👑 Pro — {p['pro']['days']} days | {p['pro']['daily']} req/day | {p['pro']['per_min']} req/min | {p['pro']['videos']} videos\n"
        )
        kb = InlineKeyboardMarkup([[InlineKeyboardButton('🚀 Upgrade / Contact', url=settings.UPGRADE_URL)]])
        await q.message.edit_text(txt, reply_markup=kb, parse_mode='html')
