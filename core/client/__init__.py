"""
客户端模块

包含不同协议的 Telegram 客户端实现
"""

from .base import BaseClient
from .telegram import TelegramClient

__all__ = [
    'BaseClient',
    'TelegramClient'
]
