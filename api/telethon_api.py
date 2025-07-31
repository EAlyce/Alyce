"""
Telethon API 适配器
实现 BaseAPI 接口，封装 Telethon 相关操作
"""
from typing import Any, Callable
from telethon import TelegramClient, events
from .base import BaseAPI

class TelethonAPI(BaseAPI):
    def __init__(self, client: TelegramClient):
        self.client = client

    async def send_message(self, chat_id: Any, text: str, **kwargs):
        await self.client.send_message(chat_id, text, **kwargs)

    async def get_me(self):
        return await self.client.get_me()

    async def add_handler(self, handler: Callable):
        self.client.add_event_handler(handler, events.NewMessage)

    async def start(self):
        await self.client.start()

    async def stop(self):
        await self.client.disconnect()
