"""Alyce - Telegram client entry point"""

import asyncio
import sys
import os
from core.client.telegram import TelegramClient
from utils.config import config
from utils.logging import setup_logger

# Setup logger
logger = setup_logger(
    level='DEBUG' if config.get_bool('DEBUG') else 'INFO',
    log_file='alyce.log'
)

async def main():
    """Main entry function"""
    # Validate config
    if not config.validate():
        logger.error("Missing required configuration. Please check your .env file.")
        print("\nPlease create a .env file with the following content:")
        print("""
# Telegram API credentials
API_ID=your_api_id
API_HASH=your_api_hash
PHONE=your_phone_number  # with country code, e.g., +1234567890
# Optional
# SESSION_PATH=session
# DEBUG=True
""")
        return 1

    # Create and start client
    global_client = TelegramClient()
    try:
        # Connect to Telegram
        if not await global_client.connect():
            return 1

        logger.info("Alyce 启动中...")
        print("Connected to Telegram! Press Ctrl+C to exit.")
        print(f"Logged in as: {global_client.me.first_name} (@{global_client.me.username or 'N/A'})")

        # 自动重启后 edit 上次 update 消息为“重启完成”
        import os
        if os.path.isfile('.reboot'):
            try:
                with open('.reboot', 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                os.remove('.reboot')
                if ',' in content:
                    chat_id, msg_id = content.split(',', 1)
                    chat_id = int(chat_id)
                    msg_id = int(msg_id)
                    try:
                        await global_client.client.edit_message(chat_id, msg_id, '✅ Alyce 已重启完成！')
                    except Exception:
                        # edit 失败则发新消息
                        try:
                            await global_client.client.send_message(chat_id, '✅ Alyce 已重启完成！')
                        except Exception:
                            pass
            except Exception:
                pass

        while await global_client.is_connected():
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\nDisconnecting...")

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return 1

    finally:
        await global_client.disconnect()
        return 0

if __name__ == "__main__":
    import time
    import os
    import sys
    import glob
    import sqlite3

    # 检查 session 文件是否被锁
    def is_sqlite_locked(session_glob='*.session'):
        for sfile in glob.glob(session_glob):
            try:
                conn = sqlite3.connect(sfile, timeout=1)
                conn.execute('BEGIN EXCLUSIVE')
                conn.close()
            except sqlite3.OperationalError as e:
                if 'locked' in str(e):
                    print(f"[Alyce] 检测到 session 文件被锁: {sfile}\n请确认没有多开 Alyce 或 Telethon 程序，或删除 session 文件后重试。")
                    return True
        return False

    if is_sqlite_locked():
        sys.exit(1)

    import asyncio
    try:
        exit_code = asyncio.run(main())
    except Exception as e:
        print(f"[Alyce] 主循环异常: {e}")
        exit_code = 1
    except KeyboardInterrupt:
        print("[Alyce] 收到 Ctrl+C，优雅退出。")
        exit_code = 0
    sys.exit(exit_code)