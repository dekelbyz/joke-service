from models import Base, engine

def initialize_db():
    print("Creating the database tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


