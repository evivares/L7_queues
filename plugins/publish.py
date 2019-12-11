"""
Plugin: Publish
        - is a single threaded plugin which is used to send a message to the queue.
"""


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Plugin init ("Publish a message to the RabbitMQ Queue"):', args, kwargs)
        import pika
        self.pika = pika
        import time
        self.time = time

    def publish_message(self, q, m, h):
        # Create a new instance of the Connection object
        connection = self.pika.BlockingConnection(
            self.pika.ConnectionParameters(host=h))

        # Create a new channel with the next available channel number or pass in a channel number to use
        channel = connection.channel()

        # Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
        channel.queue_declare(queue=q)

        channel.basic_publish(
            exchange='', routing_key=q, body=m)

        print(f'[x] Published "{m}".')

        connection.close()

    def execute(self, q, m, h):
        start = self.time.perf_counter()
        self.publish_message(q, m, h)
        finish = self.time.perf_counter()
        print(f'Finished in {round(finish-start, 2)} second(s).')
