"""
PagerMaid 插件 API 兼容层
提供 send_message, edit_message, delete_message, reply, forward, get_user, ban/kick 等常用接口
兼容 Telethon/Pyrogram
"""
from typing import Any, Optional
from utils.logging import get_logger
logger = get_logger("alyce.plugins.api")

# 消息发送
async def send_message(client, chat_id: Any, text: str, **kwargs):
    logger.info(f"send_message: chat_id={chat_id}, text={text}")
    try:
        return await client.send_message(chat_id, text, **kwargs)
    except Exception as e:
        logger.error(f"send_message error: {e}")
        raise

# 编辑消息
async def edit_message(client, chat_id: Any, message_id: int, text: str, **kwargs):
    return await client.edit_message(chat_id, message_id, text, **kwargs)

# 删除消息
async def delete_message(client, chat_id: Any, message_id: int):
    return await client.delete_messages(chat_id, message_id)

# 回复消息
async def reply_message(client, message, text: str, **kwargs):
    if hasattr(message, 'reply'):
        return await message.reply(text, **kwargs)
    # 兼容 Pyrogram
    elif hasattr(client, 'send_message') and hasattr(message, 'chat'):
        return await client.send_message(message.chat.id, text, reply_to_message_id=getattr(message, 'message_id', None), **kwargs)

# 转发消息
async def forward_message(client, chat_id: Any, from_chat_id: Any, message_id: int):
    if hasattr(client, 'forward_messages'):
        return await client.forward_messages(chat_id, from_chat_id, message_id)
    elif hasattr(client, 'forward_message'):
        return await client.forward_message(chat_id, from_chat_id, message_id)

# 获取消息详情
async def get_message(client, chat_id: Any, message_id: int):
    if hasattr(client, 'get_messages'):
        return await client.get_messages(chat_id, ids=message_id)
    elif hasattr(client, 'get_message'):
        return await client.get_message(chat_id, message_id)

# 获取用户信息
async def get_user(client, user_id: Any):
    if hasattr(client, 'get_entity'):
        return await client.get_entity(user_id)
    elif hasattr(client, 'get_users'):
        return await client.get_users(user_id)

# 获取聊天信息
async def get_chat(client, chat_id: Any):
    if hasattr(client, 'get_entity'):
        return await client.get_entity(chat_id)
    elif hasattr(client, 'get_chat'):
        return await client.get_chat(chat_id)

# 踢人
async def kick_user(client, chat_id: Any, user_id: Any):
    if hasattr(client, 'kick_participant'):
        return await client.kick_participant(chat_id, user_id)
    elif hasattr(client, 'ban_chat_member'):
        return await client.ban_chat_member(chat_id, user_id)

# 禁言
async def mute_user(client, chat_id: Any, user_id: Any, until_date: Optional[int]=None):
    if hasattr(client, 'edit_permissions'):
        from telethon.tl.types import ChatBannedRights
        rights = ChatBannedRights(until_date=until_date or 0, send_messages=True)
        return await client.edit_permissions(chat_id, user_id, rights)
    elif hasattr(client, 'restrict_chat_member'):
        return await client.restrict_chat_member(chat_id, user_id, permissions={"can_send_messages": False}, until_date=until_date)

# 解禁
async def unmute_user(client, chat_id: Any, user_id: Any):
    if hasattr(client, 'edit_permissions'):
        from telethon.tl.types import ChatBannedRights
        rights = ChatBannedRights(until_date=None, send_messages=None)
        return await client.edit_permissions(chat_id, user_id, rights)
    elif hasattr(client, 'restrict_chat_member'):
        return await client.restrict_chat_member(chat_id, user_id, permissions={"can_send_messages": True})

# 统一异常处理装饰器
import functools

def safe_api(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"[PluginAPI] Exception: {e}")
            return None
    return wrapper

# ====== 文件/媒体支持 ======

@safe_api
async def send_photo(client, chat_id, photo, caption: str = "", **kwargs):
    if hasattr(client, 'send_file'):
        return await client.send_file(chat_id, photo, caption=caption, **kwargs)
    elif hasattr(client, 'send_photo'):
        return await client.send_photo(chat_id, photo, caption=caption, **kwargs)

@safe_api
async def send_video(client, chat_id, video, caption: str = "", **kwargs):
    if hasattr(client, 'send_file'):
        return await client.send_file(chat_id, video, caption=caption, **kwargs)
    elif hasattr(client, 'send_video'):
        return await client.send_video(chat_id, video, caption=caption, **kwargs)

