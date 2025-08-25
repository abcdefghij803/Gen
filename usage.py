from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from config import settings
from db import get_keys_for_user
from api import api as yta
import html

def register(app):
    @app.on_callback_query(filters.regex('^usage$'))
    async def usage_cb(c, q: CallbackQuery):
        keys = get_keys_for_user(q.from_user.id)
        if not keys:
            await q.message.edit_text("❌ You don't have a key yet. Tap *Get API Key*." )
            return
        doc = keys[0]
        limits = settings.PLANS.get(doc['plan'], {})
        txt = (f"📊 **Usage**\n\n"
            f"Plan: {doc['plan']}\n"
            f"Daily: {doc['daily_count']} / {limits.get('daily')}\n"
            f"Per-min: {doc['minute_count']} / {limits.get('per_min')}\n"
            f"Videos: {doc.get('video_count',0)} / {limits.get('videos')}\n"
            f"Expires: `<code>{doc['expires_at'].isoformat()}</code>`\n")
        kb = InlineKeyboardMarkup([[InlineKeyboardButton('🌐 View API (Validate)', url=f"{settings.BASE_PUBLIC_URL}/api/validate?key={doc['_id']}")]])
        await q.message.edit_text(txt, reply_markup=kb, parse_mode='html')

    @app.on_inline_query()
    async def inline_search(c, inline_query):
        qtext = inline_query.query or ''
        if not qtext.startswith('yt '):
            return
        query_text = qtext[len('yt '):].strip()
        if not query_text:
            await inline_query.answer([], cache_time=1)
            return
        res = yta.yt_search_sync(query_text, limit=6)
        items = res.get('items', []) if isinstance(res, dict) else []
        articles = []
        for i, it in enumerate(items[:5]):
            title = it.get('title') or 'No title'
            url = it.get('url') or '#'
            duration = it.get('duration') or 'Unknown'
            content = InputTextMessageContent(f"🎬 <b>{html.escape(title)}</b>\n🔗 {url}\n⏱ {duration}", parse_mode='html')
            articles.append(InlineQueryResultArticle(id=f"r{i}", title=title, description=f"⏱ {duration}", input_message_content=content))
        if not articles:
            articles = [InlineQueryResultArticle(id='no', title='No results', input_message_content=InputTextMessageContent('No results'))]
        await inline_query.answer(articles, cache_time=60)
