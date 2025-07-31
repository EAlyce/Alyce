"""Alyce Client Base Class

This module provides a unified base class for all Telegram client implementations,
defining core interfaces for connecting, disconnecting, and plugin management.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type

from telethon import TelegramClient

from core.plugin.manager import PluginManager


class BaseClient(ABC):
    """Alyce Client Base Class"""

    def __init__(self, **kwargs):
        """
        Initializes the Alyce Client.

        Args:
            **kwargs: Client configuration parameters.
        """
        self.config = kwargs
        self.client: Optional[TelegramClient] = None
        self.plugin_manager = PluginManager(self)

    @abstractmethod
    async def connect(self) -> bool:
        """Connect to the Telegram server."""
        pass

    @abstractmethod
    async def disconnect(self):
        """Disconnect from the Telegram server."""
        pass

    @abstractmethod
    async def is_connected(self) -> bool:
        """Check if the client is connected."""
        pass

    async def run(self):
        """Run the client's main loop."""
        try:
            # Connect to Telegram
            if not await self.connect():
                raise RuntimeError("Failed to connect to Telegram")

            # Initialize plugins
            await self.plugin_manager.initialize()

            # Keep running until disconnected
            while await self.is_connected():
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            pass
        finally:
            # Cleanup resources
            await self.plugin_manager.cleanup()
            await self.disconnect()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(connected={self.client is not None and self.client.is_connected()})"