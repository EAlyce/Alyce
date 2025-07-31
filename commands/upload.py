from .base import command
from telethon.tl.types import MessageMediaDocument
import aiohttp
import os

# 配置：插件上传API
UPLOAD_API = 'https://alyce.example.com/api/upload_plugin'  # 替换为实际API

@command('upload', description='上传插件到 Alyce 插件市场（如 +upload foo.py）')
async def upload_cmd(event, args):
    # 检查是否为 owner
    sender = await event.get_sender()
    if getattr(sender, 'id', None) not in [123456789]:  # 替换为 owner ID
        await event.reply('仅 owner 可上传插件。')
        return
    # 支持直接文件名或回复文件
    file_path = args.strip()
    if not file_path and event.reply_to_msg_id:
        reply = await event.get_reply_message()
        if isinstance(getattr(reply, 'media', None), MessageMediaDocument):
            file_path = reply.file.name or 'plugin.py'
            await reply.download_media(file_path)
    if not file_path or not os.path.isfile(file_path):
        await event.reply('请指定本地插件文件名或回复插件文件。')
        return
    await event.reply(f'正在上传插件 {file_path} ...')
    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'application/octet-stream')}
                data = aiohttp.FormData()
                data.add_field('file', f, filename=os.path.basename(file_path), content_type='application/octet-stream')
                async with session.post(UPLOAD_API, data=data, timeout=30) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        await event.reply(f"插件上传成功！\n市场审核结果：{result.get('msg', '待审核')}")
                    else:
                        await event.reply(f"上传失败，HTTP状态码：{resp.status}")
    except Exception as e:
        await event.reply(f"插件上传出错：{e}")
