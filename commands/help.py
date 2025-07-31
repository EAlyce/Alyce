from .base import command, registry

@command('help', description='显示所有可用命令及其描述')
async def help_cmd(event, args):
    cmds = registry.all_commands()
    msg = "Alyce 可用命令：\n"
    for name, entry in cmds.items():
        desc = entry['description']
        msg += f"+{name} - {desc}\n"
    await event.reply(msg)
