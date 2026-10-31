import logging
from pathlib import Path


def get_logger(name: str = "ETL_Framework") -> logging.Logger:
    """
    Create and return a reusable ETL logger.
    """

    # Create logs directory
    log_directory = Path("logs")
    log_directory.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate log messages
    logger.propagate = False

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Define log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Log to file
    file_handler = logging.FileHandler(
        log_directory / "etl_pipeline.log",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Log to terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger