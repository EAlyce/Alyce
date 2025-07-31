""
插件管理器
"""
import asyncio
import importlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Type, TypeVar

from alyce.core.plugin.base import Plugin

T = TypeVar('T', bound='Plugin')

class PluginManager:
    """管理插件的加载、初始化和卸载"""
    
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger('alyce.plugin.manager')
        self.plugins: Dict[str, Plugin] = {}
        
    async def load_plugin(self, plugin_class: Type[T]) -> Optional[T]:
        """加载单个插件"""
        if not issubclass(plugin_class, Plugin):
            self.logger.error(f"Invalid plugin class: {plugin_class.__name__}")
            return None
            
        plugin_name = plugin_class.name
        if plugin_name in self.plugins:
            self.logger.warning(f"Plugin {plugin_name} is already loaded")
            return None
            
        try:
            plugin = plugin_class(self.client)
            await plugin.initialize()
            self.plugins[plugin_name] = plugin
            self.logger.info(f"Loaded plugin: {plugin_name}")
            return plugin
        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_name}: {e}", exc_info=True)
            return None
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """卸载指定插件"""
        plugin = self.plugins.pop(plugin_name, None)
        if not plugin:
            self.logger.warning(f"Plugin {plugin_name} is not loaded")
            return False
            
        try:
            await plugin.cleanup()
            self.logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error unloading plugin {plugin_name}: {e}", exc_info=True)
            return False
    
    async def load_plugins_from_path(self, path: str):
        """从指定路径加载所有插件"""
        plugins_dir = Path(path)
        if not plugins_dir.exists() or not plugins_dir.is_dir():
            self.logger.warning(f"Plugins directory not found: {path}")
            return
            
        # 实现插件自动发现和加载
        # 注意：实际实现中需要更完善的插件发现机制
        pass
    
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
