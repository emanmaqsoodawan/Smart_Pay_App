Final Project Report: Smart Pay App
Course: Software Construction and Development
Project Name: Smart Pay App
Version: 1.0.0
Date: December 28, 2025

Table of Contents
1. Project Overview
2. Software Process Model & Justification
3. Software Process Improvement (SPI)
4. Version Control Implementation
5. Justification of Lehman's Laws
6. Software Deployment Management
7. Refactoring and Legacy Code Removal
8. Unit and Automated Testing
9. Exception Handling
10. Peer Reviews (Inspections & Walkthroughs)
11. System Architecture
12. Features and Modules
13. Database Design
14. User Interface Design
15. Security Implementation
16. Testing Strategy
17. Future Enhancements
18. Conclusion
19. References

---

# 1. Project Overview
## 1.1 Objective
To develop a robust, desktop-based financial transaction management system ("Smart Pay App") demonstrating core software construction principles such as Model-View-Controller (MVC) architecture, automated testing using standard libraries, and secure database practices.

## 1.2 Purpose
The Smart Pay App allows users to manage their personal finances securely. It facilitates:
- User Registration and Secure Login
- Real-time Balance Tracking
- P2P (Peer-to-Peer) Money Transfers via Account Identifiers
- Transaction History Tracking (Incomes/Expenses)
- Automated Receipt Generation (PDF)

## 1.3 Scope
The system is targeted for personal banking simulation, focusing on:
- **Financial Management:** Tracking income, expenses, and categories.
- **Digital Payments:** Simulating QR-code based or direct account transfers.
- **Reporting:** Visual transaction history and downloadable PDF receipts.

## 1.4 Technology Stack
- **Programming Language:** Python 3.x
- **GUI Framework:** Tkinter (Custom styled)
- **Database:** SQL Server (via `pyodbc`) / SQLite (Development)
- **Testing:** Python `unittest` framework & `unittest.mock`
- **Additional Libraries:** 
  - `qrcode` (for visual account ID)
  - `fpdf` (for PDF receipt generation)

---

# 2. Software Process Model & Justification
## 2.1 Selected Model: Agile (Iterative & Incremental)
We adopted an Agile methodology, specifically an Iterative approach, to build the Smart Pay App.

## 2.2 Justification
- **Iterative Delivery:** The project was broken down into functional components:
    - *Iteration 1:* Database Connectivity & Schema Design.
    - *Iteration 2:* Authentication (Login/Register) & User Controller.
    - *Iteration 3:* Core Dashboard & Transaction Logic.
    - *Iteration 4:* Advanced Features (Transfers, PDF Receipts) & Refactoring.
- **Adaptability:** Requirements evolved during development (e.g., adding "Account Numbers" and "Proactive DB Maintenance Scripts"), which Agile accommodated without halting progress.
- **Risk Management:** Critical components like Database Connectivity were tested and verified first (`db_connection.py`), minimizing integration risks later.

---

# 3. Software Process Improvement (SPI)
## 3.1 Initial State Analysis
Initially, the project relied on manual testing of GUI forms and scattered SQL scripts (`diagnose_db.py`, `setup_db_auto.py`) in the root directory, leading to clutter and potential errors.

## 3.2 Implemented Improvements
- **Testing-First Mindset:** We integrated the `unittest` framework, creating a dedicated `tests/` directory. This allowed us to verify logic (like transfer balance checks) without loading the GUI.
- **Directory Organization:** We moved ad-hoc scripts to `maintenance_scripts/` to clean the workspace, enforcing a standard structure.
- **Standardized naming:** Adopted `controller` vs `gui` naming to separate logic from presentation.

---

# 4. Version Control Implementation
## 4.1 Git Strategy
Used Git for local version control to track evolution.

## 4.2 Branching Strategy
We implemented a structured branching strategy to manage features and stability:

**Branch Structure:**
```text
main/  (Stable Production Release)
├── develop/  (Integration Branch)
│   ├── feature/auth-system      (Login/Register implementation)
│   ├── feature/transaction-log  (Core logic for Money Transfer)
│   ├── feature/gui-dashboard    (Tkinter UI layout)
│   └── feature/pdf-reporting    (Receipt generation module)
└── hotfix/
    └── db-connection-patch      (Critical fix for SQL Server timeout)
```

**Strategy Implementation:**
- **Main:** Contains only tested, production-ready code.
- **Develop:** Acts as the staging area where features are merged.
- **Feature Branches:** Isolated environments for developing specific modules (e.g., `feature/auth-system`) without breaking the main build.
- **Hotfix:** Immediate patches for critical bugs found during testing.

## 4.3 Application
- **Commit History:** Tracked changes from initial "Hello World" GUI to the complex Multi-Window application.
- **Simulated Collaboration:** The workflow mimicked a pair-programming environment (User + AI Assistant), where "Reviews" acted as pull request approvals.

