from enum import Enum
from dataclasses import dataclass
from datetime import date

"""
Those below are nothing but a type hinter
It's not strict and will not intervene in runtime/interpretation process
"""


class HTTPMethod(Enum):
    """
    HTTPMethod represents an enumeration of possible values for this parameter
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"


@dataclass
class EventDetails:
    timetsamp: date
    account: str
    client_ip: str
    endpoint: str
    method: HTTPMethod
    status_code: int
