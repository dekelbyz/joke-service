FROM python:3.11-slim

WORKDIR /app/

COPY queue_consumer/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY accounts.json /app/

COPY queue_consumer/ /app/queue_consumer/

CMD ["sh", "-c", "python queue_consumer/main.py"]



