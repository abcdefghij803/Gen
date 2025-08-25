import yt_dlp
import aiohttp, asyncio
from urllib.parse import urlencode
from config import settings

def yt_search_sync(query: str, limit: int = 8):
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
            data = ydl.extract_info(f'ytsearch{limit}:{query}', download=False)
    except Exception as e:
        return {'error': str(e), 'items': []}
    entries = data.get('entries', []) if data else []
    out = []
    for e in entries:
        vid = e.get('id')
        out.append({'id': vid, 'title': e.get('title'), 'url': e.get('url') or (f'https://www.youtube.com/watch?v={vid}' if vid else None), 'duration': e.get('duration'), 'uploader': e.get('uploader') or e.get('channel')})
    return {'items': out}

def yt_stream_sync(video_id: str, want_video: bool = False):
    opts = {'format': 'bestvideo+bestaudio/best'} if want_video else {'format': 'bestaudio'}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
    except Exception as e:
        return {'error': str(e)}
    stream_url = info.get('url')
    if not stream_url and 'formats' in info and info['formats']:
        stream_url = info['formats'][-1].get('url')
    return {'video_id': video_id, 'title': info.get('title'), 'duration': info.get('duration'), 'channel': info.get('uploader') or info.get('channel'), 'stream_url': stream_url, 'formats': info.get('formats', [])}

async def fetch_youtube_data_external(query: str, key: str = None, limit: int = 8):
    base = settings.BASE_PUBLIC_URL.rstrip('/') if settings.BASE_PUBLIC_URL else None
    if not base:
        return {'error': 'No BASE_PUBLIC_URL configured'}
    params = {'query': query, 'limit': limit}
    if key: params['key'] = key
    url = f'{base}/api/search?{urlencode(params)}'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    return await resp.json()
                return {'error': f'HTTP {resp.status}'}
    except asyncio.TimeoutError:
        return {'error': 'timeout'}
    except Exception as e:
        return {'error': str(e)}
