from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI
from datetime import datetime
import json
from queue_publisher_middleware.queue_handler import rabbit_mq_handler
from queue_publisher_middleware import consts


with open(consts.JSON_ACCOUNTS_FILE_NAME, "r") as file:
    accounts = json.load(file)


class PublisherMiddleware(BaseHTTPMiddleware):
    """
    This class inherits from starlette.BaseHTTPMiddleware,
    which in a way gives us an access to the request & response information
    as well as providing us a middleware mechanism.
    As long as we include this middleware in the FastAPI 'app' object,
    this logic will take place with every incoming HTTP request.
    """

    async def dispatch(self, request: Request, call_next):
        account = dict(request.headers).get("authorization", "NaN")
        response = await call_next(request)

        rabbit_mq_handler.publish(
            message={
                "timestamp": datetime.now().isoformat(),
                "account": "UNAUTHORIZED" if account not in accounts else account,
                "client_ip": request.client.host,
                "endpoint": request.url.path,
                "method": request.method,
                "status_code": int(response.status_code),
            }
        )

        return response
