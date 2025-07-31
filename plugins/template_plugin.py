"""
Alyce 插件开发模板
支持命令注册、生命周期钩子、自动帮助
"""
from core.plugin.base import BasePlugin
from plugins.decorators import on_command

class MyPlugin(BasePlugin):
    """
    示例插件，展示命令注册、生命周期钩子用法
    """
    @on_command("hello")
    async def hello(self, message, client, args):
        await client.send_message(message.chat.id, "Hello from Alyce plugin!")

    async def on_load(self):
        print("[MyPlugin] 插件已加载")

    async def on_unload(self):
        print("[MyPlugin] 插件已卸载")

    async def on_error(self, exc):
        print(f"[MyPlugin] 插件异常: {exc}")
