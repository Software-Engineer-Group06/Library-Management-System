import hashlib
from models.db_connect import get_connection

class UserModel:
    def login(self, user_id, password):
        """Kiểm tra đăng nhập: Hash pass nhập vào rồi so sánh với DB"""
        conn = get_connection()
        if not conn:
            print("   -> [MODEL] ❌ Kết nối thất bại!")
            return None
        print("   -> [MODEL] 2. Kết nối OK. Đang tạo Cursor...")
        cursor = conn.cursor(dictionary=True)

        # Hash password nhập vào để so sánh với DB
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        # Query kiểm tra
        cursor.execute("""
            SELECT * FROM User 
            WHERE userID = %s AND password = %s
            """, (user_id, hashed_pw))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return user

    def change_password(self, user_id, new_password):
        conn = get_connection()
        cursor = conn.cursor()
        
        hashed_pw = hashlib.sha256(new_password.encode()).hexdigest()
        
        cursor.execute("""
            UPDATE User 
            SET password = %s 
            WHERE userID = %s
            """, (hashed_pw, user_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        return True