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


-- Tạo User Admin / password : abc@123
INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role)
VALUES (
  'LIBRA-001',
  'LIBRA-001',
  'e5857b335afdf35ca81a110bc81f38682f8a89892cc597f5398dfef82d42b513',
  'Librarian One',
  'libra1@library.com',
  '0904444444',
  '1995-01-01',
  1
);

INSERT INTO LIBRARIAN (userID)
VALUES ('LIBRA-001');

-- member password : 15032006
INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role) 
VALUES (
    'LIB-2025-001', 
    'LIB-2025-001', 
    'e1aec3b0f97a019e31d38c938b7e197315c5c12197802f57d249b0c5915f43f5', 
    'Nguyen Van Tuan', 
    'student1@email.com', 
    '0902222222', 
    '2006-03-15', 
    2 -- Role 2 = Member
);

INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID) 
VALUES (
    'LIB-2025-001', 
    'IT', 
    5, 
    'Student', 
    'LIB-2025-001'
);

INSERT INTO USER (userID, username, password, fullName, email, phone, dateOfBirth, role) 
VALUES (
    'LIB-2025-002', 
    'LIB-2025-002', 
    'e1aec3b0f97a019e31d38c938b7e197315c5c12197802f57d249b0c5915f43f5', 
    'Le Thi Nga', 
    'student2@email.com', 
    '0903333333', 
    '2006-03-15', 
    2 -- Role 2 = Member
);

-- Chèn vào bảng MEMBER (Con)
INSERT INTO MEMBER (memberID, Department, BorrowLimit, MemberType, userID) 
VALUES (
    'LIB-2025-002', 
    'Business', 
    5, 
    'Student', 
    'LIB-2025-002'
);
-- B001: Clean Code -> Trạng thái ISSUED 
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) 
VALUES ('B001', 'Clean Code', 'Robert C. Martin', '9780132350884', 'Prentice Hall', 'Software', 'A1-01', 'Issued');

-- B002: Design Patterns -> Trạng thái AVAILABLE 
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) 
VALUES ('B002', 'Design Patterns', 'Erich Gamma', '9780201633610', 'Addison-Wesley', 'Software', 'A1-02', 'Available');

-- B003: Intro to Algorithms -> Trạng thái ISSUED (Quá hạn) 
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) 
VALUES ('B003', 'Introduction to Algorithms', 'Thomas H. Cormen', '9780262033848', 'MIT Press', 'Academic', 'B2-05', 'Issued');

-- B004: Pragmatic Programmer -> AVAILABLE
INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status) 
VALUES ('B004', 'The Pragmatic Programmer', 'Andrew Hunt', '9780201616224', 'Addison-Wesley', 'Software', 'A1-03', 'Available');

-- Ngày mượn cách đây 5 ngày, Hạn trả còn 9 ngày nữa (Chưa quá hạn)
INSERT INTO BORROW_TRANSACTION (TransID, IssueDate, DueDate, ReturnDate, memberID, bookID) 
VALUES ('T001', DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_ADD(CURDATE(), INTERVAL 9 DAY), NULL, 'LIB-2025-002', 'B001');

-- Mượn 30 ngày trước, Trả 18 ngày trước
INSERT INTO BORROW_TRANSACTION (TransID, IssueDate, DueDate, ReturnDate, memberID, bookID) 
VALUES ('T002', DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_SUB(CURDATE(), INTERVAL 16 DAY), DATE_SUB(CURDATE(), INTERVAL 18 DAY), 'LIB-2025-001', 'B002');

-- Mượn 20 ngày trước, Hạn trả là 3 ngày trước (Quá hạn 3 ngày -> Sẽ bị tính phạt)
INSERT INTO BORROW_TRANSACTION (TransID, IssueDate, DueDate, ReturnDate, memberID, bookID) 
VALUES ('T003', DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_SUB(CURDATE(), INTERVAL 3 DAY), NULL, 'LIB-2025-002', 'B003');

-- N001: Nhắc nhở hạn trả
INSERT INTO NOTIFICATION (NotifiID, SentDate, Message, memberID) 
VALUES ('N001', CURDATE(), 'Reminder: Book is due in 2 days.', 'LIB-2025-001');

-- N002: Chào mừng thành viên mới
INSERT INTO NOTIFICATION (NotifiID, SentDate, Message, memberID) 
VALUES ('N002', DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Welcome to the Library System!', 'LIB-2025-001');