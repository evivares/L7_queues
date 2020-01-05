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
import json
import importlib

# Load modules
hhbunny_module = importlib.import_module("plugins.hhbunny", ".")
hhconfig_module = importlib.import_module("plugins.hhconfig", ".")
# hhtwilio_module = importlib.import_module("plugins.hhtwilio", ".")

# Instantiate configuration plugin with args and kwargs
hhconfig = hhconfig_module.Plugin("HhConfig", key=234)

# sample create configuration file
config = hhconfig.configparser.ConfigParser()
config['twilio'] = {
    'account_sid': 'AC1234567890',
    'auth_token': '0987654321',
    'from_number': '+17275551212'
}
hhconfig.createConfig(config, './dev.ini')

# sample retrieve configuration file
configs = hhconfig.retrieveConfig('/etc/hhcreds/hhcreds.ini')

# Instantiate rabbitmq plugin with just kwargs
hhbunny = hhbunny_module.Plugin(qname="hello", configs=configs)

"""
# Instantiate twilio plugin with no args or kwargs
hhtwilio = hhtwilio_module.Plugin("hhtwilio", configs=configs)
result = hhtwilio.execute(
    action='sendSMS', msg='This is a test SMS message using Twilio.', to_number='')
"""

# Sample publishing to queue
"""
for index in range(100):
    result = hhbunny.execute(
        action='publish', msg=f'This is the message {index}.')
"""
tmp = {
    "server": "electra",
    "source": "cstreet",
    "timestamp": "01/04/2020 21:04:36.1002",
    "type": "smsbounce",
    "message": "This is message content.",
    "id": "752799bb-7196-4fa1-9d05-641a6049e742"
}
result = hhbunny.execute(action='publish', msg=json.dumps(tmp))
print(result)

# Sample retrieving from queue
result = hhbunny.execute(action='retrieve', msg='')
print(result)

# Close the connection to RabbitMQ
hhbunny.closeConnection()
