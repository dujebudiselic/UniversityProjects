import os
import importlib
from plugin import plugin

def myfactory(name):
    module = importlib.import_module(f"plugins.{name}")
    return getattr(module, name)

def getPlugins():
    plugins = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plugins_dir = os.path.join(script_dir, 'plugins')
    for mymodule in os.listdir(plugins_dir):
        moduleName, moduleExt = os.path.splitext(mymodule)
        if moduleExt == '.py':
            pluginClass = myfactory(moduleName)
            instance = pluginClass()
            if isinstance(instance, plugin):
                plugins.append(instance)
    return plugins