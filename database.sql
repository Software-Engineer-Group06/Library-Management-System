CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- Tạo bảng USER dựa trên 
CREATE TABLE IF NOT EXISTS USER (
    userID VARCHAR(20) PRIMARY KEY,
    username VARCHAR(20),
    password CHAR(64), -- SHA-256 luôn dài 64 ký tự
    fullName VARCHAR(40),
    email VARCHAR(50),
    phone CHAR(10),
    dateOfBirth DATE,
    role INTEGER -- 1: Librarian, 2: Member (Student/Teacher)
);

CREATE TABLE IF NOT EXISTS MEMBER (
    memberID VARCHAR(20) PRIMARY KEY,
    Department VARCHAR(20),
    BorrowLimit INTEGER,
    MemberType VARCHAR(10), -- 'Student' hoặc 'Teacher'
    userID VARCHAR(20),
    FOREIGN KEY (userID) REFERENCES USER(userID) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS BOOK (
    bookID VARCHAR(20) PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(40),
    ISBN VARCHAR(20),
    publisher VARCHAR(40),
    category VARCHAR(50),
    shelfLocation VARCHAR(10),
    status VARCHAR(10) DEFAULT 'Available' 
    -- Status values: 'Available', 'Issued', 'Lost' [cite: 18, 307]
);

CREATE TABLE IF NOT EXISTS BORROW_TRANSACTION (
    TransID VARCHAR(20) PRIMARY KEY,
    IssueDate DATE,
    DueDate DATE,
    ReturnDate DATE, -- NULL nếu chưa trả
    memberID VARCHAR(20),
    bookID VARCHAR(20),
    FOREIGN KEY (memberID) REFERENCES USER(userID), -- Giả sử Member ID là User ID
    FOREIGN KEY (bookID) REFERENCES BOOK(bookID)
);

-- Bảng tiền phạt
CREATE TABLE IF NOT EXISTS FINE (
    FineID VARCHAR(20) PRIMARY KEY,
    Amount FLOAT,
    Paid BOOLEAN DEFAULT FALSE,
    TransID VARCHAR(20),
    FOREIGN KEY (TransID) REFERENCES BORROW_TRANSACTION(TransID)
);

CREATE TABLE IF NOT EXISTS NOTIFICATION (
    NotifiID VARCHAR(20) PRIMARY KEY,
    SentDate DATE,
    Message VARCHAR(200),
    memberID VARCHAR(20),
    FOREIGN KEY (memberID) REFERENCES USER(userID)
);
-- Insert dữ liệu mẫu
-- User 1: Admin (Librarian). Pass: 'admin123' (đã hash)
INSERT INTO USER VALUES ('LIB01', 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Tran Chi Minh', 'minh@email.com', '0901234567', '2006-07-06', 1);

-- User 2: Member mới. Pass: '06072006' (Trùng DOB -> sẽ bắt đổi pass).
INSERT INTO USER VALUES ('MEM01', 'student1', 'e86fdc2283ce92a83e054170e5f2425032543e49339239567c9c0f997f374347', 'Nguyen Van A', 'a@email.com', '0909999999', '2006-07-06', 2);

INSERT INTO BOOK VALUES ('B001', 'Clean Code', 'Robert C. Martin', '978-0132350884', 'Prentice Hall', 'Software', 'A1', 'Available');
INSERT INTO BOOK VALUES ('B002', 'Design Patterns', 'Erich Gamma', '978-0201633610', 'Addison-Wesley', 'Software', 'A2', 'Issued');
INSERT INTO BOOK VALUES ('B003', 'Harry Potter', 'J.K. Rowling', '978-0747532743', 'Bloomsbury', 'Fiction', 'B1', 'Available');

INSERT INTO NOTIFICATION VALUES ('N001', '2025-10-01', 'Reminder: Book is due in 2 days.', 'MEM01');
INSERT INTO NOTIFICATION VALUES ('N002', '2025-10-05', 'Reserved book is now available.', 'MEM01');