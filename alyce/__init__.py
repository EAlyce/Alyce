"""
Alyce - Telegram client main package
"""

__version__ = "1.0.0"
__author__ = "EAlyce"
__description__ = "Alyce: Modern Telegram client and plugin framework"

from core.client.telegram import TelegramClient
from core.plugin.manager import PluginManager
from utils.config import config
from utils.logging import setup_logger

__all__ = [
    'TelegramClient',
    'PluginManager',
    'config',
    'setup_logger',
]