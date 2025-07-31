"""
命令系统框架
支持插件注册命令、自动帮助、权限校验
"""
from typing import Callable, Dict, Any

from utils.logging import get_logger
import traceback

class CommandRegistry:
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self.logger = get_logger("alyce.command")

    def register(self, name: str, handler: Callable):
        self.logger.info(f"注册命令: {name} handler: {handler.__name__}")
        self.commands[name] = handler

    async def execute(self, name: str, *args, **kwargs):
        self.logger.info(f"执行命令: {name} args: {args} kwargs: {kwargs}")
        # 插件帮助命令
        if name == "help":
            plugin_name = (args[0] if args else None)
            if plugin_name and plugin_name in self.commands:
                handler = self.commands[plugin_name]
                doc = getattr(handler, "__doc__", "无帮助信息")
                client = kwargs.get("client")
                message = kwargs.get("message")
                if client and message:
                    await client.send_message(message.chat.id, doc)
                return
            else:
                client = kwargs.get("client")
                message = kwargs.get("message")
                if client and message:
                    await client.send_message(message.chat.id, "用法：/help 插件命令名")
                return
        if name in self.commands:
            try:
                await self.commands[name](*args, **kwargs)
            except Exception as e:
                self.logger.error(f"命令处理异常: {name} - {e}\n{traceback.format_exc()}")

    def get(self, name: str):
        return self.commands.get(name)

    def list_commands(self):
        return list(self.commands.keys())
