from .base import command
import asyncio
import subprocess

@command('update', description='热更新 Alyce 代码/依赖/插件，并自动重启')
async def update_cmd(event, args, sent=None):
    msg = "[Alyce] 正在检查并拉取最新更新..."
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
            await safe_edit(f"[Alyce] 更新失败，详细日志见 logs/alyce-YYYY-MM-DD.log")
            return
        msg += f"\n\n[Alyce] 代码已更新，详细日志见 logs/alyce-YYYY-MM-DD.log\n正在升级依赖..."
        await safe_edit(msg)
        # 2. pip install -r requirements.txt
        import sys
        pip_cmds = [
            ['pip3', 'install', '-r', 'requirements.txt'],
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']
        ]
        pip_log = []
        for pip_cmd in pip_cmds:
            try:
                proc2 = await asyncio.create_subprocess_exec(
                    *pip_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout2, stderr2 = await proc2.communicate()
                pip_msg = stdout2.decode().strip() or stderr2.decode().strip()
                # 写入日志
                for line in (stdout2.decode().splitlines() + stderr2.decode().splitlines()):
                    logger.info(f"[pip] {line}")
                if proc2.returncode == 0:
                    break
            except FileNotFoundError:
                pip_msg = f"未找到 pip 命令：{' '.join(pip_cmd)}"
                logger.error(pip_msg)
                continue
        else:
            await safe_edit(msg + f"\n\n[Alyce] 依赖升级失败，详细日志见 logs/alyce-YYYY-MM-DD.log")
            return
        msg += f"\n\n[Alyce] 依赖已升级，详细日志见 logs/alyce-YYYY-MM-DD.log\n正在检测插件热加载..."
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
            await safe_edit(msg + f"\n\n[Alyce] 插件热加载完成：{', '.join(reloaded) if reloaded else '无插件变更'}\n无需重启。")
            return
        # 4. 自动重启 Alyce 进程（代码/依赖变更）
        await safe_edit(msg + "\n\n[Alyce] 代码和依赖已更新，正在自动重启 Alyce...\nSession 文件已独立保存，无需重新登录。")
        await asyncio.sleep(1)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        await safe_edit(msg + f"\n\n[Alyce] 更新出错：{e}")
