import logging

import structlog


def configure_logging(level: str = "INFO") -> None:
    """Configure Dobby's structured logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(message)s",
    )

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.KeyValueRenderer(),
        ],
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a structured logger for a Dobby component."""
    logger = structlog.get_logger()

    if name:
        return logger.bind(component=name)

    return logger
