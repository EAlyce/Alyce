"""
Alyce - Telegram 客户端框架

主包初始化文件
"""

__version__ = "1.0.0"
__author__ = "EAlyce"
__description__ = "模块化的 Telegram 客户端框架"

# 导出主要组件
from core.client.telegram import TelegramClient
from core.plugin.manager import PluginManager
from utils.config import config
from utils.logging import setup_logger

__all__ = [
    'TelegramClient',
    'PluginManager', 
    'config',
    'setup_logger'
]
