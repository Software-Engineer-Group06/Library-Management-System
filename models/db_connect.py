import mysql.connector
from config import DB_CONFIG # Import từ file config

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        return None