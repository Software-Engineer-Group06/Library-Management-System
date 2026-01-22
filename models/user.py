import hashlib
from models.db_connect import get_connection

class UserModel:
    def login(self, user_id, password):
        conn = get_connection()
        if not conn: return None
        cursor = conn.cursor(dictionary=True)

        # 1. Hash password nhập vào để so sánh với DB
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        # 2. Query kiểm tra
        sql = "SELECT * FROM User WHERE userID = %s AND password = %s"
        cursor.execute(sql, (user_id, hashed_pw))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return user

    def change_password(self, user_id, new_password):
        conn = get_connection()
        cursor = conn.cursor()
        
        hashed_pw = hashlib.sha256(new_password.encode()).hexdigest()
        
        sql = "UPDATE User SET password = %s WHERE userID = %s"
        cursor.execute(sql, (hashed_pw, user_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        return True