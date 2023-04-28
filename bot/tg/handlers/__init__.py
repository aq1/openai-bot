from . import (
    start_handler,
    db_log_handler,
    file_handler,
    set_language_handler,
)

__all__ = [
    'HANDLER_GROUPS',
]

HANDLER_GROUPS = (
    (
        start_handler.handler,
        file_handler.handler,
        set_language_handler.handler,
    ),
    (
        db_log_handler.handler,
    ),
)
