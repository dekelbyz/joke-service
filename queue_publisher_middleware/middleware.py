from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI
from datetime import datetime
import json
from queue_publisher_middleware.queue_handler import send_to_rabbitmq
from queue_publisher_middleware import consts


file = open(consts.JSON_ACCOUNTS_FILE_NAME)
accounts = json.load(file)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        headers = dict(request.headers)
        response = await call_next(request)

        send_to_rabbitmq(
            message={
            'timestamp': datetime.utcnow().isoformat(),
            'account': 'UNAUTHORIZED' if headers.get('authorization', 'NaN') not in accounts else headers.get('authorization', 'UNAUTHORIZED'),
            'client_ip': request.client.host,
            'endpoint': request.url.path,
            'method': request.method,
            'status_code':  int(response.status_code), 
        },
        queue=consts.RABBITMQ_JOKE_METADATA_QUEUE
        )
        
        return response