@safe_api
async def send_audio(client, chat_id, audio, caption: str = "", **kwargs):
    if hasattr(client, 'send_file'):
        return await client.send_file(chat_id, audio, caption=caption, **kwargs)
    elif hasattr(client, 'send_audio'):
        return await client.send_audio(chat_id, audio, caption=caption, **kwargs)

@safe_api
async def send_document(client, chat_id, document, caption: str = "", **kwargs):
    if hasattr(client, 'send_file'):
        return await client.send_file(chat_id, document, caption=caption, **kwargs)
    elif hasattr(client, 'send_document'):
        return await client.send_document(chat_id, document, caption=caption, **kwargs)

@safe_api
async def send_sticker(client, chat_id, sticker, **kwargs):
    if hasattr(client, 'send_file'):
        return await client.send_file(chat_id, sticker, **kwargs)
    elif hasattr(client, 'send_sticker'):
        return await client.send_sticker(chat_id, sticker, **kwargs)

@safe_api
async def send_animation(client, chat_id, animation, caption: str = "", **kwargs):
    if hasattr(client, 'send_file'):
        return await client.send_file(chat_id, animation, caption=caption, **kwargs)
    elif hasattr(client, 'send_animation'):
        return await client.send_animation(chat_id, animation, caption=caption, **kwargs)

@safe_api
async def download_media(client, message, file_name: str = None):
    if hasattr(message, 'download_media'):
        return await message.download_media(file=file_name)
    elif hasattr(client, 'download_media'):
        return await client.download_media(message, file_name)

# ====== 群管理/消息管理接口 ======

@safe_api
async def get_chat_members(client, chat_id):
    if hasattr(client, 'get_participants'):
        return await client.get_participants(chat_id)
    elif hasattr(client, 'get_chat_members'):
        return await client.get_chat_members(chat_id)

@safe_api
async def promote_user(client, chat_id, user_id, **kwargs):
    if hasattr(client, 'edit_admin'): # Telethon
        return await client.edit_admin(chat_id, user_id, **kwargs)
    elif hasattr(client, 'promote_chat_member'):
        return await client.promote_chat_member(chat_id, user_id, **kwargs)

@safe_api
async def demote_user(client, chat_id, user_id):
    if hasattr(client, 'edit_admin'):
        return await client.edit_admin(chat_id, user_id, is_admin=False)
    elif hasattr(client, 'promote_chat_member'):
        return await client.promote_chat_member(chat_id, user_id, can_manage_chat=False, can_post_messages=False, can_edit_messages=False, can_delete_messages=False)

@safe_api
async def set_chat_title(client, chat_id, title):
    if hasattr(client, 'edit_title'):
        return await client.edit_title(chat_id, title)
    elif hasattr(client, 'set_chat_title'):
        return await client.set_chat_title(chat_id, title)

@safe_api
async def set_chat_photo(client, chat_id, photo):
    if hasattr(client, 'edit_photo'):
        return await client.edit_photo(chat_id, photo)
    elif hasattr(client, 'set_chat_photo'):
        return await client.set_chat_photo(chat_id, photo)

@safe_api
async def set_chat_description(client, chat_id, description):
    if hasattr(client, 'edit_about'):
        return await client.edit_about(chat_id, description)
    elif hasattr(client, 'set_chat_description'):
        return await client.set_chat_description(chat_id, description)

@safe_api
async def batch_delete_messages(client, chat_id, message_ids):
    if hasattr(client, 'delete_messages'):
        return await client.delete_messages(chat_id, message_ids)
    elif hasattr(client, 'delete_messages'):
        return await client.delete_messages(chat_id, message_ids)

@safe_api
async def pin_message(client, chat_id, message_id):
    if hasattr(client, 'pin_message'):
        return await client.pin_message(chat_id, message_id)
    elif hasattr(client, 'pin_chat_message'):
        return await client.pin_chat_message(chat_id, message_id)

@safe_api
async def unpin_message(client, chat_id, message_id):
    if hasattr(client, 'unpin_message'):
        return await client.unpin_message(chat_id, message_id)
    elif hasattr(client, 'unpin_chat_message'):
        return await client.unpin_chat_message(chat_id, message_id)

# ====== 其他建议接口可后续补充 ======
