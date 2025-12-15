import pyodbc
from tkinter import messagebox

class DBConnection:
    @staticmethod
    def get_connection():
        # Update these details as per your SQL Server configuration
        server =  r'localhost\SQLEXPRESS' # Updated by auto-fixer
        database = 'SmartPayDB'
        
        # Windows Authentication (Trusted_Connection=yes)
        # If using SQL Login, change to: UID=username;PWD=password
        drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
        driver = drivers[0] if drivers else 'ODBC Driver 17 for SQL Server'

        conn_str = (
            f'DRIVER={{{driver}}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'Trusted_Connection=yes;'
        )
        
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database.\nError: {e}")
            return None
