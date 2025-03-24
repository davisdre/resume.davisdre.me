import os
import logging
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import time

app = Flask(__name__, static_folder='../frontend')
CORS(app, resources={r"/*": {"origins": "*"}})

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_db_connection():
    return mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database="visitor_counter"
    )

# Wait for the database to be ready
while True:
    try:
        conn = get_db_connection()
        conn.close()
        break
    except mysql.connector.Error:
        logging.info("Waiting for the database to be ready...")
        time.sleep(5)

# Create the table and initial counter if they don't exist
conn = get_db_connection()
cursor = conn.cursor()
try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        id INT PRIMARY KEY,
        count INT DEFAULT 0
    )
    ''')
    
    cursor.execute('''
    INSERT INTO visitors (id, count) VALUES (1, 0)
    ON DUPLICATE KEY UPDATE id=id
    ''')
    conn.commit()
finally:
    cursor.close()
    conn.close()

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/visitors", methods=["GET"])
def read_root():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Start a transaction
        conn.start_transaction()
        try:
            # Fetch the current count
            cursor.execute("SELECT count FROM visitors WHERE id = 1")
            row = cursor.fetchone()
            if row is None:
                count = 0
                # Initialize the counter if it doesn't exist
                cursor.execute("INSERT INTO visitors (id, count) VALUES (1, 0)")
            else:
                count = row[0]
            logging.info(f"Current count: {count}")

            # Increment the count
            new_count = count + 1
            cursor.execute("UPDATE visitors SET count = %s WHERE id = 1", (new_count,))
            logging.info("Count incremented")

            # Commit the transaction
            conn.commit()
        except Exception as e:
            logging.error(f"Error updating count: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

        return jsonify({"count": new_count})
    except Exception as e:
        cursor.close()
        conn.close()
        raise

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)