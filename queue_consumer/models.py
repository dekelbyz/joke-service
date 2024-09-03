from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# todo: create consts.py to store env vars & default values
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class HttpLog(Base):
    __tablename__ = 'http_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    status_code = Column(Integer, nullable=False)
    client_ip = Column(String(45), nullable=True)
    method = Column(String(10), nullable=True)
    endpoint = Column(Text, nullable=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
