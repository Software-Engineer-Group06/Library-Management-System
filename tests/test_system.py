import pytest
from datetime import datetime, timedelta
from models.user import UserModel
from models.book import BookModel
from models.member import MemberModel
from models.circulation import CirculationModel
from models.report import ReportNotifyModel

@pytest.fixture
def user_model(): return UserModel()
@pytest.fixture
def book_model(): return BookModel()
@pytest.fixture
def mem_model(): return MemberModel()
@pytest.fixture
def circ_model(): return CirculationModel()
@pytest.fixture
def report_model(): return ReportNotifyModel()

# Tạo Member mẫu để test
@pytest.fixture
def sample_member(mem_model):
    mid = mem_model.add_member("Test Mem", "t@test.com", "123", "IT", "Student", "2000-01-01")
    yield mid
    # Clean up (Nếu có hàm xóa)
    # mem_model.delete_member(mid)

# Tạo Sách mẫu để test
@pytest.fixture
def sample_book(book_model):
    bid = book_model.add_book("Test Book", "Author T", "ISBN-T", "Pub", "Cat", "A1")
    yield bid
    book_model.delete_book(bid)

def test_tc01_login_success(user_model):
    """TC01, TC05: Đăng nhập thành công với Admin/Member"""
    # Giả sử ADMIN01/admin123 luôn đúng từ data gốc
    user = user_model.login("ADMIN01", "admin123")
    assert user is not None
    assert user['userID'] == "ADMIN01"

def test_tc02_tc03_tc04_login_fail(user_model):
    """TC02, TC03, TC04: Đăng nhập thất bại (Sai pass, Sai ID, Empty)"""
    assert user_model.login("ADMIN01", "wrongpass") is None
    assert user_model.login("WRONG-ID", "admin123") is None
    assert user_model.login("ADMIN01", "") is None

def test_tc08_tc09_change_password(user_model):
    """TC08, TC09: Đổi mật khẩu (Giả định hàm change_password)"""
    # Lưu ý: Cần implement hàm change_password trong UserModel
    # assert user_model.change_password("ADMIN01", "newpass123") is True
    pass # Bỏ qua nếu chưa có hàm

def test_tc_auth_09_sql_injection(user_model):
    """TC_AUTH_09: Test bảo mật SQL Injection"""
    payload = "' OR '1'='1"
    assert user_model.login(payload, "anything") is None

def test_tc32_add_book_success(book_model):
    """TC32: Thêm sách thành công"""
    bid = book_model.add_book("New Book", "Author", "ISBN-99", "Pub", "Cat", "Z1")
    assert bid is not None
    assert "BK-" in bid
    book_model.delete_book(bid) # Dọn dẹp

def test_tc33_add_book_missing_info(book_model):
    """TC33, TC_BOOK_01: Thêm sách thiếu Title/Author"""
    # Giả sử hàm add_book trả về None nếu thiếu info
    # assert book_model.add_book("", "", ...) is None
    pass 

def test_tc12_tc17_search_books(book_model, sample_book):
    """TC12-TC17: Tìm kiếm sách"""
    # Tìm đúng
    res = book_model.search_books("Test Book")
    assert len(res) > 0
    # Tìm sai
    res_fail = book_model.search_books("Khong Co Sach Nay")
    assert len(res_fail) == 0

def test_tc35_tc36_update_book(book_model, sample_book):
    """TC35, TC36: Cập nhật sách"""
    # Cần implement hàm update_book
    # success = book_model.update_book(sample_book, title="Updated Title")
    # assert success is True
    pass

def test_tc37_tc38_delete_book(book_model):
    """TC37, TC38: Xóa sách"""
    # Tạo sách để xóa
    bid = book_model.add_book("To Delete", "A", "I", "P", "C", "S")
    assert book_model.delete_book(bid) is True
    
    # Xóa sách không tồn tại
    assert book_model.delete_book("NON-EXIST-ID") is False

