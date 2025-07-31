from core.plugin.base import BasePlugin
from plugins.decorators import on_command

class MyPlugin(BasePlugin):
    @on_command("hello")
    async def hello(self, message, client, args):
        await client.send_message(message.chat.id, "Hello from Alyce plugin!")

    async def on_load(self):
        print("[MyPlugin] Plugin loaded")

    async def on_unload(self):
        print("[MyPlugin] Plugin unloaded")

    async def on_error(self, exc):
        print(f"[MyPlugin] Plugin error: {exc}")