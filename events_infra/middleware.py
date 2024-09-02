'''
*** Dataclass EventDetails ***
timestamp: str
account: str | None
ip_address: str
Endpoint: str
Method: Enum
status_code: int

*** Class EventRecorder ***
- extract event details from response object! (response not request because we need the status code)
- Call queue_handler.publish_event

'''