"""
客户端基类
定义 Alyce 客户端的通用接口
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseClient(ABC):
    """Alyce 客户端基类"""
    
    def __init__(self, **kwargs):
        """
        初始化 Alyce 客户端
        
        Args:
            **kwargs: 客户端配置参数
        """
        self.config = kwargs
        self.client = None
    
    @abstractmethod
    async def connect(self) -> bool:
        """连接到服务器"""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """断开与服务器的连接"""
        pass
    
    @abstractmethod
    async def is_connected(self) -> bool:
        """检查是否已连接"""
        pass
    
    @property
    @abstractmethod
    def me(self) -> Optional[Dict[str, Any]]:
        """获取当前用户信息"""
        pass
