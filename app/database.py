import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlmodel import Session
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else{}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def getSession():
    with Session(engine) as session:
        yield session