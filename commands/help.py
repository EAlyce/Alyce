from .base import command, get_all_commands
import math

@command('help', description='显示所有命令、用法和权限', usage='+help [命令/分组]', aliases=['h','?'], group='系统')
async def help_cmd(event, args):
    arg = args.strip().lower()
    cmds = get_all_commands()
    if arg:
        # 详细命令或分组帮助
        for meta in cmds:
            if arg == meta.name or arg in meta.aliases:
                text = f"指令: +{meta.name}\n"
                if meta.aliases:
                    text += f"别名: {'/'.join(meta.aliases)}\n"
                text += f"分组: {meta.group or '未分组'}\n权限: {meta.permission}\n触发: {meta.trigger_mode}\n"
                text += f"用法: {meta.usage or '+%s ...' % meta.name}\n"
                text += f"说明: {meta.description or '无'}"
                await event.reply(text)
                return
        # 按分组显示
        group_cmds = [m for m in cmds if m.group and m.group.lower() == arg]
        if group_cmds:
            text = f"[{arg}] 分组命令：\n"
            for m in group_cmds:
                text += f"+{m.name} - {m.description or '无'}\n"
            await event.reply(text)
            return
        await event.reply(f"未找到命令或分组：{arg}")
        return
    # 分组+分页
    groups = {}
    for m in cmds:
        groups.setdefault(m.group or '未分组', []).append(m)
    msg = "Alyce 可用命令（分组/权限/用法）：\n"
    for group, items in groups.items():
        msg += f"\n[{group}]\n"
        for m in items:
            alias = f" (别名: {'/'.join(m.aliases)})" if m.aliases else ''
            msg += f"+{m.name}{alias} | 权限:{m.permission} | {m.usage or ''}\n  {m.description or ''}\n"
    await event.reply(msg)
