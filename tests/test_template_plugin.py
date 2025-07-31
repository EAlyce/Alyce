"""
Alyce 插件自动化测试模板
pytest + pytest-asyncio
"""
import pytest
import asyncio
from plugins.template_plugin import MyPlugin

@pytest.mark.asyncio
async def test_hello_command():
    class DummyClient:
        async def send_message(self, chat_id, text, **kwargs):
            assert chat_id == 123
            assert "Hello" in text
            return True
    class DummyMessage:
        chat = type("chat", (), {"id": 123})()
    plugin = MyPlugin(DummyClient())
    await plugin.hello(DummyMessage(), DummyClient(), ["test"])
