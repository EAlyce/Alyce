from telethon.events import NewMessage

class CommandRegistry:
    def __init__(self):
        self._commands = {}

    def register(self, name, handler, description=None):
        self._commands[name] = {
            'handler': handler,
            'description': description or ''
        }

    def get(self, name):
        return self._commands.get(name)

    def all_commands(self):
        return self._commands

registry = CommandRegistry()

def command(name, description=None):
    def decorator(func):
        registry.register(name, func, description)
        return func
    return decorator

def setup_command_handlers(client):
    @client.client.on(NewMessage(incoming=True))
    async def handle_command(event):
        text = event.raw_text.strip()
        if not text.startswith('+') or len(text) < 2:
            return
        cmd, *args = text[1:].split(maxsplit=1)
        cmd = cmd.lower()
        entry = registry.get(cmd)
        if entry:
            await entry['handler'](event, args[0] if args else '')
