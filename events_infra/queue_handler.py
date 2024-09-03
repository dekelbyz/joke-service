from events_infra.model import EventDetails
import pika
import json


# TODO: use env vars
def send_to_rabbitmq(message: EventDetails):
    credentials = pika.PlainCredentials('user','password')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
    channel = connection.channel()
    
    channel.queue_declare(queue='http_logs')
    
    channel.basic_publish(
        exchange='',
        routing_key='http_logs',
        body=json.dumps(message)
    )
    
    connection.close()