from telethon.events import NewMessage
from .base import registry

class CommandListener:
    def __init__(self, prefix='+'):
        self.prefix = prefix

    def set_prefix(self, prefix: str):
        self.prefix = prefix

    def parse_command(self, text: str):
        if not text.startswith(self.prefix) or len(text) <= len(self.prefix):
            return None, None
        rest = text[len(self.prefix):].lstrip()
        if not rest:
            return None, None
        # Split command and args
        parts = rest.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''
        return cmd, args

    def setup(self, client):
        @client.client.on(NewMessage(incoming=True))
        async def handle_command(event):
            text = event.raw_text.strip()
            cmd, args = self.parse_command(text)
            if not cmd:
                return
            entry = registry.get(cmd)
            if entry:
                await entry['handler'](event, args)

# Usage (in TelegramClient):
# from commands.listener import CommandListener
# listener = CommandListener(prefix='+')
# listener.setup(self)
