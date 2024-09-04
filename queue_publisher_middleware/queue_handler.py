from queue_publisher_middleware.model import EventDetails
import pika  # type: ignore
import json
from queue_publisher_middleware import consts
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class _RabbitMQHandler:
    """
    A class for handling RabbitMQ interaction
    In this case that would be connection and publishing messages
    """

    def __init__(self, queue: str) -> None:
        """
        This constructor constructs initial variables for interaction with RabbitMQ
        :param queue: the queue name we want to interact with
        """

        # connection credentials
        self.credentials = pika.PlainCredentials(
            consts.RABBITMQ_USER, consts.RABBITMQ_PASSWORD
        )

        self.connection_parameters = pika.ConnectionParameters(
            host=consts.RABBITMQ_HOST, credentials=self.credentials
        )
        self.queue = queue

        # initially set to None, values will be assigned by the _connect method
        self.connection = None
        self._channel = None

    @property
    def channel(self):
        self._connect()
        return self._channel

    def _connect(self) -> None:
        """
        This method establishes a connection in case there isn't already one (singleton pattern)
        """
        if not self.connection or self.connection.is_closed:

            # This is the code that actually creates the connection
            self.connection = pika.BlockingConnection(self.connection_parameters)
            self._channel = self.connection.channel()
            self._channel.queue_declare(queue=self.queue)

    def publish(self, message: EventDetails):
        """
        Publishes a message to the queue
        :param message: in our case that would be the event details
        """
        try:
            self.channel.basic_publish(
                exchange="", routing_key=self.queue, body=json.dumps(message)
            )

        except Exception as e:
            logging.error("Failed to publish to queue:", e)
            raise e


# instantiating the _RabbitMQHandler once (no need to re-instantiating it every time)
rabbit_mq_handler = _RabbitMQHandler(queue=consts.RABBITMQ_JOKE_METADATA_QUEUE)
