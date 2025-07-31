from .base import command
import asyncio
import sys
import os

@command('rollback', description='回滚到上一个或指定历史版本（+rollback 或 +rollback <commit/tag>）')
async def rollback_cmd(event, args):
    commit = args.strip()
    if not commit:
        cmd = ['git', 'reset', '--hard', 'HEAD~1']
        msg = '回滚到上一个版本'
    else:
        cmd = ['git', 'reset', '--hard', commit]
        msg = f'回滚到 {commit}'
    await event.reply(f"[Alyce] 正在{msg}...")
    try:
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        out = stdout.decode().strip() or stderr.decode().strip()
        if proc.returncode == 0:
            await event.reply(f"[Alyce] {msg}成功，正在自动重启...\n{out}")
            await asyncio.sleep(1)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            await event.reply(f"[Alyce] {msg}失败：\n{out}")
    except Exception as e:
        await event.reply(f"[Alyce] 回滚出错：{e}")

@command('history', description='查看最近 10 个 git 提交历史')
async def history_cmd(event, args):
    try:
        proc = await asyncio.create_subprocess_exec('git', 'log', '-n', '10', '--pretty=oneline', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        log = stdout.decode().strip() or stderr.decode().strip()
        await event.reply(f"[Alyce] 最近 10 个提交：\n{log}")
    except Exception as e:
        await event.reply(f"[Alyce] 获取历史失败：{e}")
