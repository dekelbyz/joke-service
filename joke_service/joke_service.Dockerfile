FROM python:3.11-slim

WORKDIR /joke_service

COPY joke_service/requirements.txt /joke_service/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /joke_service/

EXPOSE 8000

CMD ["uvicorn", "joke_service.main:app"]


