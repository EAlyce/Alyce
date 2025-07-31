from .base import command
import sys
import os
import asyncio

@command('restart', description='安全重启 Alyce 进程')
async def restart_cmd(event, args):
    await event.reply("[Alyce] 正在安全重启进程……")
    await asyncio.sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)
