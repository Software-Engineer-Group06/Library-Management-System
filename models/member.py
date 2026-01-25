import hashlib
from datetime import datetime
from models.db_connect import get_connection

class MemberModel:
    def generate_member_id(self):
        """Sinh ID format: LIB-YYYY-XXX (Ví dụ: LIB-2026-001)"""
        conn = get_connection()
        if not conn: 
            return None
        cursor = conn.cursor()

        current_year = datetime.now().year
        prefix = f"LIB-{current_year}"

        # Lấy ID lớn nhất hiện tại
        cursor.execute("""
            SELECT memberID 
            FROM Member 
            WHERE memberID LIKE %s 
            ORDER BY memberID 
            DESC LIMIT 1
            """, (f"{prefix}-%",))
        result = cursor.fetchone()
        
        if result:
            # Nếu đã có (LIB-2026-005) -> Tách đuôi 005 ra cộng thêm 1
            val = result[0] if isinstance(result, tuple) else result['memberID']
            last_seq = int(val.split('-')[-1])
            new_seq = last_seq + 1
        else:
            new_seq = 1
            
        cursor.close()
        conn.close()
        return f"{prefix}-{new_seq:03d}"

    def add_member(self, full_name, email, phone, department, member_type, dob):
        conn = get_connection()
        if not conn: 
            return False
        try:
            conn.start_transaction() # Bắt đầu transaction an toàn
            cursor = conn.cursor()
            
            full_name = full_name.strip()
            email = email.strip()
            dob_str = dob.strip()
            
            # Sinh Pass mặc định từ ngày sinh (DDMMYYYY)
            # Giả sử dob input là string 'YYYY-MM-DD'
            try: 
                dob_obj = datetime.strptime(dob, "%Y-%m-%d")
                default_pass = dob_obj.strftime("%d%m%Y") 
                hashed_pw = hashlib.sha256(default_pass.encode()).hexdigest()
            except ValueError:
                print(f"❌ Lỗi định dạng ngày tháng: {dob}")
                return None

            # Sinh ID mới
            new_id = self.generate_member_id()

            # Insert bảng User
            cursor.execute("""
                INSERT INTO User (userID, username, password, fullName, email, phone, dateOfBirth, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 2)
                """, (new_id, new_id, hashed_pw, full_name, email, phone, dob))

            # Insert bảng Member
            limit = 10 if member_type == 'Teacher' else 5
            cursor.execute("""
                INSERT INTO Member (memberID, userID, department, memberType, borrowLimit)
                VALUES (%s, %s, %s, %s, %s)
                """, (new_id, new_id, department, member_type, limit))

            conn.commit()
            return new_id
        except Exception as e:
            conn.rollback()
            print(f"Error adding member: {e}")
            return None
        finally:
            cursor.close()
            conn.close()