from .base import command
import re

APT_USAGE = (
    "用法: +apt {update|search|show|status|install|remove|enable|disable|upload|export} <插件名称/文件>\n"
    "所需权限: system.apt\n"
    "用于管理安装到 PagerMaid-Modify 的插件。"
)

@command('apt', description='插件管理指令 (PagerMaid风格)')
async def apt_cmd(event, args, sent=None):
    text = event.raw_text.strip()
    match = re.match(r"^\+apt\s+(\w+)(?:\s+(.*))?", text, re.I)
    edit = sent.edit if sent else event.reply
    if not match:
        await edit(APT_USAGE)
        return
    subcmd = match.group(1).lower()
    param = (match.group(2) or '').strip()
    # 权限检查（示例，实际可扩展）
    # if not await check_permission(event, 'system.apt'):
    #     await event.reply('权限不足：system.apt')
    #     return
    if subcmd == 'update':
        await edit("[模拟] 插件列表已更新。")
    elif subcmd == 'search':
        if not param:
            await edit("用法: +apt search <关键词>")
            return
        from .plugin_market import fetch_market
        market = await fetch_market()
        results = [p for p in market.get('plugins', []) if param.lower() in p['name'].lower() or param.lower() in p.get('desc', '')]
        if results:
            msg = '\n'.join([f"{p['name']} - {p.get('desc','')[:40]}" for p in results])
            await edit(f"搜索结果：\n{msg}")
        else:
            await edit("未找到相关插件。")
    elif subcmd == 'install':
        import sys, importlib, os
        # 支持对着 .py 文件回复自动安装
        if not param and getattr(event, 'reply_to_msg_id', None):
            reply_msg = await event.get_reply_message()
            if reply_msg and reply_msg.document and reply_msg.document.mime_type == 'text/x-python' and reply_msg.document.name.endswith('.py'):
                fname = reply_msg.document.name
                target_path = os.path.join('commands', fname)
                await edit(f"[Alyce] 正在保存插件文件 {fname} ...")
                try:
                    await reply_msg.download_media(file=target_path)
                    modname = f"commands.{fname[:-3]}"
                    if modname in sys.modules:
                        importlib.reload(sys.modules[modname])
                    else:
                        importlib.import_module(modname)
                    await edit(f"插件 {fname} 安装并热加载成功！")
                except Exception as e:
                    await edit(f"插件文件保存或加载失败：{e}")
                return
        # 兼容原有市场插件名安装
        if not param:
            await edit("用法: +apt install <插件名> 或回复 .py 插件文件")
            return
        from .plugin_market import fetch_market, download_plugin, check_permissions
        market = await fetch_market()
        plugin = next((p for p in market.get('plugins', []) if p['name'].lower() == param.lower()), None)
        if not plugin:
            await edit(f"未找到插件：{param}")
            return
        user_permissions = ['owner']
        if not check_permissions(plugin, user_permissions):
            await edit(f"插件 {plugin['name']} 需要权限：{plugin.get('permissions')}，当前权限不足！")
            return
        await edit(f"[Alyce] 正在下载并校验插件 {plugin['name']} ...")
        path, err = await download_plugin(plugin, target_dir='commands')
        if err:
            await edit(f"插件 {plugin['name']} 安装失败：{err}")
            return
        modname = f"commands.{path.stem}"
        try:
            if modname in sys.modules:
                importlib.reload(sys.modules[modname])
            else:
                importlib.import_module(modname)
            await edit(f"插件 {plugin['name']} 安装并热加载成功！\n版本: {plugin.get('version','?')} 作者: {plugin.get('author','?')}\n描述: {plugin.get('desc','')}\n依赖: {plugin.get('dependencies','无')}")
        except Exception as e:
            await edit(f"插件已下载，但加载失败：{e}")
    elif subcmd == 'show':
        await edit(f"[模拟] 显示插件信息：{param or '[未指定插件名]'}。")
    elif subcmd == 'status':
        await edit("[模拟] 当前插件状态：全部正常。")
    elif subcmd == 'remove':
        await edit(f"[模拟] 已卸载插件：{param or '[未指定插件名]'}。")
    elif subcmd == 'enable':
        await edit(f"[模拟] 已启用插件：{param or '[未指定插件名]'}。")
    elif subcmd == 'disable':
        await edit(f"[模拟] 已禁用插件：{param or '[未指定插件名]'}。")
    elif subcmd == 'upload':
        await edit(f"[模拟] 已上传插件文件：{param or '[未指定文件]'}。")
    elif subcmd == 'export':
        await edit(f"[模拟] 已导出插件：{param or '[未指定插件名]'}。")
    else:
        await edit(f"未知子命令: {subcmd}\n" + APT_USAGE)
