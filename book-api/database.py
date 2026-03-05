from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Loading environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Creating an engine (manages connection to db)
engine = create_engine(DATABASE_URL, echo = True)

# Creating a session (to interact with db)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        


