# Chuck Norris Jokes Application
> Who doesn't need a good laugh nowadays?


## introduction
Welcome to Chuck Norris Jokes Application!
This is a server application, REST based, that provides random Chuck Norris Jokes! 

## How it works?
**You send us an HTTP request and get a Chuck Norris joke in return!**

- We document every incoming HTTP request
- We use starlette for middleware configuration
- The request details are being written to RabbitMQ, which serves as our event broker
- Meanwhile, we have a consumer that listens to the same queue and inserts the messages to PostgresQL

## Components Breakdown

#### joke_service
This service is a RestAPI that fetches Chuck Norris jokes on demand
This service is also in charge of the authentication, so:

**PLEASE NOTE THAT YOU HAVE TO BE A REGISTERED USER IN ORDER TO USE THIS SERVICE**


### Endpoints
**GET /joke**</br>
Get Chuck Norris joke 

**Headers**
|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `Authorization` | required | string  | Your account authorization.                                                                     |


** Example **

```bash
curl --location --request GET 'http://localhost:8000/joke' \
--header 'Authorization: 1111-2222-3333'
```

**Response**
```
{
    "id": "F6v0fEXeREek9FnF6_9k4A",
    "categories": ["some category"],
    "createdAt": "2020-01-05 13:42:25.352697",
    "joke": "Chuck Norris' first car was Optimus Prime."
}
```
---
#### queue_publisher_middleware
The **queue_publisher_middleware** package is the component that records the incoming events and publishes to our [RabbitMQ](https://www.rabbitmq.com/ "RabbitMQ")

**How?**
It has a **middleware** ([starlette](https://www.starlette.io/ "starlette") based) to do that. As soon as a request coming in, the middleware will be alerted and have access to all its data.
Once it retrieves the data it needs from both request and response (we document the status code as well), it records this event to RabbitMQ, which is integrated using [pika](https://pika.readthedocs.io/ "pika") library

#### queue_consumer
The queue_consumer microservice is designed to serve as a **listener**.
It connets to **RabbitMQ** and keeps track of incoming events to a certain **queue**.
When a new event comes in, the queue consumer receives it and** posts it to PostgresQL**

---

# How to run it?
We have prepared a **docker-compose** for convenient
It's a great tool for locally orchestrating several services and applications that have dependencies between them.

**Run this command (from the root dir):**
```sh
docker compose up --build -d
```
*it will build all the docker images, inject environment variables, assign volumes and deploy our services by a predefined order and conditions*

# UI
The docker image we chose for RabbitMQ also provides a nice UI, simply by navigating to this URL:

```
http://localhost:15672/
```

