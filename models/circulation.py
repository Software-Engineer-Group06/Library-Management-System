from models.db_connect import get_connection

def get_member_stats(member_id):
    """Truy vấn DB để lấy số lượng sách chưa trả và tổng tiền phạt chưa thanh toán"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Đếm số giao dịch chưa trả (returnDate IS NULL)
    cursor.execute("""
        SELECT COUNT(*) FROM BorrowTransaction 
        WHERE memberID = %s AND returnDate IS NULL
    """, (member_id,))
    borrowed_count = cursor.fetchone()[0]
    
    # Tính tổng tiền phạt chưa thanh toán (isPaid = False) từ bảng Fine
    cursor.execute("""
        SELECT SUM(f.amount) 
        FROM Fine f
        JOIN BorrowTransaction br ON f.transID = br.transID
        WHERE br.memberID = %s AND f.isPaid = False
    """, (member_id,))
    total_fines = cursor.fetchone()[0] or 0
    
    cursor.close()
    conn.close()
    return borrowed_count, total_fines

def check_book_status(book_id):
    """Kiểm tra tình trạng sách hiện tại"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM Book WHERE bookID = %s", (book_id,))
    result = cursor.fetchone()
    
    if result:
        cursor.close()
        conn.close()
        return result[0]
    
    cursor.close()
    conn.close()
    return None # Không tìm thấy


def create_issue_transaction(trans_id, member_id, book_id, due_date):
    """Tạo giao dịch mượn mới và cập nhật trạng thái sách thành 'Borrowed'"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Thêm bản ghi vào bảng BorrowTransaction
    cursor.execute("""
            INSERT INTO BorrowTransaction (transID, memberID, bookID, dueDate)
            VALUES (%s, %s, %s, %s)
        """, (trans_id, member_id, book_id, due_date))
    
    # Cập nhật trạng thái sách trong bảng Book
    cursor.execute("""
        UPDATE Book 
        SET status = 'Issued' 
        WHERE bookID = %s
    """, (book_id,))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    return True
    

def update_return_book(book_id, fine_amount):
    """Cập nhật ngày trả, trạng thái sách và tạo phiếu phạt nếu có"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tìm giao dịch theo book_id
    cursor.execute("""
        SELECT transID FROM BorrowTransaction
        WHERE bookID = %s AND returnDate IS NULL
    """, (book_id,))
    
    result = cursor.fetchone()
    
    if result is None:
        print("This Borrow transaction could not be found.")
        return False
    
    trans_id = result[0] # Lấy giá trị transID từ tuple kết quả
    
    # Cập nhật ngày trả sách trong BorrowTransaction
    cursor.execute("""
        UPDATE BorrowTransaction SET returnDate = NOW() WHERE transID = %s
    """, (trans_id,))
    
    # Cập nhật trạng thái sách về "Available"
    cursor.execute("UPDATE Book SET status = 'Available' WHERE bookID = %s", (book_id,))
    
    # Nếu có tiền phạt, thêm record vào bảng Fine
    if fine_amount > 0:
        fine_id = f"FIN-{trans_id}"    # Tạo mã phạt theo định dạng FIN-{trans_id}
        cursor.execute("""
            INSERT INTO Fine (fineID, transID, amount, isPaid) 
            VALUES (%s, %s, %s, %s)
        """, (fine_id, trans_id, fine_amount, False))
        
    conn.commit()
    print(f"Trả sách thành công! Mã giao dịch {trans_id}")
    
    cursor.close()
    conn.close()
    return True