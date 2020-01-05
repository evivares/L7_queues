"""
Plugin: Retrieve
        - is a multi-threaded plugin that retrieves messages from the queue one at a time
          and prints message body.
"""


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Plugin init ("Retrieve messages from RabbitMQ Queue"):', args, kwargs)
        self.configs = kwargs['configs']
        import pika
        self.pika = pika
        import time
        self.time = time
        import concurrent.futures
        self.concfutures = concurrent.futures

    def retrieve(self, q, m, h):
        # Create a new instance of the Connection object
        credentials = self.pika.credentials.PlainCredentials(
            self.configs.get('rabbitmq', 'uname'),
            self.configs.get('rabbitmq', 'pword'))
        connection = self.pika.BlockingConnection(
            self.pika.ConnectionParameters(host=h, credentials=credentials))

        # Create a new channel with the next available channel number or pass in a channel number to use
        channel = connection.channel()

        # Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
        channel.queue_declare(queue=q)

        method_frame, header_frame, body = channel.basic_get(queue=q)
        if method_frame == None or method_frame.NAME == 'Basic.GetEmpty':
            connection.close()
            return ''
        else:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            connection.close()
            return body

    def get_message_count(self, q, m, h):
        # Create a new instance of the Connection object
        credentials = self.pika.credentials.PlainCredentials(
            self.configs.get('rabbitmq', 'uname'),
            self.configs.get('rabbitmq', 'pword'))
        connection = self.pika.BlockingConnection(
            self.pika.ConnectionParameters(host=h, credentials=credentials))

        # Create a new channel with the next available channel number or pass in a channel number to use
        channel = connection.channel()

        # Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
        # channel.queue_declare(queue=q)

        queue = channel.queue_declare(
            queue=q, auto_delete=False
        )
        return queue.method.message_count

    def execute(self, q, m, h):
        start = self.time.perf_counter()

        message_count = self.get_message_count(q, m, h)

        # Loop through each message and retrieve and print the message body
        for i in range(message_count):
            with self.concfutures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.retrieve, q, m, h)

                print(future.result())

        finish = self.time.perf_counter()
        return f'Finished in {round(finish-start, 2)} second(s).'
