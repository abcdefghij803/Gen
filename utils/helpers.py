from datetime import timedelta
def fmt_seconds(secs: int) -> str:
    try:
        return str(timedelta(seconds=int(secs)))
    except:
        return 'unknown'
def plan_badge(plan: str) -> str:
    return {'free': '🆓 Free', 'premium': '💠 Premium', 'pro': '👑 Pro'}.get(plan, plan)
