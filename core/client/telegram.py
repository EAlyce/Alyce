"""
Telegram 客户端实现 (基于 Telethon)
"""
import asyncio
import logging
from typing import Optional, Dict, Any

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from telethon.tl.types import User

from ..base import BaseClient
from utils.config import config


class TelegramClient(BaseClient):
    """Telegram 客户端实现"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger('alyce.client.telegram')
        self._me: Optional[User] = None
        
    async def connect(self) -> bool:
        """连接到 Telegram 服务器"""
        try:
            api_id = config.get_int('API_ID')
            api_hash = config.get('API_HASH')
            phone = config.get('PHONE')
            
            if not all([api_id, api_hash, phone]):
                self.logger.error("Missing required configuration (API_ID, API_HASH, PHONE)")
                return False
                
            # 初始化 Telegram 客户端
            self.client = TelegramClient(
                str(config.get_session_path()),
                api_id=api_id,
                api_hash=api_hash,
                device_model="Alyce Client",
                app_version="1.0.0",
                system_version="Alyce/1.0.0"
            )
            
            # 连接服务器
            await self.client.connect()
            
            # 检查是否已登录
            if not await self.client.is_user_authorized():
                await self._login(phone)
                
            # 获取当前用户信息
            self._me = await self.client.get_me()
            self.logger.info(f"Logged in as {self._me.first_name} (@{self._me.username or 'N/A'})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Telegram: {e}", exc_info=True)
            return False
    
    async def _login(self, phone: str):
        """登录流程"""
        if not self.client:
            raise RuntimeError("Client not initialized")
            
        # 发送验证码
        await self.client.send_code_request(phone)
        
        # 请求用户输入验证码
        while True:
            try:
                code = input("Enter the code you received: ").strip()
                if not code:
                    continue
                    
                # 尝试登录
                await self.client.sign_in(phone, code)
                break
                
            except PhoneCodeInvalidError:
                print("Invalid code. Please try again.")
                
            except SessionPasswordNeededError:
                # 需要两步验证密码
                password = input("Enter your 2FA password: ").strip()
                if password:
                    await self.client.sign_in(password=password)
                    break
    
    async def disconnect(self):
        """断开连接"""
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            self.logger.info("Disconnected from Telegram")
    
    async def is_connected(self) -> bool:
        """检查连接状态"""
        return bool(self.client and self.client.is_connected())
    
    @property
    def me(self) -> Optional[User]:
        """获取当前用户信息"""
        return self._me
