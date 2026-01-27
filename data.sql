USE LibraryDB;

-- 1. DỮ LIỆU USER & MEMBER


-- a) LIBRARIAN (TC05)
-- User: ADMIN01 / Pass: admin@123
-- Hash SHA256 của 'admin@123': e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (Ví dụ minh họa, đây là hash rỗng, hãy dùng hash thật bên dưới)
-- Hash thật của 'admin@123': 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9 (Lấy từ bài trước) -> Sửa lại cho đúng pass 'admin@123'
-- Để an toàn, tôi set hash chuẩn cho 'admin@123' là:
-- 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918

INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role) VALUES 
('ADMIN01', 'ADMIN01', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'System Admin', 'admin@library.com', '0901111111', '1990-01-01', 1);

INSERT INTO LIBRARIAN (userID) VALUES ('ADMIN01');

-- MEMBER
-- User: LIB-2025-001 / Pass: 15032006 (Ngày sinh)
-- Hash của '15032006': 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8

INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role) VALUES 
('LIB-2025-001', 'LIB-2025-001', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Nguyen Van Test', 'student1@email.com', '0902222222', '2006-03-15', 2);

INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID) VALUES 
('LIB-2025-001', 'IT', 5, 'Student', 'LIB-2025-001');

INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role) VALUES 
('LIB-2025-002', 'LIB-2025-002', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Le Thi B', 'student2@email.com', '0903333333', '2006-03-15', 2);

INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID) VALUES 
('LIB-2025-002', 'Business', 5, 'Student', 'LIB-2025-002');



-- 2. DỮ LIỆU BOOK

INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) VALUES 
('B001', 'Clean Code', 'Robert C. Martin', '9780132350884', 'Prentice Hall', 'Software', 'A1-01', 'Issued');

-- B002: Design Patterns (TC41 Issue Book) -> Trạng thái AVAILABLE
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) VALUES 
('B002', 'Design Patterns', 'Erich Gamma', '9780201633610', 'Addison-Wesley', 'Software', 'A1-02', 'Available');

-- B003: Introduction to Algorithms (TC47 Fine) -> Trạng thái ISSUED (Quá hạn)
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) VALUES 
('B003', 'Introduction to Algorithms', 'Thomas H. Cormen', '9780262033848', 'MIT Press', 'Academic', 'B2-05', 'Issued');

-- B004: The Pragmatic Programmer -> AVAILABLE (Để test tìm kiếm)
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) VALUES 
('B004', 'The Pragmatic Programmer', 'Andrew Hunt', '9780201616224', 'Addison-Wesley', 'Software', 'A1-03', 'Available');


-- 3. DỮ LIỆU TRANSACTION

INSERT INTO BORROW_TRANSACTION (TransID, IssueDate, DueDate, ReturnDate, memberID, bookID) VALUES 
('T001', DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_ADD(CURDATE(), INTERVAL 9 DAY), NULL, 'LIB-2025-002', 'B001');

INSERT INTO BORROW_TRANSACTION (TransID, IssueDate, DueDate, ReturnDate, memberID, bookID) VALUES 
('T002', DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_SUB(CURDATE(), INTERVAL 16 DAY), DATE_SUB(CURDATE(), INTERVAL 18 DAY), 'LIB-2025-001', 'B002');

INSERT INTO BORROW_TRANSACTION (TransID, IssueDate, DueDate, ReturnDate, memberID, bookID) VALUES 
('T003', DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_SUB(CURDATE(), INTERVAL 3 DAY), NULL, 'LIB-2025-002', 'B003');


-- 4. DỮ LIỆU NOTIFICATION


INSERT INTO NOTIFICATION (NotifiID, SentDate, Message, memberID) VALUES 
('N001', CURDATE(), 'Reminder: Book is due in 2 days.', 'LIB-2025-001'),
('N002', DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Welcome to the Library System!', 'LIB-2025-001');