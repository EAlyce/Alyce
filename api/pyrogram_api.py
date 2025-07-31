"""
Pyrogram API 适配器
实现 BaseAPI 接口，封装 Pyrogram 相关操作
"""
from typing import Any, Callable
from pyrogram import Client, filters
from .base import BaseAPI

class PyrogramAPI(BaseAPI):
    def __init__(self, client: Client):
        self.client = client

    async def send_message(self, chat_id: Any, text: str, **kwargs):
        await self.client.send_message(chat_id, text, **kwargs)

    async def get_me(self):
        return await self.client.get_me()

    async def add_handler(self, handler: Callable):
        self.client.add_handler(handler, filters.text)

    async def start(self):
        await self.client.start()

    async def stop(self):
        await self.client.stop()
