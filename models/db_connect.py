import mysql.connector
from mysql.connector import Error
import os

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def get_connection(self):
        # Nếu chưa có kết nối hoặc kết nối bị đứt thì kết nối lại
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST', 'localhost'), # Hoặc 'db' nếu chạy Docker
                    user=os.getenv('DB_USER', 'root'),      # Default user
                    password=os.getenv('DB_PASS', ''),  # Default pass
                    database=os.getenv('DB_NAME', 'LibraryDB')
                )
                print(">> [INFO] Connected to Database.")
            except Error as e:
                print(f">> [CRITICAL] Database connection failed: {e}")
                # Raise Exception để App dừng ngay lập tức, không chạy tiếp với None
                raise e 
        
        return self.connection

# Hàm wrapper để các Model gọi cho gọn
def get_connection():
    return Database().get_connection()