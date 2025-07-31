"""
插件管理器

负责插件的加载、初始化和卸载。
"""
import asyncio
import importlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Type, TypeVar

from alyce.core.plugin.base import BasePlugin

T = TypeVar('T', bound='BasePlugin')

class PluginManager:
    """管理插件的加载, 初始化和卸载"""
    
    def __init__(self, client):
        self.client = client
        self.logger = get_logger('alyce.plugin.manager')
        self.plugins: Dict[str, BasePlugin] = {}
        
    async def load_plugin(self, plugin_class: Type[T]) -> Optional[T]:
        """加载单个插件"""
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
        """卸载指定插件"""
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
        """从指定路径加载所有插件（支持 Alyce 和 PagerMaid 风格）"""
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
        # 兼容 Alyce 原生插件加载机制（类式插件）
        # TODO: 可根据实际需求进一步完善

    
    async def initialize(self):
        """初始化所有已加载的插件"""
        tasks = [plugin.initialize() for plugin in self.plugins.values()]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def cleanup(self):
        """清理所有插件资源"""
        tasks = [self.unload_plugin(name) for name in list(self.plugins.keys())]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """获取指定名称的插件实例"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[str]:
        """获取所有已加载的插件名称"""
        return list(self.plugins.keys())
