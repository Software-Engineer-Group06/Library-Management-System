import pytest
from unittest.mock import MagicMock, patch
from models.member import MemberModel

# Mock (Giả lập) kết nối DB
@pytest.fixture
def mock_db():
    with patch('models.member.get_connection') as mock_connect:
        mock_conn_instance = MagicMock()
        mock_cursor = MagicMock()
        
        mock_connect.return_value = mock_conn_instance
        mock_conn_instance.cursor.return_value = mock_cursor
        
        yield mock_cursor  # Trả về con trỏ giả để ta điều khiển

def test_generate_new_member_id_logic(mock_db):
    """
    Unit Test: Kiểm tra logic sinh ID (TC_SYS_02)
    Không cần DB thật, ta giả bộ DB trả về kết quả cũ.
    """
    model = MemberModel()
    
    # 1. Giả lập trường hợp DB đã có ID cũ là LIB-2026-009
    mock_db.fetchone.return_value = ('LIB-2026-009',) 
    
    # 2. Gọi hàm cần test
    new_id = model._generate_new_member_id()
    
    # 3. Kiểm tra xem nó có cộng lên 1 thành 010 không
    assert new_id == "LIB-2026-010"

def test_add_member_transaction_call(mock_db):
    """Unit Test: Kiểm tra xem hàm add_member có gọi commit() không"""
    model = MemberModel()
    data = {
        'fullname': 'Test Unit', 'department': 'IT', 'email': 't@t.com',
        'phone': '123', 'member_type': 'Student', 'dob': None
    }
    
    model.add_member(data)
    
    # Kiểm tra code có gọi lệnh commit không? (Đảm bảo tính toàn vẹn)
    model.db.commit.assert_called_once()