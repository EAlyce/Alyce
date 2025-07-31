"""
Alyce - Telegram 客户端主包
"""

__version__ = "1.0.0"
__author__ = "EAlyce"
__description__ = "Alyce: 现代化的 Telegram 客户端与插件框架"

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