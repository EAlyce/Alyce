from .base import command
import re

APT_USAGE = (
    "用法: +apt {update|search|show|status|install|remove|enable|disable|upload|export} <插件名称/文件>\n"
    "所需权限: system.apt\n"
    "用于管理安装到 PagerMaid-Modify 的插件。"
)

@command('apt', description='插件管理指令 (PagerMaid风格)')
async def apt_cmd(event, args):
    text = event.raw_text.strip()
    match = re.match(r"^\+apt\s+(\w+)(?:\s+(.*))?", text, re.I)
    if not match:
        await event.reply(APT_USAGE)
        return
    subcmd = match.group(1).lower()
    param = (match.group(2) or '').strip()
    # 权限检查（示例，实际可扩展）
    # if not await check_permission(event, 'system.apt'):
    #     await event.reply('权限不足：system.apt')
    #     return
    if subcmd == 'update':
        await event.reply("[模拟] 插件列表已更新。")
    elif subcmd == 'search':
        if not param:
            await event.reply("用法: +apt search <关键词>")
            return
        from .plugin_market import fetch_market
        market = await fetch_market()
        results = [p for p in market.get('plugins', []) if param.lower() in p['name'].lower() or param.lower() in p.get('desc', '')]
        if results:
            msg = '\n'.join([f"{p['name']} - {p.get('desc','')[:40]}" for p in results])
            await event.reply(f"搜索结果：\n{msg}")
        else:
            await event.reply("未找到相关插件。")
    elif subcmd == 'install':
        if not param:
            await event.reply("用法: +apt install <插件名>")
            return
        from .plugin_market import fetch_market, download_plugin
        import sys, importlib
        market = await fetch_market()
        plugin = next((p for p in market.get('plugins', []) if p['name'].lower() == param.lower()), None)
        if not plugin:
            await event.reply(f"未找到插件：{param}")
            return
        path = await download_plugin(plugin, target_dir='commands')
        if not path:
            await event.reply(f"插件下载失败：{plugin['name']}")
            return
        # 热加载
        modname = f"commands.{path.stem}"
        try:
            if modname in sys.modules:
                importlib.reload(sys.modules[modname])
            else:
                importlib.import_module(modname)
            await event.reply(f"插件 {plugin['name']} 安装并热加载成功！")
        except Exception as e:
            await event.reply(f"插件已下载，但加载失败：{e}")
    elif subcmd == 'show':
        await event.reply(f"[模拟] 显示插件信息：{param or '[未指定插件名]'}。")
    elif subcmd == 'status':
        await event.reply("[模拟] 当前插件状态：全部正常。")
    elif subcmd == 'remove':
        await event.reply(f"[模拟] 已卸载插件：{param or '[未指定插件名]'}。")
    elif subcmd == 'enable':
        await event.reply(f"[模拟] 已启用插件：{param or '[未指定插件名]'}。")
    elif subcmd == 'disable':
        await event.reply(f"[模拟] 已禁用插件：{param or '[未指定插件名]'}。")
    elif subcmd == 'upload':
        await event.reply(f"[模拟] 已上传插件文件：{param or '[未指定文件]'}。")
    elif subcmd == 'export':
        await event.reply(f"[模拟] 已导出插件：{param or '[未指定插件名]'}。")
    else:
        await event.reply(f"未知子命令: {subcmd}\n" + APT_USAGE)
