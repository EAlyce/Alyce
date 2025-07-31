"""Alyce - Telegram 客户端启动入口"""

import asyncio
import sys
from core.client.telegram import TelegramClient
from utils.config import config
from utils.logging import setup_logger

# 配置日志
logger = setup_logger(level='DEBUG' if config.get_bool('DEBUG') else 'INFO')

async def main():
    """主入口函数"""
    # 校验配置
    if not config.validate():
        logger.error("缺少必要配置，请检查 .env 文件。")
        print("\n请创建 .env 文件，内容如下：")
        print("""
# Telegram API credentials
API_ID=your_api_id
API_HASH=your_api_hash
PHONE=your_phone_number  # 带国家码, 如 +8613800138000
# 可选项
# SESSION_PATH=session
# DEBUG=True
""")
        return 1

    # 创建并启动客户端
    client = TelegramClient()
    try:
        # 连接 Telegram
        if not await client.connect():
            return 1

        print("\n已连接 Telegram！按 Ctrl+C 退出。")
        print(f"当前账号：{client.me.first_name} (@{client.me.username or '无用户名'})")

        while await client.is_connected():
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n正在断开连接...")

    except Exception as e:
        logger.error(f"运行时异常: {e}", exc_info=True)
        return 1

    finally:
        await client.disconnect()
        return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))