---

# 5. Justification of Lehman's Laws
## 5.1 Law of Increasing Complexity
*Lehman's Second Law* states that as a system evolves, its complexity increases unless work is done to maintain it.

## 5.2 Evidence in Project
- **Evolution:** We started with simple `Income/Expense` recording. We then added `P2P Transfers`, which introduced complex constraints (Atomic transactions: Sender Debit + Receiver Credit).
- **Complexity Management:** 
    - To handle this, we refactored the monolithic logic into `TransactionController` with specific methods (`add_transaction` vs `transfer_funds`).
    - We introduced `try-except-finally` blocks in database handling to manage the increased risk of connection leaks.

---

# 6. Software Deployment Management
## 6.1 Deployment Strategy
The application is designed as a standalone Desktop Application.

## 6.2 Pre-requisites
1.  **Python 3.10+** installed.
2.  **SQL Server** instance available (or configured Connection String).
3.  **Dependencies:** `pip install pyodbc qrcode fpdf pillow`

## 6.3 Execution
The entry point is standardized to `main.py`.
```bash
python main.py
```
This script handles the initialization of the Root Tkinter window and safe shutdown.

---

# 7. Refactoring and Legacy Code Removal
## 7.1 Identifiable Technical Debt
Early versions had SQL queries hardcoded inside GUI buttons (e.g., in `gui_auth.py`). This made it impossible to test logic without clicking buttons.

## 7.2 Refactoring Actions
- **MVC Separation:** Extracted SQL logic into `user_controller.py` and `transaction_controller.py`.
- **Legacy Cleanup:** Old diagnostic scripts (`verify_transfer.py`, `update_db.py`) were consolidated or moved to `maintenance_scripts/` to avoid confusion.
- **Code reuse:** Created `utils.py` for shared functions like QR Code generation and Receipt formatting, removing duplication in UI files.

---

# 8. Unit and Automated Testing
## 8.1 Framework
We utilized the standard **Python `unittest`** library.

## 8.2 Test Suite Structure (`tests/`)
- `test_user_controller.py`: Mocks the DB connection to test Login/Register logic (Success/Fail scenarios).
- `test_transaction_controller.py`: logical tests for balance calculations.
- `test_utils.py`: Verifies that helper functions (like PDF generation) run without errors.

## 8.3 Automation
Tests can be executed in bulk via the terminal:
```bash
python -m unittest discover tests
```
This ensures regression testing is fast and reliable.

---

# 9. Exception Handling
## 9.1 Strategy
Robust error handling prevents the application from crashing effectively.

## 9.2 Implementation
- **Database Level:** `db_connection.py` uses `try-except` to catch `pyodbc.Error` and print friendly troubleshooting messages (e.g., "Check Server Name").
- **GUI Level:** All Controller calls are wrapped. If `TransactionController.add_transaction` fails, the GUI catches the boolean `False` return and shows a `messagebox.showerror`.
- **Input Validation:** inputs are validated (e.g., Amount must be float) before ever reaching the database layer, preventing SQL errors.

---

# 10. Peer Reviews (Inspections & Walkthroughs)
## 10.1 Workflow
The development process followed a "Propose -> Review -> Implement" cycle.
- **Design Review:** The Entity-Relationship schema for Users/Transactions was reviewed before creating SQL tables.
- **Code Walkthrough:** The move to `TransactionController` was proposed in an Implementation Plan artifact and approved by the User ("Project Lead").

---

# 11. System Architecture
## 11.1 Pattern: MVC (Model-View-Controller)
- **Model (Database):** SQL Server Tables (`Users`, `Transactions`, `Categories`).
- **View (GUI):** 
    - `gui_auth.py` (Login/Register)
    - `gui_dashboard.py` (Main Hub)
    - `gui_transactions.py` (History/Add)
    - `gui_transfer.py` (Send Money)
- **Controller (Logic):** 
    - `user_controller.py` (Auth logic)
    - `transaction_controller.py` (Business rules)

---

# 12. Features and Modules
## 12.1 Authentication Module
- Secure Login with Username/Password.
- Registration with default "Account Number" assignment.

