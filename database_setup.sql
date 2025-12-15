-- Database: SmartPayDB
USE master;
GO

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SmartPayDB')
BEGIN
    CREATE DATABASE SmartPayDB;
END
GO

USE SmartPayDB;
GO

-- Table: Users
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
BEGIN
    CREATE TABLE Users (
        user_id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(50) NOT NULL UNIQUE,
        password NVARCHAR(255) NOT NULL -- In a real app, store hashed passwords
    );
END
GO

-- Table: Categories
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Categories')
BEGIN
    CREATE TABLE Categories (
        category_id INT IDENTITY(1,1) PRIMARY KEY,
        category_name NVARCHAR(50) NOT NULL UNIQUE
    );
END
GO

-- Table: Transactions
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Transactions')
BEGIN
    CREATE TABLE Transactions (
        trans_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        category_id INT NOT NULL,
        amount DECIMAL(18, 2) NOT NULL,
        trans_type NVARCHAR(10) CHECK (trans_type IN ('Income', 'Expense')) NOT NULL,
        trans_date DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    );
END
GO

-- Seed Default Categories
IF NOT EXISTS (SELECT * FROM Categories)
BEGIN
    INSERT INTO Categories (category_name) VALUES 
    ('Salary'), ('Business'), ('Investment'), -- Income
    ('Food'), ('Rent'), ('Utilities'), ('Entertainment'), ('Transport'), ('Health'); -- Expense
END
GO
