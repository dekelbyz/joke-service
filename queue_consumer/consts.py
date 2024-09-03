from os import environ

POSTGRES_HOST = environ.get('POSTGRES_HOST', 'postgres')
POSTGRES_USER = environ.get('POSTGRES_USER', 'postgres_user')
POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD', 'postgres_password')
POSTGRES_DB = environ.get('POSTGRES_DB', 'joke_db')

RABBITMQ_HOST = environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = environ.get('RABBITMQ_PORT', 5672)
RABBITMQ_USER = environ.get('RABBITMQ_USER', 'user')
RABBITMQ_PASSWORD = environ.get('RABBITMQ_PASSWORD', 'password')
RABBITMQ_JOKE_METADATA_QUEUE = environ.get('RABBITMQ_JOKE_METADATA_QUEUE', 'joke_metadata_queue')


