# Queue Consumer 
### A RabbitMQ message consuming service

The queue consumer's purpose is to subscribe to a queue and insert the messages to a DB
For this example I chose to use PostgresQL, but it can easily do the same process with any other DB 

- OOP Designed (for the most part)
- Extandible to work with any type of DBhandler
- Easily configured using environment variables

## Install & run

This service depends on both Postgres and RabbitMQ, so it would probably to run the 
Docker compose in the root directory.
It will orchestrate all the necessary services and will provide the right environment variables
The root README.md file explains exactly how to do so


#### Future steps:

> More Error handling
> Unit/integration testing
> Pydantic implementation 
> Logger configuration improvement

