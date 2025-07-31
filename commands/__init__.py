# Alyce Command Plugins
# Auto-import all command plugins for registration
import os
import importlib

plugin_dir = os.path.dirname(__file__)
for fname in os.listdir(plugin_dir):
    if fname.endswith('.py') and fname not in ('__init__.py', 'base.py'):
        modname = f"{__name__}.{fname[:-3]}"
        importlib.import_module(modname)
