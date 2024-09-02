import pika
import time

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

if __name__ == "__main__":
    connection = connect_to_rabbitmq()

