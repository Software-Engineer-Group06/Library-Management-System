from datetime import datetime, timedelta
from models.circulation import get_member_stats, update_return_book, create_issue_transaction, check_book_status

DAILY_FINE_RATE = 5000  # 5,000 VND/ngày

def process_borrowing(member_id, book_id, member_type, manual_due_date=None):
    """
    Xử lý yêu cầu mượn sách
    manual_due_date: Ngày do Librarian chọn thủ công (nếu có không thì mặc định sau 14 ngày)
    """
    # Kiểm tra tình trạng sách có đang Available không
    status = check_book_status(book_id)
    
    if status is None:
        return False, "Book ID not found in inventory"
    
    if status != "Available":
        return False, f"Book is currently {status}. Cannot issue."
    
    borrowed_count, total_fines = get_member_stats(member_id)
    
    # giới hạn mượn 5 với student và 10 với teacher
    limit = 10 if member_type == 'Teacher' else 5
    
    if borrowed_count >= limit:
        return False, f"Member have borrowed a maximum of {limit} books."
    
    # Không có số tiền phạt nào > 50,000 VND
    if total_fines > 50000:
        return False, f"Unpaid fines ({total_fines} VND) exceed 50,000 VND limit."
    
    # Xác định ngày đến hạn (Default or Manual)
    if manual_due_date:
        if isinstance(manual_due_date, str):
            try:
                # Ép kiểu từ string sang datetime (YYYY-MM-DD)
                due_date = datetime.strptime(manual_due_date, '%Y-%m-%d')
            except ValueError:
                return False, "Invalid date format. Please use YYYY-MM-DD."
        else:
            due_date = manual_due_date
    else:
        # Default: 14 ngày kể từ hôm nay
        due_date = datetime.now() + timedelta(days=14)
    
    # Tạo Transaction theo định dạng ISS-datetime thêm time để tránh trùng lặp
    trans_id = f"ISS-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    success = create_issue_transaction(trans_id, member_id, book_id, due_date)
    
    return success, "Success" if success else "DB Error"

def process_returning(book_id, due_date):
    """
    Xử lý yêu cầu trả sách và tự động tính tiền phạt, 
    trả về thành công hoặc thất bại và giá tiền phạt,
    Cấu trúc datetime trong mysql có dạng chuẩn là: YYYY-MM-DD HH:MM:SS
    VD: ngày mượn 2026-01-17 00:00:00  --> 2026-01-31 00:00:00
    --> tính phạt sau ngày 31, ép về date = Y-M-D để xử lý không dùng H:M:S
    """
    # Lấy thời gian hệ thống hiện tại 
    return_date = datetime.now().date()
    
    # Chuyển due_date nếu đang string sang datetime
    if isinstance(due_date, str):
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid date format. Please use YYYY-MM-DD."
        
    # Automated Fine Calculation
    fine_amount = 0
    if return_date > due_date:
        overdue_delta = return_date - due_date
        # Chỉ tính tiền phạt nếu số ngày quá hạn >= 1
        if overdue_delta.days > 0:
            fine_amount = overdue_delta.days * DAILY_FINE_RATE
            
    # Gọi Model cập nhật Database
    success = update_return_book(book_id, fine_amount)
    
    if success:
        return True, fine_amount
    
    return False, 0