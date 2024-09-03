import pika
import time
import json
from models import SessionLocal, HttpLog
from init_db import initialize_db

# TODO: USE env vars, decouple logic

rabbitmq_host = 'rabbitmq'
rabbitmq_port = 5672
rabbitmq_user = 'user'
rabbitmq_password = 'password'

def connect_to_rabbitmq(retries=5, delay=5):
    for i in range(retries):
        try:
            credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
            parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            print("Connected to RabbitMQ")
            return connection
        except Exception as e:
            print(f"Failed to connect to RabbitMQ, attempt {i+1} of {retries}: {e}")
            time.sleep(delay)
    print("All attempts to connect to RabbitMQ failed.")
    exit(1)

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        print(f"Received message: {message}")

        db = SessionLocal()
        log_entry = HttpLog(
            timestamp=message['timestamp'],
            status_code=message['status_code'],
            client_ip=message.get('client_ip'),
            method=message.get('method'),
            endpoint=message.get('endpoint')
        )
        db.add(log_entry)
        db.commit()
        db.close()

        print("Message inserted into PostgreSQL")
    except Exception as e:
        print(f"Failed to insert message into PostgreSQL: {e}")

if __name__ == "__main__":
    initialize_db()
    rabbitmq_connection = connect_to_rabbitmq()

    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue='http_logs')

    channel.basic_consume(
        queue='http_logs',
        on_message_callback=callback,
        auto_ack=True
    )

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
