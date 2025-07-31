"""
Alyce 核心包，包含客户端、插件管理器、插件基类等核心功能。
"""

from .client.base import BaseClient
from .client.telegram import TelegramClient
from .plugin.manager import PluginManager
from .plugin.base import BasePlugin

__all__ = [
    'BaseClient',
    'TelegramClient',
    'PluginManager',
    'BasePlugin',
]