import logging
import os


def setup_logger():
    """Configure application logging"""

    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs (IMPORTANT )
    if not logger.handlers:

        file_handler = logging.FileHandler("logs/pipeline.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger