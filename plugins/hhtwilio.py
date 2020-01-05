"""
Plugin: hhtwilio
        - The sendSMS function is a single threaded plugin which is used to send a 
          SMS message to a phone number.
"""


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Plugin init ("Send SMS message using Twilio"):', args, kwargs)
        self.configs = kwargs['configs']
        self.account_sid = self.configs.get('twilio', 'account_sid')
        self.auth_token = self.configs.get('twilio', 'auth_token')
        self.from_number = self.configs.get('twilio', 'from_number')
        self.test_number = self.configs.get('twilio', 'test_number')
        from twilio.rest import Client
        self.Client = Client
        import pika
        self.pika = pika
        import time
        self.time = time

    def execute(self, action, msg, to_number):
        start = self.time.perf_counter()

        if action == 'sendSMS':
            # Send SMS via twilio
            client = self.Client(self.account_sid, self.auth_token)

            message = client.messages.create(to=self.test_number, from_=self.from_number,
                                             body=msg)

        finish = self.time.perf_counter()
        return f'Finished {action} in {round(finish-start, 2)} second(s).'
