import json

import pika
import random
from base64 import b64encode


# from hms_message_audit.hms_logger import HMSLogger
# from hms_message_audit.hms_standard_message import StandardMessage


class RabbitMQ:
    def __init__(self, rmq_settings, auto_connect=True):
        # self._logger = HMSLogger().get_logger()

        rabbitmq_setting = rmq_settings
        self.host = rabbitmq_setting.get('host')
        self.port = rabbitmq_setting.get('port')
        self.api_port = rabbitmq_setting.get('api_port')
        self.vhost = rabbitmq_setting.get('vhost')
        self.timeout = rabbitmq_setting.get('check_queue_available_timeout')

        self._user = rabbitmq_setting.get('username')
        self._pass = rabbitmq_setting.get('password')
        basic_auth_text = f"{self._user}:{self._pass}".encode()
        self.token = b64encode(basic_auth_text).decode("ascii")

        self.props = pika.BasicProperties(content_type='text/plain', delivery_mode=2)
        credentials = pika.PlainCredentials(username=self._user, password=self._pass)
        parameters = list()
        for item in self.host:
            conn_params = pika.ConnectionParameters(host=item, port=self.port, virtual_host=self.vhost,
                                                    credentials=credentials, heartbeat=600,
                                                    blocked_connection_timeout=600)
            parameters.append(conn_params)
        self._parameters = parameters

        self.connection = None
        self.channel = None

        if auto_connect:
            self.connect()

    def connect(self):
        random.shuffle(self._parameters)
        self.connection = pika.BlockingConnection(self._parameters)
        self.channel = self.connection.channel()
        # self._logger.info(StandardMessage.INFO_RABBITMQ_CONNECTED.format(host=self._parameters[0].host))

    def is_closed(self):
        return self.connection.is_closed

    def close(self):
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        self.channel.close()
        # self._logger.info(StandardMessage.INFO_RABBITMQ_CHANNEL_CLOSED)

    def close_connection(self):
        self.connection.close()
        # self._logger.info(StandardMessage.INFO_RABBITMQ_CONNECTION_CLOSED)

    def queue_declare(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def publish_data(self, data, queue_name):
        encode_data = json.dumps(data, indent=2).encode('utf-8')
        self.channel.basic_publish(exchange='', routing_key=queue_name, properties=self.props,
                                   body=encode_data)
