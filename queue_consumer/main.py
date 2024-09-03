from db_handler import DatabaseHandler
from consumer import RabbitMQConsumer
import consts

def main():
    db_handler = DatabaseHandler()

    rabbitmq_consumer = RabbitMQConsumer(
        host=consts.RABBITMQ_HOST,
        port=consts.RABBITMQ_PORT,
        user=consts.RABBITMQ_USER,
        password=consts.RABBITMQ_PASSWORD,
        queue_name=consts.RABBITMQ_JOKE_METADATA_QUEUE,
        db_handler=db_handler  # Pass the handler to the consumer (dependency injection)
    )

    rabbitmq_consumer.connect()
    rabbitmq_consumer.start_consuming()

if __name__ == "__main__":
    main()