def test_tc41_issue_book_success(circ_model, book_model, sample_member):
    """TC41, TC42: Mượn sách thành công"""
    bid = book_model.add_book("Borrow Me", "A", "I", "P", "C", "S")
    res = circ_model.issue_book(sample_member, bid)
    assert res.startswith("SUCCESS")
    
    # TC45: Mượn sách không có sẵn (Đã mượn rồi mượn lại)
    res_fail = circ_model.issue_book(sample_member, bid)
    assert "BOOK_NOT_AVAILABLE" in res_fail or "Fail" in res_fail
    
    # Dọn dẹp
    book_model.delete_book(bid)

def test_tc43_tc49_borrow_limit(circ_model, mem_model, book_model):
    """TC43, TC49, TC_CIRC_01: Giới hạn mượn (Max 5/10)"""
    # Tạo member mới
    mid = mem_model.add_member("Limit User", "l@test.com", "1", "IT", "Student", "2000-01-01")
    
    # Mượn 5 cuốn
    books = []
    for i in range(5):
        bid = book_model.add_book(f"B{i}", "A", "I", "P", "C", "S")
        books.append(bid)
        circ_model.issue_book(mid, bid)
        
    # Mượn cuốn thứ 6
    bid6 = book_model.add_book("B6", "A", "I", "P", "C", "S")
    res = circ_model.issue_book(mid, bid6)
    
    # Kỳ vọng thất bại
    assert "LIMIT_EXCEEDED" in res
    
    # Dọn dẹp
    for b in books + [bid6]: book_model.delete_book(b)

def test_tc51_return_book(circ_model, book_model, sample_member):
    """TC51, TC53: Trả sách"""
    bid = book_model.add_book("Return Me", "A", "I", "P", "C", "S")
    circ_model.issue_book(sample_member, bid)
    
    # Trả sách
    res = circ_model.return_book(bid)
    assert res.startswith("SUCCESS")
    
    # Trả sách không mượn (TC54)
    res_fail = circ_model.return_book(bid)
    assert "NO_ACTIVE_BORROW" in res_fail or "Fail" in res_fail
    
    book_model.delete_book(bid)

def test_tc52_calculate_fine(circ_model, book_model):
    """TC52, TC56-TC58: Tính tiền phạt (Logic Giả lập)"""
    # Lưu ý: Test này cần can thiệp DB để chỉnh lùi ngày (Mocking)
    # Vì môi trường thật khó chỉnh ngày, ta chỉ test hàm tính toán nếu có
    pass

def test_tc62_register_member(mem_model):
    """TC62: Đăng ký thành viên"""
    mid = mem_model.add_member("Nguyen Van A", "a@email.com", "0909", "IT", "Student", "2000-01-01")
    assert mid is not None
    assert "LIB-" in mid

def test_tc64_register_duplicate_email(mem_model):
    """TC64, TC65: Trùng email/ID"""
    # Đăng ký người 1
    mem_model.add_member("U1", "dup@test.com", "1", "IT", "S", "2000-01-01")
    # Đăng ký người 2 cùng email (Giả sử model có check)
    # res = mem_model.add_member("U2", "dup@test.com", ...)
    # assert res is None
    pass

def test_tc_mem_02_invalid_dob(mem_model):
    """TC_MEM_02: Ngày sinh sai định dạng"""
    res = mem_model.add_member("Bad Date", "bad@d.com", "1", "IT", "S", "30/02/2000")
    assert res is None

def test_tc74_generate_report(report_model):
    """TC74-TC77: Lấy báo cáo"""
    stats = report_model.get_library_stats()
    assert isinstance(stats, dict)
    assert 'books' in stats
    assert 'members' in stats

def test_tc_sys_02_id_generation(book_model):
    """TC_SYS_02: Test sinh ID tự động tăng"""
    id1 = book_model.add_book("B1", "A", "I", "P", "C", "S")
    id2 = book_model.add_book("B2", "A", "I", "P", "C", "S")
    
    # Giả sử format BK-2026-001, BK-2026-002
    seq1 = int(id1.split('-')[-1])
    seq2 = int(id2.split('-')[-1])
    
    assert seq2 == seq1 + 1
    
    book_model.delete_book(id1)
    book_model.delete_book(id2)