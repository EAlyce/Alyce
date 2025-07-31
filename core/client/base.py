"""
Alyce 客户端基类

本模块为所有 Telegram 客户端实现提供统一基类，定义了连接、断开、插件管理等核心接口。
"""
import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type

from telethon import TelegramClient

from alyce.core.plugin.manager import PluginManager


class AlyceClient(ABC):
    """Alyce 客户端基类"""
    
    def __init__(self, **kwargs):
        """
        初始化 Alyce 客户端
        
        Args:
            **kwargs: 客户端配置参数
        """
        self.config = kwargs
        self.client: Optional[TelegramClient] = None
        self.plugin_manager = PluginManager(self)
    
    @abstractmethod
    async def connect(self) -> bool:
        """连接到 Telegram 服务器"""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """断开与 Telegram 服务器的连接"""
        pass
    
    @abstractmethod
    async def is_connected(self) -> bool:
        """检查是否已连接"""
        pass
    
    async def run(self):
        """运行客户端主循环"""
        try:
            # 连接到 Telegram
            if not await self.connect():
                raise RuntimeError("Failed to connect to Telegram")
            
            # 初始化插件
            await self.plugin_manager.initialize()
            
            # 保持运行直到断开连接
            while await self.is_connected():
                await asyncio.sleep(1)
                
        except asyncio.CancelledError:
            pass
        finally:
            # 清理资源
            await self.plugin_manager.cleanup()
            await self.disconnect()
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(connected={self.client is not None and self.client.is_connected()})"
