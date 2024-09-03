import psycopg2
import time

from models import HttpLog, SessionLocal, Base, engine

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

class DatabaseHandler:
    def __init__(self):
        self.db = SessionLocal()

    def insert_log(self, message):
        log_entry = HttpLog(
            timestamp=message['timestamp'],
            status_code=message['status_code'],
            client_ip=message.get('client_ip'),
            method=message.get('method'),
            account=message.get('account'),
            endpoint=message.get('endpoint')
        )
        self.db.add(log_entry)
        self.db.commit()
        self.db.close()

