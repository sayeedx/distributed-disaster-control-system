import time
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/ddcs"

def get_engine():
    for i in range(10):
        try:
            engine = create_engine(DATABASE_URL)
            conn = engine.connect()
            conn.close()
            print("✅ Connected to DB")
            return engine
        except Exception as e:
            print(f"DB not ready, retrying... ({i})")
            time.sleep(2)
    raise Exception("❌ Could not connect to DB")

engine = get_engine()