-- ================================================================
-- SQL SCRIPT GENERATED FROM TEST CASES (GROUP 6)
-- Tự động sinh dữ liệu test từ file Excel
-- ================================================================

USE LibraryDB;

-- ----------------------------------------------------------------
-- 1. INSERT USERS & MEMBERS
-- Mật khẩu mặc định:
-- 'admin@123' -> 7676aaafb027c825bd9abab78b234070e702752f625b752e55e55b48e607e358
-- '15032006'  -> e1aec3b0f97a019e31d38c938b7e197315c5c12197802f57d249b0c5915f43f5
-- '123'       -> a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
-- ----------------------------------------------------------------

-- [TC01, TC05] Admin & Member mặc định
INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role) VALUES 
('ADMIN01', 'ADMIN01', '7676aaafb027c825bd9abab78b234070e702752f625b752e55e55b48e607e358', 'System Administrator', 'admin@library.com', '0901000000', '1990-01-01', 1),
('LIB-2025-001', 'LIB-2025-001', 'e1aec3b0f97a019e31d38c938b7e197315c5c12197802f57d249b0c5915f43f5', 'Test Student 01', 'student1@email.com', '0902000001', '2006-03-15', 2);

INSERT INTO LIBRARIAN (userID) VALUES ('ADMIN01');
INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID) VALUES 
('LIB-2025-001', 'IT', 5, 'Student', 'LIB-2025-001');

-- [TC62] Đăng ký Member mới: Nguyen Van A (Student)
INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role) VALUES 
('LIB-2025-101', 'LIB-2025-101', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Nguyen Van A', 'a@gmail.com', '0902000101', '2000-01-01', 2);

INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID) VALUES 
('LIB-2025-101', 'IT', 5, 'Student', 'LIB-2025-101');

-- [TC66] Đăng ký Member mới: Tran Thi B (Teacher - Limit 10)
INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role) VALUES 
('LIB-2025-100', 'LIB-2025-100', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Tran Thi B', 'b@gmail.com', '0902000100', '1985-05-05', 2);

INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID) VALUES 
('LIB-2025-100', 'Mathematics', 10, 'Teacher', 'LIB-2025-100');


-- ----------------------------------------------------------------
-- 2. INSERT BOOKS
-- Dữ liệu sách lấy từ Test Case (Search, Add, Issue)
-- ----------------------------------------------------------------

-- [TC12] Clean Code
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) VALUES 
('B001', 'Clean Code', 'Robert C. Martin', '9780132350884', 'Prentice Hall', 'Software', 'A1-01', 'Available');

-- [TC41] Book B002 (Sách dùng để test mượn trả)
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) VALUES 
('B002', 'Design Patterns', 'Erich Gamma', '9780201633610', 'Addison-Wesley', 'Software', 'A1-02', 'Issued');

-- [TC32] Python 101 (Sách thêm mới)
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) VALUES 
('B010', 'Python 101', 'Mike Driscoll', '9781234567890', 'Packt', 'Programming', 'B2-10', 'Available');

-- [TC80] Docker Persistence Test (Kiểm tra Volume)
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) VALUES 
('B080', 'Docker Persistence Test', 'Test Author', '978-DOCKER', 'Tech', 'DevOps', 'D1-01', 'Available');


-- ----------------------------------------------------------------
-- 3. INSERT TRANSACTIONS (Giả lập mượn trả)
-- Để test các case trả sách, tính phạt
-- ----------------------------------------------------------------

-- Giao dịch T001: Member 001 đang mượn sách B002 (Issued)
-- Mượn cách đây 5 ngày, chưa trả -> Status Issued là hợp lý
INSERT INTO BORROW_TRANSACTION (TransID, IssueDate, DueDate, ReturnDate, memberID, bookID) VALUES 
('T001', DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_ADD(CURDATE(), INTERVAL 9 DAY), NULL, 'LIB-2025-001', 'B002');

-- ----------------------------------------------------------------
-- 4. INSERT NOTIFICATIONS (Nếu có)
-- ----------------------------------------------------------------
INSERT INTO NOTIFICATION (NotifiID, SentDate, Message, memberID) VALUES 
('N001', CURDATE(), 'Welcome to Library System!', 'LIB-2025-001');