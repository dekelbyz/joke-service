from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI
from datetime import datetime
import json
from queue_publisher_middleware.queue_handler import send_to_rabbitmq
from queue_publisher_middleware import consts


file = open(consts.JSON_ACCOUNTS_FILE_NAME)
accounts = json.load(file)

class PublisherMiddleware(BaseHTTPMiddleware):
    '''
    PublisherMiddleware is a middleware class 
    In charge of extracting specific metadata for every incoming request
    And trigger the send_to_rabbitmq function

    - We use starlette for the middleware behavior by inheriting from its BaseHTTPMiddleware class
    - We trigger the send_to_rabbitmq function that writes the data to rabbitMQ
    '''

    async def dispatch(self, request: Request, call_next):
        account = dict(request.headers).get('authorization', 'NaN')
        response = await call_next(request)

        send_to_rabbitmq(
            message={
            'timestamp': datetime.utcnow().isoformat(),
            'account': 'UNAUTHORIZED' if account not in accounts else account,
            'client_ip': request.client.host,
            'endpoint': request.url.path,
            'method': request.method,
            'status_code':  int(response.status_code), 
        },
        queue=consts.RABBITMQ_JOKE_METADATA_QUEUE
        )
        
        return response

