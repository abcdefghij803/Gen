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
