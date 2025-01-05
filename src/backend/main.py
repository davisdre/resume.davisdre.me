from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa
from sqlalchemy.sql import text
import logging
import os

app = FastAPI()

# Configuring CORS
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_USER = os.getenv("DATABASE_USER", "app_user")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "app_password")
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@db/visitor_counter"

engine = sa.create_engine(DATABASE_URL)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.get("/visitors")
async def read_root():
    with engine.connect() as connection:
        # Start a transaction
        with connection.begin() as transaction:
            try:
                # Fetch the current count
                result = connection.execute(text("SELECT count FROM visitors WHERE id = 1"))
                count = result.fetchone()[0]
                logging.info(f"Current count: {count}")

                # Increment the count
                connection.execute(text("UPDATE visitors SET count = count + 1 WHERE id = 1"))
                logging.info("Count incremented")

                # Commit the transaction
                transaction.commit()
            except Exception as e:
                logging.error(f"Error updating count: {e}")
                transaction.rollback()
                raise

        return {"count": count + 1}