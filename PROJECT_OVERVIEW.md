# Smart Pay App - Project Overview

## 1. Project Description
**Smart Pay App** is a comprehensive desktop-based personal finance management system built with Python. It allows users to manage their daily finances, track income/expenses, and perform peer-to-peer (P2P) money transfers. The application mimics a real-world digital wallet with professional features like QR code generation and PDF reporting.

## 2. Technology Stack
- **Language**: Python 3.x
- **GUI Framework**: Tkinter (Standard Python Library)
- **Database**: Microsoft SQL Server (Express Edition)
- **Database Driver**: `pyodbc`
- **PDF Generation**: `fpdf`
- **QR Code Generation**: `qrcode` + `Pillow`
- **OS Compatibility**: Windows

## 3. Key Features (Functional Requirements)
The application implements **13 Core Features**:
1.  **User Registration**: Secure account creation with duplicate username checks.
2.  **Auto-generated Account Numbers**: Every user gets a unique 10-digit Account ID upon registration.
3.  **Secure Login**: Username/Password authentication system.
4.  **Interactive Dashboard**: Central hub displaying Welcome Message, Live Balance, Account Number, and QR Code.
5.  **QR Code Integration**: Visual representation of the User's Account Number for easy scanning.
6.  **Add Income**: Log earnings with Date, Amount, Category, and Description.
7.  **Add Expense**: Log spending with detailed metadata.
8.  **P2P Money Transfer (Send Money)**:
    - Atomic transactions (ensures data consistency).
    - Auto-populates descriptions (e.g., "Received from Ali").
9.  **Transaction History**: Tabular view (Treeview) of all financial activities (Income, Expenses, Transfers).
10. **Data Persistence**: All data is stored permanently in a relational SQL Server database.
11. **Live Balance Calculation**: Dynamic aggregation of (Total Income - Total Expenses).
12. **PDF Receipts**:
    - **Instant**: Generate receipt immediately after a transfer.
    - **On-Demand**: Download a receipt for *any* past transaction from history.
13. **Sender Identification**: Receipts intelligently display the Sender's Name for received funds.

## 4. Database Schema
**Database Name**: `SmartPayDB`

### Table: `Users`
| Column | Type | Description |
| :--- | :--- | :--- |
| `user_id` | INT (PK) | Auto-incrementing ID |
| `username` | NVARCHAR(50) | Unique Login ID |
| `password` | NVARCHAR(50) | User Password |
| `account_number` | NVARCHAR(20) | Unique 10-digit ID |

### Table: `Categories`
| Column | Type | Description |
| :--- | :--- | :--- |
| `category_id` | INT (PK) | Auto-incrementing ID |
| `category_name` | NVARCHAR(50) | e.g., Food, Salary, Transfer Sent |
| `type` | NVARCHAR(10) | 'Income' or 'Expense' |

### Table: `Transactions`
| Column | Type | Description |
| :--- | :--- | :--- |
| `trans_id` | INT (PK) | Auto-incrementing ID |
| `user_id` | INT (FK) | Links to `Users.user_id` |
| `category_id` | INT (FK) | Links to `Categories.category_id` |
| `amount` | DECIMAL(10,2)| Transaction Value |
| `trans_type` | NVARCHAR(10) | 'Income' or 'Expense' |
| `trans_date` | DATE | Date of transaction |
| `description` | NVARCHAR(255)| Notes / Sender Info |

## 5. Project File Structure
- `main.py`: Entry point. Manages app lifecycle and window switching.
- `db_connection.py`: Singleton class for managing SQL Server connection strings and drivers.
- `user_controller.py`: Handles Auth logic (Register, Login, User IDs).
- `transaction_controller.py`: Core logic for Balance, Adding Transactions, and Transfers.
- `gui_auth.py`: Login and Registration window classes.
- `gui_dashboard.py`: Main User Interface (Dashboard).
- `gui_transactions.py`: Income/Expense forms and History Table views.
- `gui_transfer.py`: "Send Money" UI logic.
- `utils.py`: Helper functions for **QR generation** and **PDF creation**.
- `setup_db_auto.py`: Automation script to create DB and Tables.

## 6. Setup Instruction
1.  **Install Python Libraries**:
    ```bash
    pip install pyodbc qrcode[pil] fpdf
    ```
2.  **Database**: Ensure SQL Server Express is running.
3.  **Run Application**:
    ```bash
    python main.py
    ```
