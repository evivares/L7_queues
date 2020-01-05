"""
Plugin: HhConfig
        - is a plugin to create and retrieve configuration files.
"""


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Plugin init ("Create or retrieve configuration file"):', args, kwargs)
        import time
        self.time = time
        import configparser
        self.configparser = configparser

    def retrieveConfig(self, fp):
        start = self.time.perf_counter()

        parser = self.configparser.ConfigParser()
        parser.read(fp)

        finish = self.time.perf_counter()
        print(
            f'Finished retrieveConfig in {round(finish-start, 2)} second(s).')
        return parser

    def createConfig(self, c, fp):
        start = self.time.perf_counter()

        config = c

        with open(fp, 'w') as f:
            config.write(f)

        finish = self.time.perf_counter()
        print(f'Finished createConfig in {round(finish-start, 2)} second(s).')
        return ''

    def execute(self, q, m, h):
        start = self.time.perf_counter()

        message_count = self.get_message_count(q, m, h)

        # Loop through each message and retrieve and print the message body
        for i in range(message_count):
            with self.concfutures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.retrieve, q, m, h)

                print(future.result())

        finish = self.time.perf_counter()
        return f'Finished execution in {round(finish-start, 2)} second(s).'
