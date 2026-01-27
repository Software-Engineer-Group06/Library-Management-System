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
        query = "SELECT memberID FROM MEMBER WHERE memberID LIKE %s ORDER BY memberID DESC LIMIT 1"
        cursor.execute(query, (f"{prefix}%",))
        result = cursor.fetchone()

        if result:
            # Nếu đã có, lấy số đuôi + 1
            # format: LIB-2026-001 -> cắt lấy 001
            last_seq = int(result[0].split('-')[-1])
            new_seq = last_seq + 1
        else:
            # Nếu chưa có, bắt đầu từ 001
            new_seq = 1
            
        # Format lại thành chuỗi 3 chữ số (001, 002...)
        return f"{prefix}{new_seq:03d}"

    def add_member(self, data):
        try:
            self.db.start_transaction()
            cursor = self.db.cursor()

            # Tự sinh Member ID
            new_id = self._generate_new_member_id()

            # Tạo Password mặc định từ DOB
            if 'dob' in data and data['dob']:
                default_pass = data['dob'].strftime('%d%m%Y')
            else:
                # Fallback nếu không nhập DOB (dù UI nên bắt buộc)
                default_pass = "123456" 
            
            hashed_pass = self._hash_password(default_pass)

            # Insert vào bảng USER
            query_user = """
                INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 2)
            """
            cursor.execute(query_user, (
                new_id, new_id, hashed_pass, # username = memberID
                data['fullname'], data['email'], data['phone'], data['dob']
            ))

            # Insert vào bảng MEMBER
            limit = 10 if data['member_type'] == 'Teacher' else 5
            
            query_member = """
                INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_member, (
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

            query_user = """
                UPDATE USER SET fullName=%s, email=%s, phone=%s, dateOfBirth=%s
                WHERE userID=%s
            """
            cursor.execute(query_user, (
                data['fullname'], data['email'], data['phone'], data['dob'], member_id
            ))

            new_limit = 10 if data['member_type'] == 'Teacher' else 5
            query_member = """
                UPDATE MEMBER SET Department=%s, MemberType=%s, BorrowLimit=%s
                WHERE memberID=%s
            """
            cursor.execute(query_member, (
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
            cursor.execute("SELECT COUNT(*) FROM BORROW_TRANSACTION WHERE memberID=%s AND ReturnDate IS NULL", (member_id,))
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

    def get_member_details(self, member_id):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT U.*, M.Department, M.MemberType, M.BorrowLimit
            FROM USER U JOIN MEMBER M ON U.userID = M.memberID 
            WHERE U.userID = %s
        """
        cursor.execute(query, (member_id,))
        return cursor.fetchone()