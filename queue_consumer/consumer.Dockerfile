FROM python:3.11-slim

WORKDIR /app/

COPY queue_consumer/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY accounts.json /app/

COPY queue_consumer/ /app/queue_consumer/

EXPOSE 8000

# TODO: use env vars / build args
CMD ["sh", "-c", "python queue_consumer/init_db.py && python queue_consumer/consumer.py"]



