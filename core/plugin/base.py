"""
Alyce Plugin Base Class

All plugins must inherit from this class. It defines the basic metadata
and lifecycle hooks for a plugin.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict


class BasePlugin(ABC):
    """
    Abstract base class for all Alyce plugins.

    Attributes:
        name (str): A unique identifier for the plugin (e.g., 'my_awesome_plugin').
        version (str): The version of the plugin (e.g., '0.1.0').
        description (str): A brief description of what the plugin does.
        enabled (bool): Whether the plugin is currently enabled.
    """

    # --- Plugin Metadata ---
    name: str = "unnamed_plugin"
    version: str = "0.0.1"
    description: str = "No description provided."
    enabled: bool = True

    def __init__(self, client: Any):
        """
        Initializes the plugin.

        Args:
            client: The main Alyce client instance.
        """
        self.client = client
        self.logger = logging.getLogger(f"alyce.plugin.{self.name}")
        self.config: Dict[str, Any] = {}  # Plugin-specific configuration

    async def on_load(self) -> None:
        """
        Asynchronous hook called when the plugin is loaded and initialized.
        Use this for setup tasks like registering commands or event handlers.
        """
        pass

    async def on_unload(self) -> None:
        """
        Asynchronous hook called when the plugin is unloaded or the client shuts down.
        Use this for cleanup tasks.
        """
        pass

    def __str__(self) -> str:
        """Returns a string representation of the plugin."""
        return f"{self.__class__.__name__}(name='{self.name}', version='{self.version}')"

    def __repr__(self) -> str:
        """Returns a detailed string representation of the plugin."""
        return str(self)