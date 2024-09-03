import pika # type: ignore
import json
import logging
import time
from db_handler import DatabaseHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RabbitMQConsumer:
    '''
    RabbitMQConsumer Class
    In charge of everything related to RabbitMQ on the consumer end (connecting, consuming etc)
    It is also in charge of triggering DB insertion
    This class is pretty generic:
     - It can work with every RabbitMQ queue
     - It can work with every db_handler that has the insert_log method, doesn't have to be postgres 
    '''
    def __init__(self, host: str, 
                       port: int, 
                       user: str, 
                       password: str,
                       queue_name: str,
                       db_handler: DatabaseHandler):
        ''' RabbitMQConsumer constructor '''
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.queue_name = queue_name
        self.db_handler = db_handler
        self.connection = None
        self.channel = None

    def connect(self, retries=5, delay=10):
        # Usually I tend to adhere to the SRP (SOLID), but that would also do the trick for now
        '''
        Connects to RabbitMQ server
        :param retries: int - the number of connectivity retries
        :param delay: int -the number of seconds you want to wait between connection retry

        In a natural way, the rabbitMQ container takes longer to be ready, so the first few attempts 
        Will probably fail. Don't freak out
        '''
        for _ in range(retries):
            try:
                credentials = pika.PlainCredentials(self.user, self.password)
                parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                logging.info("Connected to RabbitMQ")
                return
            except Exception:
                time.sleep(delay)
        logging.critical("All attempts to connect to RabbitMQ failed.")
        exit(1)

    def start_consuming(self):
        self.channel.queue_declare(queue=self.queue_name) # creates the queue in case missing
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.consume, auto_ack=False) 
        logging.info("Waiting for messages")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop_consuming()

    def consume(self, ch, method, properties, body):
        '''
        Callback method for consuming messages
        This function also triggers the DB writing 
        '''
        try:
            message = json.loads(body)
            event_id = method.delivery_tag
            message['event_id'] = event_id

            logging.info(f"Received message: {message}")

            self.db_handler.insert_log(message)

            logging.info("Message inserted into PostgreSQL")
            ch.basic_ack(event_id)
        except Exception as e:
            logging.error(f"Failed to insert message into PostgreSQL: {e}")
            ch.basic_nack(event_id)

    def stop_consuming(self):
        logging.info("Stopping consumer...")
        if self.channel is not None:
            self.channel.stop_consuming()
        if self.connection is not None:
            self.connection.close()
        logging.info("RabbitMQ connection closed")
