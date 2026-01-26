from datetime import datetime, timedelta, date
from models.circulation import CirculationModel


class CirculationController:
    def __init__(self):
        self.model = CirculationModel()
        self.daily_fine_rate = 5000

    def process_borrowing(self, member_id, book_id, manual_due_date=None):
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
        
        # Kiểm tra giới hạn mượn ở student và teacher
        member_type = self.model.get_member_type(member_id)
        if not member_type:
            return False, "Error: Member ID not found."
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
                    due_date = datetime.strptime(manual_due_date, "%d/%m/%Y").date()
                except ValueError:
                    return False, "Invalid date format. Please use DD/MM/YYYY."
            elif isinstance(manual_due_date, datetime):
                due_date = manual_due_date.date()
            elif isinstance(manual_due_date, date):
                due_date = manual_due_date
            else:
                return False, "Invalid manual_due_date type."
        else:
            # Default: 14 ngày kể từ hôm nay
            due_date = datetime.now().date() + timedelta(days=14)
        
        # Tạo Transaction tự động
        trans_id = self.model.create_transID()
        success = self.model.create_issue_transaction(trans_id, member_id, book_id, due_date)
        
        if success:
            formatted_date = due_date.strftime("%d/%m/%Y")
            return True, f"Due date: {formatted_date}."
        else:
            return False, "System Error: Failed to record transaction."

    def process_returning(self, book_id):
        """
        Xử lý yêu cầu trả sách và tự động tính tiền phạt, 
        trả về thành công hoặc thất bại và giá tiền phạt,
        Cấu trúc date trong mysql có dạng chuẩn là: YYYY-MM-DD
        VD: ngày mượn 2026-01-17  --> 2026-01-31
        --> tính phạt sau ngày 31, ép về date = Y-M-D để xử lý không dùng H:M:S
        """
        # Lấy due_date từ db thông qua book_id
        raw_due_date = self.model.get_due_date(book_id)
        
        if not raw_due_date:
            # Trả tuple cố định để view không bị unpack lỗi
            return False, 0, 0, "Error: No active borrow transaction found for this book."
        
        # Ép kiểu về .date() để chỉ so sánh YYYY-MM-DD
        if isinstance(raw_due_date, datetime):
            due_date = raw_due_date.date() 
        else:
            due_date= raw_due_date
        
        
        # Lấy thời gian hệ thống hiện tại 
        return_date = datetime.now().date()
            
        # Automated Fine Calculation
        fine_amount = 0
        overdue_delta = timedelta(0)
        if return_date > due_date:
            overdue_delta = return_date - due_date
            # Chỉ tính tiền phạt nếu số ngày quá hạn >= 1
            if overdue_delta.days > 0:
                fine_amount = overdue_delta.days * self.daily_fine_rate
                
        # cập nhật Database
        success = self.model.update_return_book(book_id, fine_amount)
        
        if success:
            return True, fine_amount, overdue_delta.days, "Book returned successfully."

        return False, fine_amount, overdue_delta.days, "System Error: Failed to update return transaction."
    
    def view_fine_details(self, trans_id):
        """Xử lý logic hiển thị chi tiết tiền phạt"""
        fine = self.model.get_fine_details(trans_id)
        
        if not fine:
            return False, "Fine record not found for this Transaction ID."
        
        # Giải nén dữ liệu từ tuple (transID, amount, isPaid, lateDays)
        t_id, amount, is_paid, late_days = fine
        
        status = "Paid" if is_paid else "Unpaid"
        
        # Trả về kết quả đã format
        details = (
            f"Transaction ID: {t_id}\n"
            f"Late days: {late_days}\n"
            f"Fine amount: {amount:,.0f} VND\n"
            f"Payment status: {status}"
        )
        return True, details

    def pay_fine(self, trans_id):
        """Xử lý logic thanh toán tiền phạt"""
        success = self.model.update_fine_payment(trans_id)
        if success:
            return True, "Fine paid successfully."
        return False, "Failed to update payment status."