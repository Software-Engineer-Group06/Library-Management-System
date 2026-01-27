import mysql.connector
from mysql.connector import Error
import os

def get_connection():
    # Lấy cấu hình từ biến môi trường
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS') 
    db_name = os.getenv('DB_NAME')

    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        
        if connection.is_connected():
            return connection
            
    except Error as e:
        print(f"❌ DB Connection Error: {e}")
        return None