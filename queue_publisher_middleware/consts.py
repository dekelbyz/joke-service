from os import environ

RABBITMQ_HOST = environ.get("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = environ.get("RABBITMQ_PORT", 5672)
RABBITMQ_USER = environ.get("RABBITMQ_USER", "user")
RABBITMQ_PASSWORD = environ.get("RABBITMQ_PASSWORD", "password")
RABBITMQ_JOKE_METADATA_QUEUE = environ.get(
    "RABBITMQ_JOKE_METADATA_QUEUE", "joke_metadata_queue"
)

JSON_ACCOUNTS_FILE_NAME = "accounts.json"
RABBITMQ_JOKE_METADATA_QUEUE = environ.get(
    "RABBITMQ_JOKE_METADATA_QUEUE", "joke_metadata_queue"
)
