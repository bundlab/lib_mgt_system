# db_connection.py

import psycopg2
from psycopg2 import OperationalError

def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",          # Change if your DB is elsewhere
            database="library_db",     # Your database name
            user="postgres",      # Your PostgreSQL username
            password="Mypg@25",  # Your password
            port="5432"
        )
        return conn
    except OperationalError as e:
        print(f"Connection error: {e}")
        raise