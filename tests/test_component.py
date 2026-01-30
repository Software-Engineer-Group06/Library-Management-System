import pytest
from models.book import BookModel

# Fixture này chạy 1 lần trước khi test
@pytest.fixture(scope="module")
def setup_database():
    print("\n--- SETUP: CLEANING TEST DATA ---")
    # Viết code xóa dữ liệu rác nếu cần
    # cursor.execute("DELETE FROM BOOK WHERE title LIKE 'TEST%'")
    yield
    print("\n--- TEARDOWN: FINISHED ---")

def test_tc32_add_book_real_db(setup_database):
    """Test thêm sách vào DB thật"""
    model = BookModel()
    
    book_data = {
        'bookID': 'TEST-BK-999',
        'title': "TEST_INTEGRATION",
        'author': "Author",
        'ISBN': "ISBN-TEST-UNIQUE-999", 
        'publisher': "Pub",
        'category': "Cat",
        'shelfLocation': "Z1",
        'status': 'Available'
    }
    
    # Gọi hàm thêm
    bid = model.add_book(book_data)
    
    # 1. Debug: In ra xem nó trả về cái gì?
    print(f"\n>> DEBUG ADD BOOK RESULT: {bid}")

    # 2. Kiểm tra chặn: Nếu thêm thất bại thì dừng test luôn, báo lỗi rõ ràng
    assert bid is not None and bid is not False, "Lỗi: Hàm add_book trả về False/None (Thêm thất bại)"

    # 3. Tìm kiếm lại
    books = model.search_books("TEST_INTEGRATION")
    
    # 4. Debug: In ra danh sách tìm được
    print(f">> DEBUG SEARCH RESULT: {books}")

    assert len(books) >= 1
    
    # Dọn dẹp
    if bid:
        model.delete_book(bid)