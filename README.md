# plugin_system
Plugin system for python code and uses the `pika` python module and `concurrent.futures` module for multi-threading in order to interact with RabbitMQ. The code also utilizes the `importlib` python module to dynamically load your custom modules inside the `plugins` folder.

There are two(2) sample plugin modules inside the `plugins` folder. The `publish` plugin is a plugin that is used to send a message to a RabbitMQ queue. The `retrieve` plugin is a plugin that is used to get messages from a RabbitMQ queue and just currently prints the message but could easily be modified to execute a function that does processing on the message.

The examples uses a common `execute` function that can be called with the same number of arguments.

## Dynamically loading a plugin
1. Create your plugin in the `plugins` folder with a class of `Plugin`.
2. Modify the `app.py` file replacing the **PLUGIN_NAME** variable with the plugin to be dynamically loaded.
3. Call the `execute` function providing the arguments.
