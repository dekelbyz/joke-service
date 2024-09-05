import logging
from models import JokeMetadata, SessionLocal, Base, engine
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DatabaseHandler:
    def __init__(self):
        self._initialize_db()

    def _initialize_db(self):
        """Creates DB tables if not already exist"""

        logging.info("Creating the database tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        logging.info("Database initialized successfully.")

    def insert_log(self, message):
        """Saves the metadata of every request joke_service receives"""
        try:
            db = SessionLocal()
            log_entry = JokeMetadata(
                timestamp=message.get("timestamp"),
                status_code=message.get("status_code"),
                client_ip=message.get("client_ip"),
                method=message.get("method"),
                account=message.get("account"),
                endpoint=message.get("endpoint"),
                event_id=message.get("event_id"),
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
