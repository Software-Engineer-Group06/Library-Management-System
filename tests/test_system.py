import pytest
from datetime import datetime
from unittest.mock import patch
from controllers.auth_controller import AuthController

def test_tc01_full_login_flow():
    controller = AuthController()

    # Tạo một user giả để Model trả về (Bỏ qua DB thật)
    mock_user = {
        'userID': 'ADMIN01', 
        'role': 1, 
        'username': 'admin',
        'password': 'hashed_password_example', # Cần field này để code không lỗi
        'dateOfBirth': datetime(1990, 1, 1)    # Cần field này để chạy strftime
    }

    with patch('builtins.input', side_effect=['ADMIN01', 'admin123']), \
         patch('views.auth_view.AuthView.display_login_success') as mock_success, \
         patch('controllers.auth_controller.AuthController.redirect_to_dashboard') as mock_redirect, \
         patch('models.user.UserModel.verify_login', return_value=mock_user): # <--- THÊM DÒNG NÀY

        # Giải thích: Dòng trên ép UserModel luôn trả về mock_user 
        # bất kể nhập cái gì. Như vậy Login chắc chắn thành công.
        
        controller.process_login()

        # Kiểm tra
        mock_success.assert_called_once()
        mock_redirect.assert_called_with(1)

def test_tc41_issue_book_flow():
    """System Test: Luồng mượn sách từ A-Z"""
    # Tương tự: Mock input MemberID, BookID, Date...
    pass