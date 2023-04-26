from . import (
    start_handler,
    log_handler,
    file_handler,
)

__all__ = [
    'HANDLER_GROUPS',
]

HANDLER_GROUPS = (
    (
        start_handler.handler,
        file_handler.handler,
    ),
    (
        log_handler.handler,
    ),
)
