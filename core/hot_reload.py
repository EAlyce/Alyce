"""
插件热加载/卸载框架
支持运行时动态加载、卸载、重载插件
"""
import importlib
import sys
from typing import Dict

class HotReloader:
    def __init__(self):
        self.loaded: Dict[str, object] = {}

    def load(self, module_name: str):
        module = importlib.import_module(module_name)
        self.loaded[module_name] = module
        return module

    def reload(self, module_name: str):
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        else:
            self.load(module_name)

    def unload(self, module_name: str):
        if module_name in sys.modules:
            del sys.modules[module_name]
        self.loaded.pop(module_name, None)
