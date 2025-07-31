from .base import command
import asyncio
import subprocess

@command('update', description='热更新 Alyce 代码/依赖/插件，并自动重启')
async def update_cmd(event, args, sent=None):
    # 步骤进度模板
    def progress(steps):
        return '\n'.join(steps)
    steps = [
        "✨ **[Alyce] 正在更新中...**",
        "请稍候，系统即将自动升级并重启。",
        "",
        "",  # 代码更新
        "",  # 插件热加载
        "",  # 自动重启
        ""   # 兼容 steps[6] 自动重启赋值
    ]
    msg = progress(steps)

    if sent is None:
        sent = await event.reply(msg)
    async def safe_edit(text):
        MAX_LEN = 4096
        if len(text) > MAX_LEN:
            text = text[:MAX_LEN-30] + "\n...\n[消息过长已截断]"
        try:
            if hasattr(sent, 'text') and (sent.text or '').strip() == text.strip():
                return  # 内容未变，跳过 edit
            await sent.edit(text)
        except Exception as e:
            if 'MessageNotModifiedError' in str(type(e)) or 'Content of the message was not modified' in str(e):
                pass  # 忽略内容未变异常
            else:
                import logging
                logging.exception(f"edit 消息异常: {e}")
    try:
        # 1. git pull
        import logging
        logger = logging.getLogger("alyce")
        proc = await asyncio.create_subprocess_exec(
            'git', 'pull',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        git_stdout, git_stderr = await proc.communicate()
        git_msg = git_stdout.decode().strip() or git_stderr.decode().strip()
        # 实时写入日志
        for line in (git_stdout.decode().splitlines() + git_stderr.decode().splitlines()):
            logger.info(f"[git] {line}")
        if proc.returncode != 0:
            await safe_edit(f"[Alyce] 更新失败")
            return
        # 每次 update 必定递增 PATCH 版本号
        # 已移除自动递增 Alyce 版本号逻辑。
        git_output = git_stdout.decode().strip() or git_stderr.decode().strip()
        steps[3] = f"✅ **代码更新完成**\n<pre>{git_output if git_output else '无输出'}</pre>"
        msg = progress(steps)
        await safe_edit(msg)
        # 3. 热加载插件（仅变更 commands/ 目录时无需重启）
        import os
        import importlib
        changed_files = git_msg.lower()
        if 'commands/' in changed_files or 'plugins/' in changed_files:
            # 热重载所有 commands 目录
            import sys
            reloaded = []
            for mod in list(sys.modules):
                if mod.startswith('commands.') and mod != 'commands.base' and mod != 'commands.listener':
                    importlib.reload(sys.modules[mod])
                    reloaded.append(mod)
            steps[5] = "🧩 正在热加载插件..."
            msg = progress(steps)
            await safe_edit(msg)
            return
        # 4. 自动重启 Alyce 进程（代码/依赖变更）
        steps[6] = "♻️ 所有更新已应用，Alyce 正在自动重启中..."
        msg = progress(steps)
        await safe_edit(msg)
        await asyncio.sleep(1)
        # os.execv 会替换进程，无法直接 edit，需在启动时检测是否为 update 后重启
        # 可以通过写入一个 .reboot 标记文件，启动后检测并 edit
        with open('.reboot', 'w', encoding='utf-8') as f:
            f.write(str(event.id) if hasattr(event, 'id') else '')
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        await safe_edit(msg + f"\n\n[Alyce] 更新出错：{e}")
