import pika
import time
import json
import logging
from models import SessionLocal, HttpLog
from db_handler import DatabaseHandler
# from init_db import initialize_db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RabbitMQConsumer:
    def __init__(self, host, port, user, password, queue_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self, retries=5, delay=5):
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
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=False)
        logging.info("Waiting for messages. To exit press CTRL+C")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop_consuming()

    def callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            logging.info(f"Received message: {message}")

            db_handler = DatabaseHandler()
            db_handler.insert_log(message)

            logging.info("Message inserted into PostgreSQL")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(f"Failed to insert message into PostgreSQL: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def stop_consuming(self):
        logging.info("Stopping consumer...")
        if self.channel is not None:
            self.channel.stop_consuming()
        if self.connection is not None:
            self.connection.close()

# class DatabaseHandler:
#     def __init__(self):
#         self.db = SessionLocal()

#     def insert_log(self, message):
#         log_entry = HttpLog(
#             timestamp=message['timestamp'],
#             status_code=message['status_code'],
#             client_ip=message.get('client_ip'),
#             method=message.get('method'),
#             account=message.get('account'),
#             endpoint=message.get('endpoint')
#         )
#         self.db.add(log_entry)
#         self.db.commit()
#         self.db.close()

# if __name__ == "__main__":
#     initialize_db()

#     rabbitmq_consumer = RabbitMQConsumer(
#         host='rabbitmq',
#         port=5672,
#         user='user',
#         password='password',
#         queue_name='http_logs'
#     )

#     rabbitmq_consumer.connect()
#     rabbitmq_consumer.start_consuming()
