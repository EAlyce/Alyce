"""
Alyce - 模块化 Telegram 客户端框架

提供基于插件的 Telegram 客户端功能，支持多种协议和代理。
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

# 导出核心组件
from alyce.core.client.base import AlyceClient
from alyce.core.plugin.manager import PluginManager

__all__ = ['AlyceClient', 'PluginManager']
