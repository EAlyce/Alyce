from .base import command
import os

@command(
    name='sendlog',
    description='发送 Alyce 运行日志文件',
    usage='+sendlog',
    group='系统',
    permission='owner',
    aliases=['log']
)
async def sendlog_cmd(event, args):
    # 假设日志文件为 logs/alyce.log 或 alyce.log
    paths = ['logs/alyce.log', 'alyce.log']
    for p in paths:
        if os.path.isfile(p):
            await event.reply(file=p, message='Alyce 日志文件如下：')
            return
    await event.reply('未找到日志文件。')
