# queue_publisher_middleware
### A RabbitMQ message publishing service

This service is a FastAPI middleware that extract specific metadata for every incoming HTTP request 
  it also extracts response data (status code)
  
  # 
 A better practice would be to use it as a 3rd party library, stored at some repository
 I chose to keep it simple for now
  
## Install & run

This service doesn't run as a standalone, for it's only an extension to a FastAPI object
Since it only runs


