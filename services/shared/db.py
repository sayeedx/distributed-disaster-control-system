import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://disaster_user:disaster_pass@postgres:5432/disaster_db"
)

def get_engine():
    for i in range(10):
        try:
            engine = create_engine(DATABASE_URL)
            conn = engine.connect()
            conn.close()
            print("Connected to DB")
            return engine
        except Exception:
            print(f"DB not ready, retrying... ({i+1}/10)")
            time.sleep(2)
    raise Exception("Could not connect to DB")

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()