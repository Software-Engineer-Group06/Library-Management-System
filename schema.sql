-- Tạo Database
CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- Tạo bảng USER (Bảng cha)
-- Lưu thông tin đăng nhập và thông tin chung
CREATE TABLE IF NOT EXISTS User (
    userID VARCHAR(20) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password CHAR(64) NOT NULL, -- SHA-256 Hash length
    fullName NVARCHAR(100),     -- Hỗ trợ tiếng Việt
    email VARCHAR(100),
    phone VARCHAR(15),
    dateOfBirth DATE,
    role INT NOT NULL           -- 1: Librarian, 2: Member
);

-- Tạo bảng LIBRARIAN (Kế thừa từ User)
CREATE TABLE IF NOT EXISTS Librarian (
    userID VARCHAR(20) PRIMARY KEY,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Tạo bảng MEMBER (Kế thừa từ User)
CREATE TABLE IF NOT EXISTS Member (
    memberID VARCHAR(20) PRIMARY KEY,
    userID VARCHAR(20) UNIQUE, -- Link 1-1 với User
    department NVARCHAR(100),
    memberType VARCHAR(20),    -- 'Student' or 'Teacher'
    borrowLimit INT,           -- 5 for Student, 10 for Teacher
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Tạo bảng BOOK (Kho sách)
CREATE TABLE IF NOT EXISTS Book (
    bookID VARCHAR(20) PRIMARY KEY,
    title NVARCHAR(255) NOT NULL,
    author NVARCHAR(100) NOT NULL,
    isbn VARCHAR(20),
    publisher NVARCHAR(100),
    category NVARCHAR(50),
    shelfLocation VARCHAR(50), -- Vị trí kệ
    status VARCHAR(20) DEFAULT 'Available' -- Available, Borrowed, Reserved, Lost
);

-- Tạo bảng BORROW_TRANSACTION (Giao dịch Mượn/Trả)
CREATE TABLE IF NOT EXISTS BorrowTransaction (
    transID VARCHAR(20) PRIMARY KEY,
    memberID VARCHAR(20),
    bookID VARCHAR(20),
    issueDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    dueDate DATETIME,
    returnDate DATETIME NULL,  -- NULL nghĩa là chưa trả
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID)
);

-- Tạo bảng FINE (Tiền phạt)
CREATE TABLE IF NOT EXISTS Fine (
    fineID VARCHAR(20) PRIMARY KEY,
    transID VARCHAR(20) UNIQUE, -- Mỗi giao dịch chỉ có 1 phiếu phạt (nếu có)
    amount DECIMAL(10, 2) NOT NULL,
    isPaid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (transID) REFERENCES BorrowTransaction(transID)
);

-- Tạo bảng RESERVATION (Đặt trước)
CREATE TABLE IF NOT EXISTS Reservation (
    reservationID VARCHAR(20) PRIMARY KEY,
    memberID VARCHAR(20),
    bookID VARCHAR(20),
    reservationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Active', -- Active, Completed, Cancelled
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID)
);

-- Tạo bảng NOTIFICATION (Thông báo)
CREATE TABLE IF NOT EXISTS Notification (
    notifyID VARCHAR(20) PRIMARY KEY,
    memberID VARCHAR(20),
    message NVARCHAR(500),
    sentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    isRead BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

-- DỮ LIỆU MẪU (SEED DATA) - DÙNG ĐỂ TEST
INSERT INTO User (userID, username, password, role) 
VALUES ('ADMIN01', 'admin', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1);

INSERT INTO Librarian (userID) VALUES ('ADMIN01');

-- Book Sample
INSERT INTO Book (bookID, title, author, category, status) 
VALUES ('BK001', 'Clean Code', 'Robert C. Martin', 'Education', 'Available');