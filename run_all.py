from threading import Thread
import time
from api_server import app as flask_app
from bot import app as bot_app

def run_api():
    try:
        from waitress import serve
        serve(flask_app, host='0.0.0.0', port=8080)
    except Exception:
        flask_app.run(host='0.0.0.0', port=8080)

def run_bot():
    bot_app.run()

if __name__ == '__main__':
    t = Thread(target=run_api, daemon=True)
    t.start()
    time.sleep(1)
    run_bot()
