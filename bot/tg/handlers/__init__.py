from . import (
    start_handler,
    db_log_handler,
    log_handler,
    file_handler,
    set_language_handler,
    call_task_handler,
    feedback_handler,
    message_handler,
)

__all__ = [
    'HANDLER_GROUPS',
]

HANDLER_GROUPS = (
    (
        start_handler.handler,
        file_handler.handler,
        set_language_handler.handler,
        call_task_handler.handler,
        feedback_handler.handler,
        message_handler.handler,
    ),
    (
        db_log_handler.handler,
    ),
    (
        log_handler.handler,
    ),
)
