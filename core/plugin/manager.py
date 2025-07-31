import asyncio
import importlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Type, TypeVar
from .base import BasePlugin

T = TypeVar('T', bound='BasePlugin')

class PluginManager:
    """Plugin manager class."""

    def __init__(self, client):
        self.client = client
        self.logger = get_logger('alyce.plugin.manager')
        self.plugins: Dict[str, BasePlugin] = {}

    async def load_plugin(self, plugin_class: Type[T]) -> Optional[T]:
        """Load a plugin."""
        if not issubclass(plugin_class, BasePlugin):
            self.logger.error(f"Invalid plugin class: {plugin_class.__name__}")
            return None
        plugin_name = plugin_class.name
        if plugin_name in self.plugins:
            self.logger.warning(f"Plugin {plugin_name} is already loaded")
            return None
        try:
            plugin = plugin_class(self.client)
            try:
                await plugin.initialize()
            except Exception as e:
                self.logger.error(f"Plugin {plugin_name} on_load/init error: {e}")
                if hasattr(plugin, 'on_error'):
                    await plugin.on_error(e)
                return None
            self.plugins[plugin_name] = plugin
            self.logger.info(f"Loaded plugin: {plugin_name}")
            if hasattr(plugin, 'on_load'):
                await plugin.on_load()
            return plugin
        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_class.__name__}: {e}", exc_info=True)
            return None

    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin."""
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            self.logger.warning(f"Plugin {plugin_name} not found")
            return False
        try:
            try:
                await plugin.cleanup()
            except Exception as e:
                self.logger.error(f"Plugin {plugin_name} on_unload/cleanup error: {e}")
                if hasattr(plugin, 'on_error'):
                    await plugin.on_error(e)
            if hasattr(plugin, 'on_unload'):
                await plugin.on_unload()
            del self.plugins[plugin_name]
            self.logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to unload plugin {plugin_name}: {e}", exc_info=True)
            return False

    async def load_plugins_from_path(self, path: str):
        """Load plugins from a directory."""
        plugins_dir = Path(path)
        if not plugins_dir.exists() or not plugins_dir.is_dir():
            self.logger.warning(f"Plugins directory not found: {path}")
            return
        import importlib.util
        for file in plugins_dir.glob("*.py"):
            if file.name.startswith("_") or file.name in ("decorators.py", "api.py", "loader.py"):
                continue
            spec = importlib.util.spec_from_file_location(file.stem, str(file))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.logger.info(f"Loaded plugin module: {file.name}")

    async def initialize(self):
        """Initialize all plugins."""
        tasks = [plugin.initialize() for plugin in self.plugins.values()]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def cleanup(self):
        """Cleanup all plugins."""
        tasks = [self.unload_plugin(name) for name in list(self.plugins.keys())]
        await asyncio.gather(*tasks, return_exceptions=True)

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get a plugin by name."""
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        """List all plugins."""
        return list(self.plugins.keys())