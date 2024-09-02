FROM python:3.11-slim

WORKDIR /app/

COPY joke_service/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY accounts.json /app/

COPY joke_service/ /app/joke_service/

EXPOSE 8000

CMD ["uvicorn", "joke_service.main:app"]


