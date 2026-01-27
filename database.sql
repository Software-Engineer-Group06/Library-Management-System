CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- Bảng USER 
CREATE TABLE IF NOT EXISTS USER (
    userID VARCHAR(20) PRIMARY KEY,
    username VARCHAR(20),
    password CHAR(64),
    fullName VARCHAR(40),
    email VARCHAR(50),
    phone CHAR(10),
    dateOfBirth DATE,
    role INTEGER
);

-- Bảng LIBRARIAN
CREATE TABLE IF NOT EXISTS LIBRARIAN (
    userID VARCHAR(20) PRIMARY KEY,
    FOREIGN KEY (userID) REFERENCES USER(userID) ON DELETE CASCADE
);

-- Bảng MEMBER
CREATE TABLE IF NOT EXISTS MEMBER (
    memberID VARCHAR(20) PRIMARY KEY,
    Department VARCHAR(20),
    BorrowLimit INTEGER,
    MemberType VARCHAR(10),
    userID VARCHAR(20),
    FOREIGN KEY (userID) REFERENCES USER(userID) ON DELETE CASCADE
);

-- Bảng BOOK
CREATE TABLE IF NOT EXISTS BOOK (
    bookID VARCHAR(20) PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(40),
    ISBN VARCHAR(20),
    publisher VARCHAR(40),
    category VARCHAR(50),
    shelfLocation VARCHAR(10),
    status VARCHAR(10) DEFAULT 'Available'
);

-- Bảng BORROW_TRANSACTION
CREATE TABLE IF NOT EXISTS BORROW_TRANSACTION (
    TransID VARCHAR(20) PRIMARY KEY,
    IssueDate DATE,
    DueDate DATE,
    ReturnDate DATE,
    memberID VARCHAR(20), 
    bookID VARCHAR(20),
    FOREIGN KEY (memberID) REFERENCES MEMBER(memberID),
    FOREIGN KEY (bookID) REFERENCES BOOK(bookID)
);

-- Bảng FINE
CREATE TABLE IF NOT EXISTS FINE (
    FineID VARCHAR(20) PRIMARY KEY,
    Amount FLOAT,
    Paid BOOLEAN DEFAULT FALSE,
    TransID VARCHAR(20),
    FOREIGN KEY (TransID) REFERENCES BORROW_TRANSACTION(TransID)
);

-- Bảng NOTIFICATION
CREATE TABLE IF NOT EXISTS NOTIFICATION (
    NotifiID VARCHAR(20) PRIMARY KEY,
    SentDate DATE,
    Message VARCHAR(200),
    memberID VARCHAR(20), 
    FOREIGN KEY (memberID) REFERENCES MEMBER(memberID)
);

-- Bảng RESERVATION
CREATE TABLE IF NOT EXISTS RESERVATION (
    ReservationID VARCHAR(20) PRIMARY KEY,
    Status VARCHAR(100),
    ReservationDate DATE,
    memberID VARCHAR(20),
    bookID VARCHAR(20),
    FOREIGN KEY (memberID) REFERENCES MEMBER(memberID),
    FOREIGN KEY (bookID) REFERENCES BOOK(bookID)
);


-- Tạo User Admin
INSERT INTO USER VALUES ('LIB01', 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Tran Chi Minh', 'minh@email.com', '0901234567', '2006-07-06', 1);
-- Insert vào bảng Librarian cho đúng logic
INSERT INTO LIBRARIAN VALUES ('LIB01');

-- Tạo User Member
INSERT INTO USER VALUES ('MEM01', 'student1', 'e86fdc2283ce92a83e054170e5f2425032543e49339239567c9c0f997f374347', 'Nguyen Van A', 'a@email.com', '0909999999', '2006-07-06', 2);
-- Insert vào bảng Member (Lưu ý: memberID đang giả định trùng với userID trong code cũ của bạn, nhưng logic đúng nên là auto-gen)
INSERT INTO MEMBER VALUES ('MEM01', 'IT', 5, 'Student', 'MEM01');

-- Tạo Sách
INSERT INTO BOOK VALUES ('B001', 'Clean Code', 'Robert C. Martin', '978-0132350884', 'Prentice Hall', 'Software', 'A1', 'Available');
INSERT INTO BOOK VALUES ('B002', 'Design Patterns', 'Erich Gamma', '978-0201633610', 'Addison-Wesley', 'Software', 'A2', 'Issued');
INSERT INTO BOOK VALUES ('B003', 'Harry Potter', 'J.K. Rowling', '978-0747532743', 'Bloomsbury', 'Fiction', 'B1', 'Available');

-- Tạo Notification
INSERT INTO NOTIFICATION VALUES ('N001', '2025-10-01', 'Reminder: Book is due in 2 days.', 'MEM01');
INSERT INTO NOTIFICATION VALUES ('N002', '2025-10-05', 'Reserved book is now available.', 'MEM01');