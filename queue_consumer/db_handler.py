import logging
from models import JokeMetadata, SessionLocal, Base, engine
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseHandler:
    def __init__(self):
        self._initialize_db()

    def _initialize_db(self):
        logging.info("Creating the database tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        logging.info("Database initialized successfully.")

    def insert_log(self, message):
        try:
            db = SessionLocal()
            log_entry = JokeMetadata(
                timestamp=message['timestamp'],
                status_code=message['status_code'],
                client_ip=message.get('client_ip'),
                method=message.get('method'),
                account=message.get('account'),
                endpoint=message.get('endpoint')
            )
            db.add(log_entry)
            db.commit()
            logging.info("Log entry inserted into PostgreSQL")
        except SQLAlchemyError as e:
            logging.error(f"Failed to insert log into PostgreSQL: {e}")
            db.rollback()
            raise
        finally:
            db.close()
