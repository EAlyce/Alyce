"""Alyce Client Base Class"""



import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseClient(ABC):
    """Alyce Base Client"""
    def __init__(self, **kwargs):
        """BaseClient init.

        Args:
            **kwargs: config dict.
        """
        self.config = kwargs
        self.client = None

    @abstractmethod
    async def connect(self) -> bool:
        """Connect to service."""
        pass

    @abstractmethod
    async def disconnect(self):
        """Disconnect from service"""
        pass

    @abstractmethod
    async def is_connected(self) -> bool:
        """Check connection status"""
        pass

    @property
    @abstractmethod
    def me(self) -> Optional[Dict[str, Any]]:
        """Current user info"""
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