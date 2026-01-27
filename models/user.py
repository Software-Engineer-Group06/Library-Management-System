import hashlib
from models.db_connect import get_connection

class UserModel:
    def __init__(self):
        self.db = get_connection()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_login(self, username, password):
        """
        Kiểm tra đăng nhập dựa trên Username và Password.
        Logic khớp với Interface yêu cầu nhập Username.
        """
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM USER WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user:
            input_hash = self._hash_password(password)
            if input_hash == user['password']:
                return user
        return None

    def check_first_login(self, user):
        """
        Logic: Nếu password hiện tại trùng với hash của DOB (DDMMYYYY) 
        thì coi là lần đăng nhập đầu.
        """
        dob_str = user['dateOfBirth'].strftime('%d%m%Y')
        current_pass_hash = user['password']
        dob_hash = self._hash_password(dob_str)
        return current_pass_hash == dob_hash
    
    def add_member(self, data):
        """Register Member"""
        try:
            cursor = self.db.cursor()
            # Insert vào bảng USER
            query_user = """
                INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Mặc định password là ngày sinh (DDMMYYYY)
            default_pass = data['dob'].strftime('%d%m%Y')
            hashed_pass = self._hash_password(default_pass)
            
            cursor.execute(query_user, (
                data['user_id'], data['username'], hashed_pass, 
                data['fullname'], data['email'], data['phone'], 
                data['dob'], 2 # Role 2 = Member
            ))
            
            # Insert vào bảng MEMBER
            query_member = """
                INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID)
                VALUES (%s, %s, %s, %s, %s)
            """
            # Giả sử MemberType quyết định BorrowLimit (Student=5, Teacher=10)
            limit = 10 if data['member_type'] == 'Teacher' else 5
            
            cursor.execute(query_member, (
                data['user_id'], data['department'], limit, 
                data['member_type'], data['user_id']
            ))
            
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def update_member(self, member_id, data):
        """
        Cập nhật thông tin Member 
        """
        try:
            self.db.start_transaction() # Dùng transaction để đảm bảo tính toàn vẹn
            cursor = self.db.cursor()

            # Cập nhật bảng USER (Thông tin cá nhân)
            query_user = """
                UPDATE USER 
                SET fullName = %s, email = %s, phone = %s, dateOfBirth = %s
                WHERE userID = %s
            """
            cursor.execute(query_user, (
                data['fullname'], data['email'], data['phone'], 
                data['dob'], member_id
            ))

            # Cập nhật bảng MEMBER (Thông tin nghiệp vụ)
            # Tính lại BorrowLimit nếu đổi MemberType
            new_limit = 10 if data['member_type'] == 'Teacher' else 5
            
            query_member = """
                UPDATE MEMBER 
                SET Department = %s, MemberType = %s, BorrowLimit = %s
                WHERE memberID = %s
            """
            cursor.execute(query_member, (
                data['department'], data['member_type'], new_limit, member_id
            ))

            self.db.commit()
            return True
        except Exception as e:
            print(f"[Error] Update failed: {e}")
            self.db.rollback()
            return False
            
    def get_member_details(self, member_id):
        """Lấy thông tin chi tiết để hiển thị trước khi edit"""
        cursor = self.db.cursor(dictionary=True)
        # Join 2 bảng để lấy full thông tin
        query = """
            SELECT U.*, M.Department, M.MemberType 
            FROM USER U JOIN MEMBER M ON U.userID = M.memberID 
            WHERE U.userID = %s
        """
        cursor.execute(query, (member_id,))
        return cursor.fetchone()

    def delete_member(self, member_id):
        """Delete Member"""
        try:
            cursor = self.db.cursor()
            # Kiểm tra active borrowing
            check_query = "SELECT COUNT(*) FROM BORROW_TRANSACTION WHERE memberID = %s AND ReturnDate IS NULL"
            cursor.execute(check_query, (member_id,))
            if cursor.fetchone()[0] > 0:
                return False # Có sách chưa trả -> Không cho xóa
            
            # Xóa MEMBER trước (Foreign Key)
            cursor.execute("DELETE FROM MEMBER WHERE memberID = %s", (member_id,))
            # Xóa USER sau
            cursor.execute("DELETE FROM USER WHERE userID = %s", (member_id,))
            self.db.commit()
            return True
        except Exception:
            return False
    def change_password(self, user_id, new_password):
        try:
            new_hash = self._hash_password(new_password)
            cursor = self.db.cursor()
            query = "UPDATE USER SET password = %s WHERE userID = %s"
            cursor.execute(query, (new_hash, user_id))
            self.db.commit()
            return True
        except Exception:
            return False