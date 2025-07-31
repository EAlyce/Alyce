""
插件基类
"""
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Plugin(ABC):
    """插件基类，所有插件必须继承此类"""
    
    # 插件元数据
    name: str = "base_plugin"
    "插件唯一标识符，建议使用小写下划线命名"
    
    version: str = "0.1.0"
    "插件版本"
    
    description: str = ""
    "插件描述"
    
    enabled: bool = True
    "是否启用插件"
    
    def __init__(self, client):
        """
        初始化插件
        
        Args:
            client: AlyceClient 实例
        """
        self.client = client
        self.logger = logging.getLogger(f'alyce.plugin.{self.name}')
        self.config: Dict[str, Any] = {}
    
    async def initialize(self):
        """初始化插件"""
        await self.on_load()
        self.logger.info(f"Initializing plugin: {self.name}")
    
    async def cleanup(self):
        """清理插件资源"""
        self.logger.info(f"Cleaning up plugin: {self.name}")
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, version={self.version})"
    
    def __repr__(self) -> str:
        return str(self)
