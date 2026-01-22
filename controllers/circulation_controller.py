from datetime import datetime, timedelta, date
from models.circulation import CirculationModel


class CirculationController:
    def __init__(self):
        self.model = CirculationModel()
        self.daily_fine_rate = 5000

    def process_borrowing(self, member_id, book_id, member_type, manual_due_date=None):
        """
        Xử lý yêu cầu mượn sách
        manual_due_date: Ngày do Librarian chọn thủ công (nếu có không thì mặc định sau 14 ngày)
        """
        # Kiểm tra tình trạng sách có đang Available không
        status = self.model.check_book_status(book_id)
        
        if status is None:
            return False, "Book ID not found in inventory"
        
        if status != "Available":
            return False, f"Book is currently {status}. Cannot issue."
        
        member_stats = self.model.get_member_stats(member_id)
        if member_stats == (None, None):
            return False, "System Error: Could not retrieve member stats."
        borrowed_count, total_fines = member_stats
        
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
                    due_date = datetime.strptime(manual_due_date, "%Y-%m-%d").date()
                except ValueError:
                    return False, "Invalid date format. Please use YYYY-MM-DD."
            elif isinstance(manual_due_date, datetime):
                due_date = manual_due_date.date()
            elif isinstance(manual_due_date, date):
                due_date = manual_due_date
            else:
                return False, "Invalid manual_due_date type."
        else:
            # Default: 14 ngày kể từ hôm nay
            due_date = datetime.now().date() + timedelta(days=14)
        
        # Tạo Transaction theo định dạng ISS-datetime thêm microseconds để tránh trùng lặp
        trans_id = f"ISS-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        success = self.model.create_issue_transaction(trans_id, member_id, book_id, due_date)
        
        if success:
            return True, f"Success: Book issued successfully. Due date: {due_date}."
        else:
            return False, "System Error: Failed to record transaction."

    def process_returning(self, book_id, due_date):
        """
        Xử lý yêu cầu trả sách và tự động tính tiền phạt, 
        trả về thành công hoặc thất bại và giá tiền phạt,
        Cấu trúc date trong mysql có dạng chuẩn là: YYYY-MM-DD
        VD: ngày mượn 2026-01-17  --> 2026-01-31
        --> tính phạt sau ngày 31, ép về date = Y-M-D để xử lý không dùng H:M:S
        """
        # Lấy thời gian hệ thống hiện tại 
        return_date = datetime.now().date()
        
        # Chuyển due_date nếu đang string sang datetime
        if isinstance(due_date, str):
            try:
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            except ValueError:
                return False, "Invalid date format. Please use YYYY-MM-DD."
        elif isinstance(due_date, datetime):
            due_date = due_date.date()
        elif isinstance(due_date, date):
            pass
        else:
            return False, "Invalid due_date type."
            
        # Automated Fine Calculation
        fine_amount = 0
        if return_date > due_date:
            overdue_delta = return_date - due_date
            # Chỉ tính tiền phạt nếu số ngày quá hạn >= 1
            if overdue_delta.days > 0:
                fine_amount = overdue_delta.days * self.daily_fine_rate
                
        # cập nhật Database
        success = self.model.update_return_book(book_id, fine_amount)
        
        if success:
            return True, fine_amount
        
        return False, fine_amount