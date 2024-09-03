import psycopg2
import time

from queue_consumer.models import HttpLog, SessionLocal, Base, engine

# TODO: validate all properties, use env vars

postgres_host = 'postgres'
postgres_user = 'postgres_user'
postgres_password = 'postgres_password'
postgres_db = 'joke_db'

def connect_to_postgres(retries=5, delay=5):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                dbname=postgres_db,
                user=postgres_user,
                password=postgres_password,
                host=postgres_host
            )
            print("Connected to PostgreSQL")
            _initialize_db()
            return conn
        except Exception as e:
            print(f"Failed to connect to PostgreSQL, attempt {i+1} of {retries}: {e}")
            time.sleep(delay)
    print("All attempts to connect to PostgreSQL failed.")
    exit(1)

def _initialize_db():
    print("Creating the database tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

def save_event_details_to_db(event_details):
    db = SessionLocal()
    log_entry = HttpLog(
        timestamp=event_details['timestamp'],
        status_code=event_details['status_code'],
        client_ip=event_details.get('client_ip'),
        method=event_details.get('method'),
        endpoint=event_details.get('endpoint')
    )
    db.add(log_entry)
    db.commit()
    db.close()

    print("Message inserted into PostgreSQL")

