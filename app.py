"""
This App can be used to dynamically load plugin modules in the plugin folder. The execute function
is what is used to call the function inside the plugin.

Parameters:
    q = queue name
    m = message
    h = host

"""
# traditional way of importing modules
# dynamically importing modules
import importlib

PLUGIN_NAME = "plugins.retrieve"

plugin_module = importlib.import_module(PLUGIN_NAME, ".")

print(plugin_module)

plugin = plugin_module.Plugin("hello", key=123)

# plugin.execute(q, m, h)
result = plugin.execute('hello', 'This is test 3 message!', 'localhost')
print(result)
