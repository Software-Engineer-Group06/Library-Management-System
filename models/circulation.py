from datetime import datetime, timedelta
from models.db_connect import get_connection

def get_member_stats(member_id):
    """Truy vấn DB để lấy số lượng sách chưa trả và tổng tiền phạt chưa thanh toán"""
    conn = get_connection()
    if not conn: 
        return False
    
    cursor = conn.cursor()
    try:
        return 0
    
    except Exception as e:
        conn.rollback()
        print(f"Lỗi khi cập nhật trả sách: {e}")
        return False
    
    finally:
        cursor.close()
        conn.close()

def update_return_book(fine_id, fine_amount):
    """Cập nhật ngày trả, trạng thái sách và tạo phiếu phạt nếu có"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        now = datetime.now()
        
        return 0
    
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return False
    
    finally:
        conn.close()

