from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import consts
import os


DATABASE_URL = f"postgresql://{consts.POSTGRES_USER}:{consts.POSTGRES_PASSWORD}@{consts.POSTGRES_HOST}/{consts.POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class JokeMetadata(Base):
    __tablename__ = 'joke_metadata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    account = Column(String(60), nullable=False)
    client_ip = Column(String(45), nullable=False)
    endpoint = Column(String(100), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
