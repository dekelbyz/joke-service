from db_handler import DatabaseHandler
from consumer import RabbitMQConsumer
import consts

def main():
    '''
    Main function
    Orchestrates the entire consuming & DB writing process
    Order of business:

    - Instantiates DB Handler - which initializes DB on its constructor
    - Instantiates RabbitMQ consumer class - which is in charge of the consuming process
    * Note - the RabbitMQ consumer also triggers the DB Writing process, that's why he's receiving 
      the db_handler instance as an argument.
    '''
    db_handler = DatabaseHandler()

    rabbitmq_consumer = RabbitMQConsumer(
        host=consts.RABBITMQ_HOST,
        port=consts.RABBITMQ_PORT,
        user=consts.RABBITMQ_USER,
        password=consts.RABBITMQ_PASSWORD,
        queue_name=consts.RABBITMQ_JOKE_METADATA_QUEUE,

        # RabbitMQConsumer is also in charge of triggering the DB write process. 
        # That's why he's getting the db_handler as a parameter. I chose dependency injection in this case.
        db_handler=db_handler 
    )

    rabbitmq_consumer.connect()
    rabbitmq_consumer.start_consuming()

if __name__ == "__main__":
    main()
