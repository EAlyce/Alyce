"""
API 基类
为不同协议（如 Telethon、Pyrogram）提供统一接口
"""
from abc import ABC, abstractmethod
from typing import Any

class BaseAPI(ABC):
    """API 基类"""
    
    @abstractmethod
    async def send_message(self, chat_id: Any, text: str, **kwargs):
        pass
    
    @abstractmethod
    async def get_me(self):
        pass
    
    @abstractmethod
    async def add_handler(self, handler):
        pass
    
    @abstractmethod
    async def start(self):
        pass
    
    @abstractmethod
    async def stop(self):
        pass
