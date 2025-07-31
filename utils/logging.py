import logging
import sys
import os
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = 'alyce',
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """Set up and return a logger with optional file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:
        return logger
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if log_file:
        log_dir = Path('logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / log_file
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger