import logging
import sys
from typing import Final

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


FMT: Final[str] = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level> | "
    "{extra}"
)


def setup_logger(*, default_level: str = "INFO") -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        level=default_level,
        format=FMT,
        backtrace=True,
        diagnose=True,
    )
    for name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
        _logger = logging.getLogger(name)
        _logger.handlers = [InterceptHandler()]
        _logger.propagate = False

    logger.add(
        "app/logs/app.log",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        level="INFO",
        encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    )
