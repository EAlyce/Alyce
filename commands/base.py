from telethon.events import NewMessage

class CommandRegistry:
    def __init__(self):
        self._commands = {}

    def register(self, name, handler, description=None, usage='', aliases=None, group='', permission='user', trigger_mode='exact', meta=None):
        self._commands[name] = {
            'handler': handler,
            'description': description or '',
            'usage': usage or '',
            'aliases': aliases or [],
            'group': group or '',
            'permission': permission or 'user',
            'trigger_mode': trigger_mode or 'exact',
            'meta': meta,
        }

    def get(self, name):
        return self._commands.get(name)

    def all_commands(self):
        return self._commands

registry = CommandRegistry()

class CommandMeta:
    def __init__(self, name, handler, description='', usage='', aliases=None, group='', permission='user', trigger_mode='exact'):
        self.name = name
        self.handler = handler
        self.description = description
        self.usage = usage
        self.aliases = aliases or []
        self.group = group
        self.permission = permission
        self.trigger_mode = trigger_mode

    def all_names(self):
        return [self.name] + self.aliases

def command(name, description=None, usage=None, aliases=None, group=None, permission=None, trigger_mode=None):
    def decorator(func):
        meta = CommandMeta(
            name=name,
            handler=func,
            description=description or '',
            usage=usage or '',
            aliases=aliases or [],
            group=group or '',
            permission=permission or 'user',
            trigger_mode=trigger_mode or 'exact',
        )
        # 注册主命令和别名
        for n in meta.all_names():
            registry.register(n, func, meta.description, meta.usage, meta.aliases, meta.group, meta.permission, meta.trigger_mode)
        return func
    return decorator

def get_all_commands():
    # 去重，仅主命令
    seen = set()
    cmds = []
    for meta in {v['meta'] for v in registry.all_commands().values()}:
        if meta.name not in seen:
            cmds.append(meta)
            seen.add(meta.name)
    return cmds

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
