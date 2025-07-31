"""
插件自动加载器
扫描插件目录，兼容 PagerMaid 单文件插件
"""
import importlib.util
import os
from pathlib import Path

PLUGIN_PATH = Path(__file__).parent


def load_plugins(dispatcher, commands):
    for file in PLUGIN_PATH.glob("*.py"):
        if file.name.startswith("_") or file.name in ("decorators.py", "api.py", "loader.py"):
            continue
        spec = importlib.util.spec_from_file_location(file.stem, str(file))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
