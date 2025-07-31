from .base import command
import sys
import importlib

@command('reload', description='热重载指定插件（如 +reload foo）')
async def reload_cmd(event, args):
    name = args.strip()
    if not name:
        await event.reply("用法: +reload <插件名>")
        return
    modname = f"commands.{name}"
    if modname not in sys.modules:
        try:
            importlib.import_module(modname)
            await event.reply(f"插件 {name} 加载成功！")
            return
        except Exception as e:
            await event.reply(f"插件 {name} 加载失败：{e}")
            return
    try:
        importlib.reload(sys.modules[modname])
        await event.reply(f"插件 {name} 热重载成功！")
    except Exception as e:
        await event.reply(f"插件 {name} 热重载失败：{e}")
