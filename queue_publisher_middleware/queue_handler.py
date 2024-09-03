from queue_publisher_middleware.model import EventDetails
import pika
import json
from queue_publisher_middleware import consts

def send_to_rabbitmq(queue:str, message: EventDetails):
    '''
    Publishes an event to rabbitMQ
    * Configurable to work with any RabbitMQ queue 
    :param message: EventDetails 
    :param queue: the desired queue name
    '''
    credentials = pika.PlainCredentials(consts.RABBITMQ_USER,consts.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=consts.RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    
    channel.queue_declare(queue=queue)
    
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message)
    )
    
    connection.close()