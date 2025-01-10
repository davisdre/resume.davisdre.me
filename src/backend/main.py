import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa
from sqlalchemy.sql import text
import time

app = FastAPI()

# Configuring CORS
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@db/visitor_counter"

engine = sa.create_engine(DATABASE_URL)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Wait for the database to be ready
while True:
    try:
        with engine.connect() as connection:
            break
    except sa.exc.OperationalError:
        logging.info("Waiting for the database to be ready...")
        time.sleep(5)

# Create the table and initial counter if they don't exist
with engine.connect() as connection:
    connection.execute(text('''
    CREATE TABLE IF NOT EXISTS visitors (
        id INT PRIMARY KEY,
        count INT DEFAULT 0
    )
    '''))
    connection.execute(text('''
    INSERT INTO visitors (id, count) VALUES (1, 0)
    ON DUPLICATE KEY UPDATE id=id
    '''))

@app.get("/visitors")
async def read_root():
    with engine.connect() as connection:
        # Start a transaction
        with connection.begin() as transaction:
            try:
                # Fetch the current count
                result = connection.execute(text("SELECT count FROM visitors WHERE id = 1"))
                row = result.fetchone()
                if row is None:
                    count = 0
                    # Initialize the counter if it doesn't exist
                    connection.execute(text("INSERT INTO visitors (id, count) VALUES (1, 0)"))
                else:
                    count = row[0]
                logging.info(f"Current count: {count}")

                # Increment the count
                new_count = count + 1
                connection.execute(text("UPDATE visitors SET count = :new_count WHERE id = 1"), {"new_count": new_count})
                logging.info("Count incremented")

                # Commit the transaction
                transaction.commit()
            except Exception as e:
                logging.error(f"Error updating count: {e}")
                transaction.rollback()
                raise

        return {"count": new_count}