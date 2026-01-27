from models.db_connect import get_connection
import hashlib
from datetime import datetime

class MemberModel:
    def __init__(self):
        self.db = get_connection()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _generate_new_member_id(self):
        """
        Tự động sinh ID theo format LIB - [Year] - [Sequence]
        Ví dụ: LIB-2026-001
        """
        current_year = datetime.now().year
        prefix = f"LIB-{current_year}-"
        
        cursor = self.db.cursor()
        # Lấy ID lớn nhất hiện tại có prefix tương ứng
        cursor.execute("""
            SELECT memberID 
            FROM MEMBER 
            WHERE memberID LIKE %s 
            ORDER BY memberID 
            DESC LIMIT 1
            """, (f"{prefix}%",))
        result = cursor.fetchone()

        if result:
            last_seq = int(result[0].split('-')[-1])
            new_seq = last_seq + 1
        else:
            new_seq = 1
            
        return f"{prefix}{new_seq:03d}" # Format lại thành chuỗi 3 chữ số (001, 002...)

    def add_member(self, data):
        try:
            self.db.start_transaction()
            cursor = self.db.cursor()

            new_id = self._generate_new_member_id()

            # Tạo Password mặc định từ DOB
            if 'dob' in data and data['dob']:
                default_pass = data['dob'].strftime('%d%m%Y')
            else:
                # Fallback nếu không nhập DOB
                default_pass = "123456" 
            
            hashed_pass = self._hash_password(default_pass)

            # Insert vào bảng USER
            cursor.execute("""
                INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 2)
                """, (
                new_id, new_id, hashed_pass, # username = memberID
                data['fullname'], data['email'], data['phone'], data['dob']
            ))

            # Insert vào bảng MEMBER
            limit = 10 if data['member_type'] == 'Teacher' else 5
            
            cursor.execute("""
                INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID)
                VALUES (%s, %s, %s, %s, %s)
                """, (
                new_id, data['department'], limit, data['member_type'], new_id
            ))

            self.db.commit()
            return new_id # Trả về ID vừa tạo để hiển thị
        except Exception as e:
            print(f"[DB Error] {e}")
            self.db.rollback()
            return None

    def update_member(self, member_id, data):
        try:
            self.db.start_transaction()
            cursor = self.db.cursor()
            cursor.execute("""
                UPDATE USER SET fullName=%s, email=%s, phone=%s, dateOfBirth=%s
                WHERE userID=%s
                """, (
                data['fullname'], data['email'], data['phone'], data['dob'], member_id
            ))

            new_limit = 10 if data['member_type'] == 'Teacher' else 5
            cursor.execute("""
                UPDATE MEMBER SET Department=%s, MemberType=%s, BorrowLimit=%s
                WHERE memberID=%s
                """, (
                data['department'], data['member_type'], new_limit, member_id
            ))

            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def delete_member(self, member_id):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM BORROW_TRANSACTION 
                WHERE memberID=%s AND ReturnDate IS NULL
                """, (member_id,))
            if cursor.fetchone()[0] > 0:
                return False # Có sách chưa trả

            self.db.start_transaction()
            cursor.execute("DELETE FROM MEMBER WHERE memberID=%s", (member_id,))
            cursor.execute("DELETE FROM USER WHERE userID=%s", (member_id,))
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False