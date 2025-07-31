"""
Alyce core package, includes client, plugin manager, plugin base and other core features.
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