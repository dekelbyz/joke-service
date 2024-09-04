from queue_publisher_middleware.model import EventDetails
import pika  # type: ignore
import json
from queue_publisher_middleware import consts
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class _RabbitMQHandler:
    def __init__(self, queue):
        self.credentials = pika.PlainCredentials(
            consts.RABBITMQ_USER, consts.RABBITMQ_PASSWORD
        )

        self.connection_parameters = pika.ConnectionParameters(
            host=consts.RABBITMQ_HOST, credentials=self.credentials
        )
        self.queue = queue
        self.connection = None
        self._channel = None

    @property
    def channel(self):
        self._connect()
        return self._channel

    def _connect(self) -> None:
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.connection_parameters)
            self._channel = self.connection.channel()
            self._channel.queue_declare(queue=self.queue)

    def publish(self, message: EventDetails):
        try:
            self.channel.basic_publish(
                exchange="", routing_key=self.queue, body=json.dumps(message)
            )

        except Exception as e:
            logging.error("Failed to publish to queue:", e)
            raise e


rabbit_mq_handler = _RabbitMQHandler(queue=consts.RABBITMQ_JOKE_METADATA_QUEUE)
