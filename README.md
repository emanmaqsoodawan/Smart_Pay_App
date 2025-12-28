# Smart Pay App

**Smart Pay App** is a comprehensive desktop-based personal finance management system built with Python. It allows users to manage their daily finances, track income/expenses, and perform peer-to-peer (P2P) money transfers. The application acts as a digital wallet with professional features like QR code generation and PDF transaction receipts.

---

## 🚀 Key Features

*   **User Management**: Secure registration and login with unique, auto-generated 10-digit Account IDs.
*   **Interactive Dashboard**: View live balance, account details, and a personal QR code.
*   **Financial Tracking**: Log Income and Expenses with categories and dates.
*   **P2P Money Transfer**: Send money to other users instantly using their account number or username.
*   **Transaction History**: View a detailed history of all financial activities (Income, Expenses, Transfers).
*   **PDF Receipts**: Generate instant transaction receipts or download past receipts from history.
*   **Data Persistence**: Robust data storage using Microsoft SQL Server.

## 🛠️ Technology Stack

*   **Language**: Python 3.x
*   **GUI**: Tkinter
*   **Database**: Microsoft SQL Server (Express Edition)
*   **Libraries**: `pyodbc`, `fpdf`, `qrcode`, `Pillow`

## 📋 Prerequisites

Before running the application, ensure you have the following installed:
1.  **Python 3.x**: [Download Python](https://www.python.org/downloads/)
2.  **Microsoft SQL Server Express**: [Download SQL Server](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)

## ⚙️ Installation & Setup

1.  **Clone the Repository** (if applicable) or download the source code.

2.  **Install Dependencies**
    Open your terminal/command prompt and run:
    ```bash
    pip install pyodbc qrcode[pil] fpdf
    ```

3.  **Database Configuration**
    *   Ensure your SQL Server instance is running.
    *   Run the setup script to create the database and required tables:
    ```bash
    python maintenance_scripts/setup_db_auto.py
    ```
    *(Alternatively, you can run the SQL commands in `database_setup.sql` manually via SSMS).*

## ▶️ Usage

To launch the application, run the main script from the project root:

```bash
python main.py
```

### Navigating the App:
*   **Login/Register**: Create an account or log in.
*   **Dashboard**: Your central hub.
*   **Add Transaction**: Use the "Add Income" or "Add Expense" buttons.
*   **Send Money**: Navigate to the transfer section to send funds.
*   **History**: View past logs and generate PDF receipts.

## 📂 Project Structure

*   `main.py`: Application entry point.
*   `gui_*.py`: UI components for Dashboard, Auth, Transactions, etc.
*   `*_controller.py`: Business logic for User and Transaction management.
*   `db_connection.py`: Database connection handler.
*   `utils.py`: Helpers for PDF and QR code generation.
*   `maintenance_scripts/`: Database setup and maintenance utilities.
*   `receipts/`: Folder where generated PDF receipts are saved.

---
*Created for the Smart Pay App project.*
