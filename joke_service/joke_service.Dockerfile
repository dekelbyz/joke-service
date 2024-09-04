FROM python:3.11-slim

WORKDIR /app/

COPY joke_service/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY accounts.json /app/

COPY queue_publisher_middleware/ /app/queue_publisher_middleware/ 
# this is an alternative to an actual shared library hosted in some repository (e.g. PYPI) 

COPY joke_service/ /app/joke_service/

EXPOSE 8000


CMD ["uvicorn", "joke_service.main:app", "--host", "0.0.0.0", "--port", "8000"]


