from telethon.events import NewMessage
from .base import registry

class CommandListener:
    def __init__(self, prefixes=None, trigger_mode='exact'):
        # prefixes: list of str, e.g. ['+', '!', '/']
        self.prefixes = prefixes or ['+']
        self.trigger_mode = trigger_mode  # exact, regex, fuzzy

    def set_prefixes(self, prefixes):
        self.prefixes = prefixes

    def parse_command(self, text: str):
        # 支持多前缀
        for prefix in self.prefixes:
            if text.startswith(prefix) and len(text) > len(prefix):
                rest = text[len(prefix):].lstrip()
                if not rest:
                    return None, None, None
                parts = rest.split(maxsplit=1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ''
                return prefix, cmd, args
        return None, None, None

    def setup(self, client):
        @client.client.on(NewMessage(outgoing=True))
        async def handle_command(event):
            text = event.raw_text.strip()
            prefix, cmd, args = self.parse_command(text)
            if not cmd:
                return
            # 获取用户、群聊、权限等上下文
            sender = await event.get_sender()
            chat = await event.get_chat()
            user_id = getattr(sender, 'id', None)
            chat_id = getattr(chat, 'id', None)
            # 权限分级（owner/admin/user/guest），可扩展
            user_permissions = ['owner'] if user_id in getattr(client, 'OWNER_IDS', [123456789]) else ['user']
            # 命令分发
            entry = registry.get(cmd)
            if entry:
                # 权限检查（如 entry['permission']）
                perm = entry.get('permission', 'user')
                if perm == 'owner' and 'owner' not in user_permissions:
                    await event.reply('无权限，仅 owner 可用。')
                    return
                try:
                    sent = await event.edit("[Alyce] 正在处理中...")
                except Exception:
                    sent = await event.respond("[Alyce] 正在处理中...")
                try:
                    await entry['handler'](event, args, sent)
                except TypeError:
                    # 兼容旧插件只接受(event, args)
                    await entry['handler'](event, args)

# Usage (in TelegramClient):
# from commands.listener import CommandListener
# listener = CommandListener(prefix='+')
# listener.setup(self)
