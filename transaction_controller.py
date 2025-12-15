from db_connection import DBConnection
import pyodbc

class TransactionController:
    @staticmethod
    def get_categories():
        conn = DBConnection.get_connection()
        if not conn:
            return []
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT category_id, category_name FROM Categories")
            rows = cursor.fetchall()
            return [{"id": row[0], "name": row[1]} for row in rows]
        except:
            return []
        finally:
            conn.close()

    @staticmethod
    def add_transaction(user_id, category_id, amount, trans_type, date, description=""):
        conn = DBConnection.get_connection()
        if not conn:
            return False, "Database connection failed"
        
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Transactions (user_id, category_id, amount, trans_type, trans_date, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (user_id, category_id, amount, trans_type, date, description))
            conn.commit()
            return True, "Transaction added successfully"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def get_user_transactions(user_id):
        conn = DBConnection.get_connection()
        if not conn:
            return []
        
        cursor = conn.cursor()
        try:
            # INNER JOIN to get category details
            # Added description to selection
            query = """
                SELECT t.trans_id, c.category_name, t.amount, t.trans_type, t.trans_date, t.description
                FROM Transactions t
                INNER JOIN Categories c ON t.category_id = c.category_id
                WHERE t.user_id = ?
                ORDER BY t.trans_date DESC
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            return rows
        except:
            return []
        finally:
            conn.close()

    @staticmethod
    def get_balance(user_id):
        conn = DBConnection.get_connection()
        if not conn:
            return 0.0
        
        cursor = conn.cursor()
        try:
            # Calculate Balance = Total Income - Total Expense
            query = """
                SELECT 
                    SUM(CASE WHEN trans_type = 'Income' THEN amount ELSE 0 END) as TotalIncome,
                    SUM(CASE WHEN trans_type = 'Expense' THEN amount ELSE 0 END) as TotalExpense
                FROM Transactions
                WHERE user_id = ?
            """
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            if row:
                income = float(row[0]) if row[0] else 0.0
                expense = float(row[1]) if row[1] else 0.0
                return income - expense
            return 0.0
        except Exception as e:
            print(f"Error in get_balance: {e}")
            return 0.0
        finally:
            conn.close()

    @staticmethod
    def process_transfer(sender_id, receiver_id, amount, date):
        conn = DBConnection.get_connection()
        if not conn:
            return False, "Database connection failed"
        
        cursor = conn.cursor()
        try:
            # Get IDs for transfer categories
            cursor.execute("SELECT category_id FROM Categories WHERE category_name = 'Transfer Sent'")
            row_sent = cursor.fetchone()
            cursor.execute("SELECT category_id FROM Categories WHERE category_name = 'Transfer Received'")
            row_received = cursor.fetchone()

            if not row_sent or not row_received:
                return False, "Transfer categories not found in DB"

            cat_sent_id = row_sent[0]
            cat_received_id = row_received[0]

            # Get Usernames for description
            cursor.execute("SELECT username FROM Users WHERE user_id = ?", (sender_id,))
            sender_name = cursor.fetchone()[0]
            cursor.execute("SELECT username FROM Users WHERE user_id = ?", (receiver_id,))
            receiver_name = cursor.fetchone()[0]

            # Start Transaction
            # 1. Deduct from Sender (Expense)
            desc_sent = f"Sent to {receiver_name}"
            query_expense = """
                INSERT INTO Transactions (user_id, category_id, amount, trans_type, trans_date, description)
                VALUES (?, ?, ?, 'Expense', ?, ?)
            """
            cursor.execute(query_expense, (sender_id, cat_sent_id, amount, date, desc_sent))

            # 2. Add to Receiver (Income)
            desc_received = f"Received from {sender_name}"
            query_income = """
                INSERT INTO Transactions (user_id, category_id, amount, trans_type, trans_date, description)
                VALUES (?, ?, ?, 'Income', ?, ?)
            """
            cursor.execute(query_income, (receiver_id, cat_received_id, amount, date, desc_received))

            conn.commit()
            return True, "Transfer successful"
        except Exception as e:
            conn.rollback()
            return False, f"Transfer failed: {str(e)}"
        finally:
            conn.close()
