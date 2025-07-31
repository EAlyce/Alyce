"""
Alyce - Telegram 客户端框架

主入口文件
"""
import asyncio
import sys
from pathlib import Path

from core.client.telegram import TelegramClient
from utils.config import config
from utils.logging import setup_logger

# 配置日志
logger = setup_logger(level='DEBUG' if config.get_bool('DEBUG') else 'INFO')

async def main():
    """主函数"""
    # 验证配置
    if not config.validate():
        logger.error("Missing required configuration. Please check your .env file.")
        print("\nPlease create a .env file with the following content:")
        print("""
# Telegram API credentials
API_ID=your_api_id
API_HASH=your_api_hash
PHONE=your_phone_number  # with country code, e.g., +1234567890

# Optional
# SESSION_PATH=session  # default: 'session'
# DEBUG=True           # enable debug logging
""")
        return 1
    
    # 创建并启动客户端
    client = TelegramClient()
    
    try:
        # 连接
        if not await client.connect():
            return 1
            
        # 保持运行直到用户中断
        print("\nConnected to Telegram! Press Ctrl+C to exit.")
        print(f"Logged in as: {client.me.first_name} (@{client.me.username or 'N/A'})")
        
        while await client.is_connected():
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\nDisconnecting...")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return 1
    finally:
        # 确保客户端正确关闭
        await client.disconnect()
    
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
