"""
Alyce - Telegram client main package
"""

# Alyce 版本号自动维护，最大 99.99.99
__version__ = "1.0.0"
__author__ = "EAlyce"
__description__ = "Alyce: Modern Telegram client and plugin framework"

from core.client.telegram import TelegramClient
from utils.config import config
from utils.logging import setup_logger

__all__ = [
    'TelegramClient',
        'config',
    'setup_logger',
]