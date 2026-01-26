-- Tạo Database
CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- Bảng USER (Cha)
CREATE TABLE IF NOT EXISTS User (
    userID VARCHAR(20) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password CHAR(64) NOT NULL,
    fullName NVARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    dateOfBirth DATE,
    role INT NOT NULL -- 1: Librarian, 2: Member
);

-- Bảng LIBRARIAN
CREATE TABLE IF NOT EXISTS Librarian (
    librarianID VARCHAR(20) PRIMARY KEY,
    userID VARCHAR(20) UNIQUE, -- Link 1-1 với User
    startDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Bảng MEMBER
CREATE TABLE IF NOT EXISTS Member (
    memberID VARCHAR(20) PRIMARY KEY,
    userID VARCHAR(20) UNIQUE,
    department NVARCHAR(100),
    memberType VARCHAR(20),    -- 'Student' or 'Teacher'
    borrowLimit INT,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Bảng BOOK
CREATE TABLE IF NOT EXISTS Book (
    bookID VARCHAR(20) PRIMARY KEY,
    title NVARCHAR(255) NOT NULL,
    author NVARCHAR(100) NOT NULL,
    isbn VARCHAR(20),
    publisher NVARCHAR(100),
    category NVARCHAR(50),
    shelfLocation VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Available'
);

-- Bảng GIAO DỊCH MƯỢN/TRẢ
CREATE TABLE IF NOT EXISTS BorrowTransaction (
    transID VARCHAR(20) PRIMARY KEY,
    memberID VARCHAR(20),
    bookID VARCHAR(20),
    issueDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    dueDate DATETIME,
    returnDate DATETIME NULL,
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID)
);

-- Bảng PHẠT
CREATE TABLE IF NOT EXISTS Fine (
    fineID VARCHAR(20) PRIMARY KEY,
    transID VARCHAR(20) UNIQUE,
    amount DECIMAL(10, 2) NOT NULL,
    isPaid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (transID) REFERENCES BorrowTransaction(transID)
);

-- Bảng ĐẶT TRƯỚC (Reservation) - (Optional)
CREATE TABLE IF NOT EXISTS Reservation (
    reservationID VARCHAR(20) PRIMARY KEY,
    memberID VARCHAR(20),
    bookID VARCHAR(20),
    reservationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID)
);

-- DỮ LIỆU MẪU (SEED DATA)
-- Tạo User trước (Pass: 'admin123')
INSERT INTO User (userID, username, password, fullName, email, role) 
VALUES ('ADMIN01', 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Super Admin', 'admin@library.com', 1);

INSERT INTO User (userID, username, password, fullName, email, phone, role) 
VALUES (
    'ADMIN02',
    'admin2',
    '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
    'Super Admin',
    'admin@library.com',
    '0909123456',
    1
);

-- 2. Tạo Librarian liên kết với User vừa tạo
INSERT INTO Librarian (librarianID, userID, startDate)
VALUES ('LIB01', 'ADMIN01', NOW());

-- 3. Tạo Sách mẫu
INSERT INTO Book (bookID, title, author, category, status) 
VALUES ('BK001', 'Clean Code', 'Robert C. Martin', 'Education', 'Available');