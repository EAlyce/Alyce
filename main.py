"""Alyce - Telegram client entry point"""

import asyncio
import sys
from core.client.telegram import TelegramClient
from utils.config import config
from utils.logging import setup_logger

# Setup logger
logger = setup_logger(level='DEBUG' if config.get_bool('DEBUG') else 'INFO')

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
    client = TelegramClient()
    try:
        # Connect to Telegram
        if not await client.connect():
            return 1

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
        await client.disconnect()
        return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))