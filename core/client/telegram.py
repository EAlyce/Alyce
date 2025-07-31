import asyncio
import logging
from typing import Optional
from telethon import TelegramClient as TelethonClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import User
from .base import BaseClient
from utils.config import config

class TelegramClient(BaseClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger("alyce.client.telegram")
        self.client: Optional[TelethonClient] = None
        self._me: Optional[User] = None

    async def connect(self) -> bool:
        api_id = config.get_int("API_ID")
        api_hash = config.get("API_HASH")
        phone = config.get("PHONE")
        if not all([api_id, api_hash, phone]):
            self.logger.error("Missing API_ID, API_HASH, or PHONE in config.")
            return False
        self.client = TelethonClient(str(config.get_session_path()), api_id, api_hash)
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self._login(phone)
        self._me = await self.client.get_me()
        self.logger.info(f"Logged in as {self._me.first_name} (@{getattr(self._me, 'username', None) or 'N/A'})")
        return True

    async def _login(self, phone: str):
        await self.client.send_code_request(phone)
        code = input("Enter the code you received: ").strip()
        try:
            await self.client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input("Enter your 2FA password: ").strip()
            await self.client.sign_in(password=password)

    async def disconnect(self):
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            self.logger.info("Disconnected from Telegram")

    async def is_connected(self) -> bool:
        return bool(self.client and self.client.is_connected())

    @property
    def me(self) -> Optional[User]:
        return self._me