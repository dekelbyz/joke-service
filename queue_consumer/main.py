from init_db import initialize_db
from consumer import RabbitMQConsumer


def main():
    initialize_db()

    rabbitmq_consumer = RabbitMQConsumer(
        host='rabbitmq',
        port=5672,
        user='user',
        password='password',
        queue_name='http_logs'
    )

    rabbitmq_consumer.connect()
    rabbitmq_consumer.start_consuming()


if __name__ == "__main__":
    main()
