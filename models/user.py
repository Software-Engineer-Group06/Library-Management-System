import hashlib
from models.db_connect import get_connection

class UserModel:
    def __init__(self):
        self.db = get_connection()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_login(self, username, password):
        """Kiểm tra đăng nhập dựa trên Username và Password"""
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USER WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            input_hash = self._hash_password(password)
            if input_hash == user['password']:
                return user
        return None

    def check_first_login(self, user):
        """Logic: Nếu password hiện tại trùng với hash của DOB (DDMMYYYY) thì coi là lần đăng nhập đầu"""
        dob_str = user['dateOfBirth'].strftime('%d%m%Y')
        current_pass_hash = user['password']
        dob_hash = self._hash_password(dob_str)
        return current_pass_hash == dob_hash
            
    def change_password(self, user_id, new_password):
        try:
            new_hash = self._hash_password(new_password)
            cursor = self.db.cursor()
            cursor.execute("UPDATE USER SET password = %s WHERE userID = %s", (new_hash, user_id))
            self.db.commit()
            return True
        except Exception:
            return False