from enum import Enum
from dataclasses import dataclass
from datetime import date


class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


# TODO: align names
@dataclass
class EventDetails:
    timetsamp: date
    account: str
    ip_address: str
    endpoint: str
    method: HTTPMethod
    status_code: int

