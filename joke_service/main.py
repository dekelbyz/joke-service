import requests
from fastapi import FastAPI
from joke_service.auth import Auth
from joke_service.joke import Joke
from queue_publisher_middleware.middleware import PublisherMiddleware

app = FastAPI()


@app.get("/joke")
async def root():
    response = requests.get("https://api.chucknorris.io/jokes/random").json()
    Joke.from_dict(response)
    return Joke.from_dict(response)


app.add_middleware(Auth)
app.add_middleware(PublisherMiddleware)
