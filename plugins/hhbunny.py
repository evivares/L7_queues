"""
Plugin: hhbunny
        - The retrieve function is a multi-threaded plugin that retrieves messages 
          from the queue one at a time and prints message body.
        - The publish function is a single threaded plugin which is used to send a 
          message to the queue.
"""


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Plugin init ("Publish/Retrieve messages to/from RabbitMQ Queue"):', args, kwargs)
        import onesignal
        self.onesignal = onesignal
        import json
        self.json = json
        import pika
        self.pika = pika
        import time
        self.time = time
        import concurrent.futures
        self.configs = kwargs['configs']
        self.qname = kwargs['qname']
        self.app_auth_key = self.configs.get('onesignal', 'app_auth_key')
        self.app_id = self.configs.get('onesignal', 'app_id')
        self.host = self.configs.get('rabbitmq', 'host')
        self.uname = self.configs.get('rabbitmq', 'uname')
        self.pword = self.configs.get('rabbitmq', 'pword')
        self.concfutures = concurrent.futures
        self.onesignal_client = self.onesignal.Client(
            app_auth_key=self.app_auth_key, app_id=self.app_id)
        self.connection = self.startConnection()

    def startConnection(self):
        # Create a new instance of the Connection object
        credentials = self.pika.credentials.PlainCredentials(
            self.uname, self.pword)
        connection = self.pika.BlockingConnection(
            self.pika.ConnectionParameters(host=self.host, credentials=credentials))
        return connection

    def closeConnection(self):
        # Close the connection
        self.connection.close()

    def publish_message(self, msg):
        # Create a new channel with the next available channel number or pass in a channel number to use
        connection = self.connection
        channel = connection.channel()

        # Declare queue, create if needed. This method creates or checks a queue. When creating
        # a new queue the client can specify various properties that control the durability of
        # the queue and its contents, and the level of sharing for the queue.
        channel.queue_declare(queue=self.qname)

        channel.basic_publish(
            exchange='', routing_key=self.qname, body=msg)

        print(f'[x] Published "{msg}".')

    def retrieve(self):
        # Create a new channel with the next available channel number or pass in a channel number to use
        connection = self.connection
        channel = connection.channel()

        # Declare queue, create if needed. This method creates or checks a queue. When creating a new
        # queue the client can specify various properties that control the durability of the queue and
        # its contents, and the level of sharing for the queue.
        channel.queue_declare(queue=self.qname)

        method_frame, header_frame, body = channel.basic_get(queue=self.qname)
        if method_frame == None or method_frame.NAME == 'Basic.GetEmpty':
            return ''
        else:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            return body

    def get_message_count(self):
        # Create a new channel with the next available channel number or pass in a channel number to use
        connection = self.connection
        channel = connection.channel()

        # Declare queue, create if needed. This method creates or checks a queue. When creating a new
        # queue the client can specify various properties that control the durability of the queue and
        # its contents, and the level of sharing for the queue.
        # channel.queue_declare(queue=q)

        queue = channel.queue_declare(
            queue=self.qname, auto_delete=False
        )
        return queue.method.message_count

    def sendNotification(self, jsn):
        player_id = []
        player_id.append(jsn['id'])
        new_notification = self.onesignal.Notification(post_body={
            "contents": {"en": jsn['message']},
            "include_player_ids": player_id,
        })
        onesignal_response = self.onesignal_client.send_notification(
            new_notification)
        # print(onesignal_response.status_code)
        print(onesignal_response.json())

    def execute(self, action, msg):
        start = self.time.perf_counter()

        if action == 'retrieve':
            # Get message count
            message_count = self.get_message_count()

            # Loop through each message and retrieve and print the message body
            for i in range(message_count):
                with self.concfutures.ThreadPoolExecutor() as executor:
                    jsn = self.json.loads(
                        executor.submit(self.retrieve).result())
                    if jsn['type'] == 'smsbounce':
                        # self.sendNotification(jsn)
                        executor.submit(self.sendNotification, jsn)

        elif action == 'publish':
            self.publish_message(msg)

        finish = self.time.perf_counter()
        return f'Finished {action} in {round(finish-start, 2)} second(s).'
