"""
Utils package initializer
Exposes all handlers, helpers, and api functions for easy import
"""

# Handlers (inside utils)
from .start import start_handler
from .keygen import keygen_handler
from .usage import usage_handler
from .plans import plans_handler
from .admins import admin_handler

# Helpers
from .helpers import (
    generate_random_string,
    current_time,
    is_admin,
    format_plan,
)

# API functions
from .api import (
    youtube_search,
    get_video_info,
)

__all__ = [
    # Handlers
    "start_handler",
    "keygen_handler",
    "usage_handler",
    "plans_handler",
    "admin_handler",

    # Helpers
    "generate_random_string",
    "current_time",
    "is_admin",
    "format_plan",

    # API
    "youtube_search",
    "get_video_info",
]
