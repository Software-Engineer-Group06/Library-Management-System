from datetime import datetime, timedelta
from models.circulation import get_member_stats, update_return_book

DAILY_FINE_RATE = 5000  # 5,000 VND/ngày

def process_borrowing(member_id, member_type):
    """Xử lý yêu cầu mượn sách"""
    borrowed_count, total_fines = get_member_stats(member_id)
    
    # giới hạn mượn 5 với student và 10 với teacher
    limit = 10 if member_type == 'Teacher' else 5
    
    if borrowed_count >= limit:
        return False, f"Member have borrowed a maximum of {limit} books."
    
    # Không có số tiền phạt nào > 50,000 VND
    if total_fines > 50000:
        return False, f"Unpaid fines ({total_fines} VND) exceed 50,000 VND limit."
    
    # Gợi ý ngày hết hạn (mặc định 14 ngày)
    suggested_due_date = datetime.now() + timedelta(days=14)
    
    return True, suggested_due_date

def process_returning(trans_id, book_id, due_date):
    """Xử lý yêu cầu trả sách và tự động tính tiền phạt"""
    # Lấy thời gian hệ thống hiện tại 
    return_date = datetime.now()
    
    # Chuyển due_date nế đang string sang datetime
    if isinstance(due_date, str):
        due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
        
    # Automated Fine Calculation
    fine_amount = 0
    if return_date > due_date:
        overdue_delta = return_date - due_date
        # Chỉ tính tiền phạt nếu số ngày quá hạn >= 1
        if overdue_delta.days > 0:
            fine_amount = overdue_delta.days * DAILY_FINE_RATE
            
    # Gọi Model cập nhật Database
    success = update_return_book(trans_id, book_id, fine_amount)
    
    if success:
        return True, fine_amount
    
    return False, 0