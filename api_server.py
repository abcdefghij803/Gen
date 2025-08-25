from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime, timezone, timedelta
from functools import wraps
from config import settings
from db import create_key, get_key, get_keys_for_user, reset_counters_if_needed, charge_usage, set_key
from api import yt_search_sync, yt_stream_sync

app = Flask(__name__, template_folder='templates')

@app.get('/')
def home():
    return redirect(url_for('generate_page'))

@app.get('/generate')
def generate_page():
    return render_template('generate.html', support_url=settings.SUPPORT_URL)

@app.get('/dashboard')
def dashboard_page():
    uid = request.args.get('user_id')
    if not uid:
        return redirect(url_for('generate_page'))
    try:
        uid = int(uid)
    except:
        return 'invalid user_id', 400
    keys = get_keys_for_user(uid)
    for k in keys:
        if isinstance(k.get('expires_at'), datetime):
            k['expires_at_iso'] = k['expires_at'].isoformat()
    return render_template('dashboard.html', user_id=uid, keys=keys, base_url=settings.BASE_PUBLIC_URL)

def admin_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        tok = request.headers.get('X-Admin-Token','')
        if tok != settings.ADMIN_API_TOKEN:
            return jsonify({'error':'unauthorized'}),401
        return f(*a, **kw)
    return wrapper

@app.post('/api/generate')
def api_generate():
    data = request.get_json(force=True)
    uid = int(data.get('user_id'))
    plan = (data.get('plan') or 'free').lower()
    days = data.get('days')
    days = int(days) if days else None
    doc = create_key(uid, plan, days)
    return jsonify({'api_key':doc['_id'],'plan':doc['plan'],'expires_at':doc['expires_at'].isoformat()})

@app.get('/api/validate')
def api_validate():
    key = request.args.get('key')
    if not key:
        return jsonify({'error':'key required'}),400
    doc = get_key(key)
    if not doc:
        return jsonify({'valid':False,'reason':'not_found'})
    if doc.get('banned'):
        return jsonify({'valid':False,'reason':'banned'})
    if doc['expires_at'] < datetime.now(timezone.utc):
        return jsonify({'valid':False,'reason':'expired'})
    return jsonify({'valid':True,'plan':doc['plan'],'expires_at':doc['expires_at'].isoformat()})

@app.get('/api/search')
def api_search():
    key = request.args.get('key')
    q = request.args.get('query','').strip()
    if not key or not q:
        return jsonify({'error':'key&query required'}),400
    doc = get_key(key)
    if not doc:
        return jsonify({'error':'invalid_key'}),403
    if doc.get('banned'):
        return jsonify({'error':'banned'}),403
    if doc['expires_at'] < datetime.now(timezone.utc):
        return jsonify({'error':'expired'}),403
    doc = reset_counters_if_needed(doc)
    limits = settings.PLANS.get(doc['plan'],{})
    if doc['minute_count'] >= limits.get('per_min',999999):
        return jsonify({'error':'per_min_limit'}),429
    if doc['daily_count'] >= limits.get('daily',999999):
        return jsonify({'error':'daily_limit'}),429
    charge_usage(doc, video=False)
    res = yt_search_sync(q, limit=int(request.args.get('limit',8)))
    return jsonify(res)

@app.get('/api/stream/<video_id>')
def api_stream(video_id):
    key = request.args.get('key')
    want_video = request.args.get('video','false').lower() in ('1','true','yes','y')
    if not key:
        return jsonify({'error':'key required'}),400
    doc = get_key(key)
    if not doc:
        return jsonify({'error':'invalid_key'}),403
    if doc.get('banned'):
        return jsonify({'error':'banned'}),403
    if doc['expires_at'] < datetime.now(timezone.utc):
        return jsonify({'error':'expired'}),403
    doc = reset_counters_if_needed(doc)
    limits = settings.PLANS.get(doc['plan'],{})
    if doc['minute_count'] >= limits.get('per_min',999999):
        return jsonify({'error':'per_min_limit'}),429
    if doc['daily_count'] >= limits.get('daily',999999):
        return jsonify({'error':'daily_limit'}),429
    if want_video and doc.get('video_count',0) >= limits.get('videos',999999):
        return jsonify({'error':'video_limit'}),429
    charge_usage(doc, video=want_video)
    res = yt_stream_sync(video_id, want_video)
    return jsonify(res)

@app.post('/api/admin/generate_unlimited')
@admin_required
def admin_generate_unlimited():
    data = request.get_json(force=True)
    uid = int(data.get('user_id'))
    plan = (data.get('plan') or 'pro').lower()
    days = 365*100
    doc = create_key(uid, plan, days)
    return jsonify({'api_key':doc['_id'],'plan':doc['plan'],'expires_at':doc['expires_at'].isoformat()})
