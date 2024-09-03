from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI
from datetime import datetime
import json
from events_infra.queue_handler import send_to_rabbitmq


file = open('accounts.json')
accounts = json.load(file)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        headers = dict(request.headers)
        response = await call_next(request)

        send_to_rabbitmq({
            'timestamp': datetime.utcnow().isoformat(),
            'account': 'UNAUTHORIZED' if headers.get('authorization', 'wtf') not in accounts else headers.get('authorization', 'UNAUTHORIZED'),
            'client_ip': request.client.host,
            'endpoint': request.url.path,
            'method': request.method,
            'status_code':  int(response.status_code),
            
        })
        
        return response