## 12.2 Dashboard
- Displays **Current Balance**.
- Generates a personal **QR Code** (encoding Account #) for easy sharing.
- Quick navigation to sub-modules.

## 12.3 Transaction System
- **Add Income/Expense:** Categorized (Food, Rent, Salary).
- **Transfer Funds:** P2P sending to other users via Account Number.
- **History:** Searchable/Viewable list of all past activity.

## 12.4 Reporting
- **PDF Receipts:** Generate professional PDF receipts for any selected transaction.

---

# 13. Database Design
## 13.1 Schema Overview
- **Users Table:** `user_id`, `username`, `password`, `account_number`, `balance` (derived or stored).
- **Categories Table:** `category_id`, `category_name`, `type` (Income/Expense).
- **Transactions Table:** 
    - `trans_id` (PK)
    - `user_id` (FK)
    - `category_id` (FK)
    - `amount`
    - `trans_date`
    - `description`
    - `related_transaction_id` (For transfers - auditing sender/receiver link)

---

# 14. User Interface Design
## 14.1 Philosophy
"Clean & Professional". We avoided cluttering the interface.
- **Dashboard:** simple "Cards" layout for Balance and Actions.
- **Consistent Styling:** Uniform button sizes, padding, and fonts (Arial) across all windows.
- **Feedback:** Immediate visual feedback via Message Boxes for every action (Success/Error).

---

# 15. Security Implementation
## 15.1 Current Measures
- **Parameterized Queries:** All SQL commands use `?` placeholders to prevent SQL Injection attacks.
- **Input Sanitization:** String inputs are stripped of whitespace; IDs are validated as Integers.
- **Exception Masking:** Database connection strings and raw error traces are hidden from the End User; only generic error messages are shown in GUI.

---

# 16. Testing Strategy
- **Unit Tests:** Run automatically to verify business logic rules (Model/Controller).
- **Integration Tests:** Manual verification of the entire flow: Default User -> Login -> Add Money -> Verify Balance Update.
- **Edge Case Testing:**
    - Sending money to a non-existent account (Handled).
    - Entering negative amounts (Handled).
    - Database server offline (Handled via Graceful Exit).

---

# 17. Future Enhancements
- **Password Hashing:** Implement `bcrypt` for storing passwords securely instead of plain text.
- **Cloud Database:** Migrate from local SQL Server/SQLite to Azure SQL or AWS RDS for global access.
- **Mobile Port:** Use Kivy or Flutter to port the logic to Android/iOS.
- **Live Bank Integration:** Use Plaid API for real bank transactions.

---

# 18. Conclusion
The Smart Pay App project successfully met its primary objectives. By adhering to **Lehman's Laws** and utilizing **Agile SPI**, we evolved a simple script into a structured, maintainable, and extensible financial application. The project serves as a concrete example of applying academic Software Construction principles to real-world application development.

---

# 19. References
## 19.1 Software Engineering Concepts
- Lehman, M. M. (1980). "Programs, Life Cycles, and Laws of Software Evolution"
- Sommerville, I. (2016). "Software Engineering" (10th Edition)
- Martin, R. C. (2008). "Clean Code: A Handbook of Agile Software Craftsmanship"
- Fowler, M. (2018). "Refactoring: Improving the Design of Existing Code"

## 19.2 Technical Documentation
- Python Software Foundation. (2024). "Python 3 Documentation"
- Microsoft. (2024). "SQL Server Technical Documentation"
- Tkinter Documentation. (2024). "Tkinter GUI Programming"
- Pytest Documentation. (2024). "Getting Started with Pytest"

## 19.3 Agile Methodologies
- Schwaber, K., & Sutherland, J. (2020). "The Scrum Guide"
- Beck, K. (2002). "Test Driven Development: By Example"

---

# Appendix A: Installation Guide
## A.1 Prerequisites
- Python 3.10 or higher
- `pip` package manager
- SQL Server (Local or Express edition)
- Git (for cloning repository)

## A.2 Installation Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/Smart-Pay-App.git
   ```
2. **Navigate to project directory:**
   ```bash
   cd Smart-Pay-App
   ```
3. **Create virtual environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   # Activate:
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   ```
4. **Install dependencies:**
   ```bash
   pip install pyodbc qrcode fpdf pillow
   ```
5. **Database Setup:**
   Ensure SQL Server is running. The app will attempt to connect to:
   `Driver={SQL Server};Server=DESKTOP-XXXX;Database=SmartPayDB;`
   *(Update `db_connection.py` if your server name differs)*

6. **Run the application:**
   ```bash
   python main.py
   ```

## A.3 Default Login Credentials
Since this is a personal banking app simulation, there are **no pre-seeded users**.
- **Action:** Launch the app and click **"Register"** to create your first Admin/User account.

---

# Appendix B: Troubleshooting
## B.1 Common Issues
- **Issue:** `pyodbc.Error: ('08001', ...)`
  - **Solution:** Verify your SQL Server is running and the `SERVER` name in `db_connection.py` matches your machine (run `hostname` in cmd).

- **Issue:** `ModuleNotFoundError: No module named 'PIL'`
  - **Solution:** Run `pip install pillow`.

- **Issue:** QR Code not displaying
  - **Solution:** Ensure the `receipts/` folder exists for saving temporary images.

## B.2 Support
For issues and support, please contact the **Smart Pay App Development Team**.

---
**Document Version:** 1.0
**Last Updated:** December 28, 2025
**Prepared By:** Smart Pay App Development Team
**Course:** Software Construction and Development
