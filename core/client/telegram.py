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
                print("[错误] 缺少必要配置项：API_ID、API_HASH、PHONE。请在配置文件中补全后重试！")
                self.logger.error("缺少必要配置 (API_ID, API_HASH, PHONE)")
                return False

            print("[信息] 正在初始化 Telegram 客户端...")
            self.client = TelegramClient(
                str(config.get_session_path()),
                api_id=api_id,
                api_hash=api_hash,
                device_model="Alyce Client",
                app_version="1.0.0",
                system_version="Alyce/1.0.0"
            )

            print("[信息] 正在连接到 Telegram 服务器...")
            await self.client.connect()

            # 检查是否已登录
            if not await self.client.is_user_authorized():
                print("[提示] 当前未登录，将进入登录流程...")
                await self._login(phone)

            # 获取当前用户信息
            self._me = await self.client.get_me()
            print(f"[成功] 登录成功，当前账号：{self._me.first_name} (@{self._me.username or '无用户名'})")
            self.logger.info(f"Logged in as {self._me.first_name} (@{self._me.username or 'N/A'})")
            return True

        except Exception as e:
            print(f"[错误] 连接 Telegram 失败：{e}")
            self.logger.error(f"Failed to connect to Telegram: {e}", exc_info=True)
            return False
    
    async def _login(self, phone: str):
        """登录流程"""
        if not self.client:
            raise RuntimeError("Client not initialized")

        print(f"[登录] 已向 {phone} 发送验证码...\n")
        await self.client.send_code_request(phone)

        # 请求用户输入验证码
        while True:
            try:
                code = input("请输入收到的验证码（数字）：").strip()
                if not code:
                    print("[提示] 验证码不能为空，请重新输入。")
                    continue

                # 尝试登录
                await self.client.sign_in(phone, code)
                print("[成功] 验证码验证通过，已登录！")
                break

            except PhoneCodeInvalidError:
                print("[错误] 验证码无效，请重新输入。")

            except SessionPasswordNeededError:
                # 需要两步验证密码
                password = input("检测到账号开启了两步验证，请输入 2FA 密码：").strip()
                if password:
                    await self.client.sign_in(password=password)
                    print("[成功] 2FA 验证通过，已登录！")
                    break
                else:
                    print("[提示] 2FA 密码不能为空，请重新输入。")
    
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
