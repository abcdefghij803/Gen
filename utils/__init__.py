"""
Combined initializer for Handlers and Utils
This file is optional - just for unified imports
"""

# ------------------ Handlers ------------------ #
from utils.start import start_handler
from utils.keygen import keygen_handler
from utils.usage import usage_handler
from utils.plans import plans_handler
from utils.admin import admin_handler

# ------------------ Utils ------------------ #
from utils.helpers import (
    generate_random_string,
    current_time,
    is_admin,
    format_plan,
)

from utils.api import (
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

    # Utils
    "generate_random_string",
    "current_time",
    "is_admin",
    "format_plan",
    "youtube_search",
    "get_video_info",
]
