"""
Handlers package initializer
Automatically imports and exposes all handlers as a list.
"""

from . import start, keygen, usage, plans, admin

# List of all handler register functions
ALL_HANDLERS = [
    start.register,
    keygen.register,
    usage.register,
    plans.register,
    admin.register,
]

__all__ = ["ALL_HANDLERS"]


"""
Utils package initializer
Exposes helpers and api functions in one place
"""

from . import helpers, api

ALL_HELPERS = [
    helpers.generate_random_string,
    helpers.current_time,
    helpers.is_admin,
    helpers.format_plan,
]

ALL_API = [
    api.youtube_search,
    api.get_video_info,
]

__all__ = ["ALL_HELPERS", "ALL_API"]
