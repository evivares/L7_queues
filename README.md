# plugin_system
Plugin system for python code that utilizes the `pika` and `concurrent.futures` python libraries. `concurrent.futures` is used for multi-threading. The sample plugins are used to interact with RabbitMQ broker. The code also utilizes the `importlib` python library to dynamically load your custom modules inside the `plugins` folder.

There are two(2) sample plugin modules inside the `plugins` folder. The `publish` plugin is a plugin that is used to send a message to a RabbitMQ queue. The `retrieve` plugin is a plugin that is used to get messages from a RabbitMQ queue and just currently prints the message but could easily be modified to execute a function that does processing on the message.

The examples uses a common `execute` function that can be called with the same number of arguments.

## Creating the RabbitMQ Managment Console Docker container
At the command prompt, run the command below to spin up the RabbitMQ container in daemon mode:

`$ docker-compose up -d`

## Dynamically loading a plugin
1. First, you need to install the required python libraries.

   `(venv)$ pip3 install -r requirements.txt`

2. Create your plugin in the `plugins` folder with a class of `Plugin`.
3. Modify the `app.py` file replacing the **PLUGIN_NAME** variable with the plugin to be dynamically loaded.
4. Call the `execute` function providing the arguments:

```
q = queue name
m = message
h = RabbitMQ hostname
```
